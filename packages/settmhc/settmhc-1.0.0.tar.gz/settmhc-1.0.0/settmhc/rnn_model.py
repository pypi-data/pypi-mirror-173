from argparse import Namespace
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torchmetrics import Accuracy
import math
from .utils import get_linear_schedule_with_warmup, aa_idx


class Attention(nn.Module):
    def __init__(self, atten_size, return_attention=False):
        super().__init__()
        self.w = nn.Parameter(torch.rand(atten_size, 1))
        self.b = nn.Parameter(torch.zeros(atten_size))
        self.return_attention = return_attention

    def forward(self, x: torch.Tensor):
        # [seq_len, batch, num_directions * hidden_size]
        assert len(x.size()) == 3
        assert self.w.size(0) == x.size(-1)
        elements = torch.matmul(x, self.w) + self.b
        elements = F.tanh(elements)  # [seq_len, batch, 1]
        alpha = F.softmax(elements, dim=0)  # [seq_len, batch, 1]
        out = x * alpha  # [seq_len, batch, num_directions * hidden_size]
        out = out.sum(dim=0)  # [batch, num_directions * hidden_size]
        assert out.size(0) == x.size(1)
        if self.return_attention:
            return out, alpha
        return out


class GRU_model(nn.Module):
    def __init__(self, config, dropout, bidirectional, use_attention=False):
        super().__init__()
        self.use_attention = use_attention
        self.n_direction = 2 if bidirectional else 1
        self.embed_dim = config['embed_dim']
        self.rnn_dim = config['rnn_dim']
        self.embedding = nn.Embedding(len(aa_idx), self.embed_dim)
        self.gru = nn.GRU(self.embedding.embedding_dim, self.rnn_dim, num_layers=3,
                          dropout=dropout, bidirectional=bidirectional)
        self.rnn_outsize = self.gru.hidden_size * self.n_direction
        self.linear = nn.Linear(self.rnn_outsize, 1)
        self.attention = Attention(atten_size=self.rnn_outsize)

    def forward(self, x):
        x = self.embedding(x)
        x = x.transpose(1, 0)
        output, hidden = self.gru(x)
        # output [seq_len, batch, num_directions * hidden_size]
        # hidden [num_layers * num_directions, batch, hidden_size]
        if self.n_direction == 2:
            # [batch, hidden_size * num_directions]
            hidden = torch.cat([hidden[-1], hidden[-2]], dim=1)
        else:
            hidden = hidden[-1]
        assert hidden.size(1) == self.n_direction*self.gru.hidden_size
        if self.use_attention:
            out = self.attention(output)
        else:
            out = hidden
        out = self.linear(out)
        out = torch.sigmoid(out)
        return out

    def get_rnn_feature(self, x, return_seq=False):
        x = self.embedding(x)
        x = x.transpose(1, 0)
        output, hidden = self.gru(x)
        # output [seq_len, batch, num_directions * hidden_size]
        # hidden [num_layers * num_directions, batch, hidden_size]
        if return_seq:
            return output.transpose(1, 0)
        if self.n_direction == 2:
            # [batch, hidden_size * num_directions]
            hidden = torch.cat([hidden[-1], hidden[-2]], dim=1)
        else:
            hidden = hidden[-1]
        assert hidden.size(1) == self.n_direction*self.gru.hidden_size
        if self.use_attention:
            out = self.attention(output)
        else:
            out = hidden
        return out


class PL_Sequence(pl.LightningModule):
    def __init__(self, config, total_steps, gpu=0):
        super().__init__()
        self.config = config
        self.total_steps = total_steps
        self.warmup_steps = math.ceil(total_steps * 0.1)
        self.gpu = gpu
        self.batch_size = config['batch_size']
        self.model_type = 'att_BGRU'
        self.dropout = config['dropout']
        self.train_acc = Accuracy()
        self.val_acc = Accuracy()
        self.save_hyperparameters(Namespace(**config))
        if self.model_type == 'GRU':
            self.model = GRU_model(
                config=config, dropout=self.dropout, bidirectional=False, use_attention=False)
        elif self.model_type == 'BGRU':
            self.model = GRU_model(
                config=config, dropout=self.dropout, bidirectional=True, use_attention=False)
        elif self.model_type == 'att_BGRU':
            self.model = GRU_model(
                config=config, dropout=self.dropout, bidirectional=True, use_attention=True)
        # print(self.model)

    def forward(self, x):
        out = self.model(x)
        return out

    def get_loss(self, pred, label):
        loss = nn.BCELoss()
        return loss(pred, label.float())

    def training_step(self, batch, batch_idx):
        input, label = batch
        pred = self.forward(input).squeeze(-1)
        loss = self.get_loss(pred, label)
        self.log(f'loss/train_loss', loss)
        self.train_acc(pred, label.int())
        self.log(f'acc/train_acc', self.train_acc,
                 on_step=False, on_epoch=True)
        return {'loss': loss}

    def validation_step(self, batch, batch_idx):
        input, label = batch
        pred = self.forward(input).squeeze(-1)
        loss = self.get_loss(pred, label)
        self.val_acc(pred, label.int())
        self.log('acc/val_acc', self.val_acc, on_step=False, on_epoch=True)
        return {'val_loss': loss}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        self.log(f'loss/val_loss', avg_loss)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(), lr=1e-3, weight_decay=1e-2)
        scheduler = get_linear_schedule_with_warmup(
            optimizer, num_warmup_steps=self.warmup_steps, num_training_steps=self.total_steps)
        return {'optimizer': optimizer, 'lr_scheduler': scheduler}
