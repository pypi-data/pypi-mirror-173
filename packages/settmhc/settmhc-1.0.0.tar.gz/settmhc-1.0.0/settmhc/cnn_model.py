from argparse import Namespace
import numpy as np
import torch
import torch.nn as nn
import pytorch_lightning as pl
from torchmetrics import Accuracy
import math
from .utils import get_linear_schedule_with_warmup


class Positional_wise_input(nn.Module):
    def __init__(self, embed_dim, max_length, gpu=0):

        super().__init__()
        self.encoding = []
        for pos in range(max_length):
            ls = [pos / (10000.0 ** (i // 2 * 2.0 / embed_dim))
                  for i in range(embed_dim)]
            self.encoding.append(ls)
        self.encoding = np.array(self.encoding)
        self.encoding[:, 0::2] = np.sin(self.encoding[:, 0::2])
        self.encoding[:, 1::2] = np.cos(self.encoding[:, 1::2])
        self.encoding = torch.Tensor(self.encoding)

    def forward(self, x: torch.Tensor):
        # x: [batch, embed_dim, width]
        x = x.permute(0, 2, 1)
        encoding = self.encoding.to(x.device)
        out = x + encoding
        return out


class CNN_model(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        # out_size = (n+2p-f)/s + 1
        acti_func = config['activation']
        conv1_size = config['conv1']
        conv2_size = config['conv2']
        conv3_size = config['conv3']
        kernel1_size = config['kernel1']
        kernel2_size = config['kernel2']
        kernel3_size = config['kernel3']
        dropout = config['dropout']
        width = config['width']
        height = 5760//width
        if acti_func == 'relu':
            self.activation = nn.ReLU(inplace=True)
        elif acti_func == 'tanh':
            self.activation = nn.Tanh()
        elif acti_func == 'leaky_relu':
            self.activation = nn.LeakyReLU(negative_slope=0.01)

        self.convs = nn.Sequential(
            nn.Conv2d(1, conv1_size, kernel_size=kernel1_size,
                      padding='same'),
            nn.Dropout(dropout),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(conv1_size, conv2_size,
                      kernel_size=kernel2_size, padding='same'),
            nn.Dropout(dropout),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(conv2_size, conv3_size,
                      kernel_size=kernel3_size, padding='same'),
            nn.Dropout(dropout),
        )
        self.cnn_size = int(conv3_size*(height//2//2)*(width//2//2))

        # This FC module dosen't work in the model prediction, but the absence of the module may cause some dropout issues.
        self.fc = nn.Sequential(
            nn.Linear(self.cnn_size, 256),
            self.activation,
            nn.Linear(256, 64),
            self.activation,
            nn.Linear(64, 1),
        )

    def forward(self, x):
        pass


class PL_CNN(pl.LightningModule):
    def __init__(self, config, total_steps, warmup_ratio=0.1, gpu=0):
        super().__init__()
        self.model = CNN_model(config)
        self.total_steps = total_steps
        self.warmup_ratio = warmup_ratio
        self.warmup_steps = math.ceil(total_steps * warmup_ratio)
        self.conv_type = config['conv_type']
        self.cnn_outsize = self.model.cnn_size
        self.final_fc = nn.Sequential(
            nn.Linear(self.cnn_outsize, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
        self.config = config
        self.gpu = gpu
        self.batch_size = config['batch_size']
        self.acti_func = config['activation']
        self.train_acc = Accuracy()
        self.val_acc = Accuracy()
        self.save_hyperparameters(Namespace(**config))

    def forward(self, x):
        out = self.model.convs(x)
        out = out.flatten(1, -1)
        out = self.final_fc(out)
        out = torch.sigmoid(out)
        return out

    def get_cnn_feature(self, x):
        out = self.model.convs(x)
        out = out.flatten(1, -1)
        return out

    def get_loss(self, pred, label):
        loss = nn.BCELoss()
        return loss(pred, label.float())

    def training_step(self, batch, batch_idx):
        input, label = batch
        pred = self(input).squeeze(-1)
        loss = self.get_loss(pred, label)
        self.log(f'loss/train_loss', loss)
        self.train_acc(pred, label.int())
        self.log(f'acc/train_acc', self.train_acc,
                 on_step=False, on_epoch=True)
        return {'loss': loss}

    def validation_step(self, batch, batch_idx):
        input, label = batch
        pred = self(input).squeeze(-1)
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
