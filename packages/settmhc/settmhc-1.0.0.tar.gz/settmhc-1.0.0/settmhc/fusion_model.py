import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import math
import warnings
from torchmetrics import Accuracy
from .rnn_model import GRU_model
from .cnn_model import PL_CNN
from .utils import get_linear_schedule_with_warmup
from argparse import Namespace
warnings.filterwarnings(action='ignore')


class Fusion_model(nn.Module):
    def __init__(self, config, fusion_type, total_steps, use_weight=False, gpu=0):
        super().__init__()
        self.gpu = gpu
        self.use_weight = use_weight
        self.fusion_type = fusion_type
        self.config = config
        acti_func = config['activation']
        self.dropout = config['dropout']
        self.conv_type = config['conv_type']
        if self.use_weight:
            self.cnn_weight = nn.Parameter(torch.tensor(
                config['cnn_weight']), requires_grad=True)
            self.rnn_weight = nn.Parameter(torch.tensor(
                config['rnn_weight']), requires_grad=True)

        self.cnn = PL_CNN(config, total_steps=total_steps)
        self.rnn = GRU_model(config=config, dropout=self.dropout,
                             bidirectional=True, use_attention=True)

        if acti_func == 'relu':
            self.activation = nn.ReLU()
        elif acti_func == 'tanh':
            self.activation = nn.Tanh()
        elif acti_func == 'leaky_relu':
            self.activation = nn.LeakyReLU(negative_slope=0.01)
        self.indiv_fc_size = config['final_fc']

        self.cnn_fc = nn.Sequential(
            nn.Linear(self.cnn.cnn_outsize, self.indiv_fc_size), self.activation)
        self.rnn_fc = nn.Sequential(
            nn.Linear(self.rnn.rnn_outsize, self.indiv_fc_size),
            self.activation
        )
        self.fc = nn.Sequential(
            nn.Linear(self.indiv_fc_size, 512),
            self.activation,
            nn.Linear(512, 512),
            self.activation,
            nn.Linear(512, 256),
            self.activation,
            nn.Linear(256, 1))

    def forward(self, cnn_input, rnn_input):
        cnn_features = self.cnn.get_cnn_feature(cnn_input)
        rnn_features = self.rnn.get_rnn_feature(rnn_input)
        if self.use_weight:
            cnn_features = self.cnn_weight * cnn_features
            rnn_features = self.rnn_weight * rnn_features
        self.cnn_fc_out = F.dropout(self.cnn_fc(cnn_features), self.dropout)
        self.rnn_fc_out = F.dropout(self.rnn_fc(rnn_features), self.dropout)
        out = self.cnn_fc_out + self.rnn_fc_out
        out = self.fc(out)
        out = torch.sigmoid(out)
        return out


class  PL_fusion(pl.LightningModule):
    def __init__(self, config, total_steps, warmup_ratio=0.1, fusion_type='backbone', use_weight=False, gpu=0):
        super().__init__()
        self.fusion_type = fusion_type
        self.gpu = gpu
        self.total_steps = total_steps
        self.warmup_ratio = warmup_ratio
        self.warmup_steps = math.ceil(total_steps * warmup_ratio)
        self.model = Fusion_model(
            config, fusion_type, total_steps, use_weight, gpu)
        self.config = config
        self.batch_size = config['batch_size']
        self.acti_func = config['activation']
        self.train_acc = Accuracy()
        self.val_acc = Accuracy()
        self.save_hyperparameters(Namespace(**config))

    def forward(self, cnn_input, rnn_input):
        return self.model(cnn_input, rnn_input)

    def get_loss(self, pred, label):
        loss = nn.BCELoss()
        return loss(pred, label.float())

    def training_step(self, batch, batch_idx):
        cnn_input = batch['cnn_input']
        rnn_input = batch['rnn_input']
        label = batch['label']
        pred = self.forward(cnn_input=cnn_input,
                            rnn_input=rnn_input).squeeze()
        loss = self.get_loss(pred, label)
        self.log(f'loss/train_loss', loss)
        self.train_acc(pred, label.int())
        self.log(f'acc/train_acc', self.train_acc,
                 on_step=False, on_epoch=True)
        opt = self.optimizers()
        self.log('lr', opt.state_dict()['param_groups'][0]['lr'])
        return {'loss': loss}

    def validation_step(self, batch, batch_idx):
        cnn_input = batch['cnn_input']
        rnn_input = batch['rnn_input']
        label = batch['label']
        pred = self.forward(cnn_input=cnn_input,
                            rnn_input=rnn_input).squeeze(-1)
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
