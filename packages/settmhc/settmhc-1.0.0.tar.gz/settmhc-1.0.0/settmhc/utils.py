import torch
import os
import pytorch_lightning as pl
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader, TensorDataset, Dataset
from sklearn.model_selection import train_test_split
from pandas import DataFrame
from Bio.PDB import PDBParser
from Bio.PDB.Selection import unfold_entities
from Bio import BiopythonWarning
import warnings
warnings.simplefilter('ignore', BiopythonWarning)
aa_idx = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10,
          'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19, 'X': 20}


def get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, last_epoch=-1):
    """
    Create a schedule with a learning rate that decreases linearly from the initial lr set in the optimizer to 0, after
    a warmup period during which it increases linearly from 0 to the initial lr set in the optimizer.

    Args:
        optimizer ([`~torch.optim.Optimizer`]):
            The optimizer for which to schedule the learning rate.
        num_warmup_steps (`int`):
            The number of steps for the warmup phase.
        num_training_steps (`int`):
            The total number of training steps.
        last_epoch (`int`, *optional*, defaults to -1):
            The index of the last epoch when resuming training.

    Return:
        `torch.optim.lr_scheduler.LambdaLR` with the appropriate schedule.
    """

    def lr_lambda(current_step: int):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        return max(
            0.0, float(num_training_steps - current_step) /
            float(max(1, num_training_steps - num_warmup_steps))
        )

    return LambdaLR(optimizer, lr_lambda, last_epoch)


class CNN_datamodule(pl.LightningDataModule):
    def __init__(self, config, datas, labels, train_idx, val_idx=None):
        super().__init__()
        self.batch_size = config['batch_size']
        self.config = config
        self.datas = datas
        self.labels = labels
        self.train_idx = train_idx
        self.val_idx = val_idx

    def prepare_data(self):
        data = self.datas
        label = self.labels
        self.data_train = data[self.train_idx]
        self.label_train = label[self.train_idx]
        if self.val_idx is not None:
            self.data_val = data[self.val_idx]
            self.label_val = label[self.val_idx]
        else:
            self.data_train, self.data_val, self.label_train, self.label_val = train_test_split(
                self.data_train, self.label_train, test_size=0.1, random_state=22)
        train_num = self.data_train.shape[0]
        self.data_train = self.data_train.reshape(
            [train_num, 1, -1, self.config['width']])
        val_num = self.data_val.shape[0]
        self.data_val = self.data_val.reshape(
            [val_num, 1, -1, self.config['width']])

        self.train_dataset = TensorDataset(torch.FloatTensor(
            self.data_train), torch.LongTensor(self.label_train))
        self.val_dataset = TensorDataset(torch.FloatTensor(
            self.data_val), torch.LongTensor(self.label_val))

    def setup(self, stage):
        pass

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=4)


class Process():
    def __init__(self, seqs, labels=None, task_type='class', seq_len=49):
        self.seqs = seqs
        self.labels = labels
        self.task_type = task_type
        self.seq_len = seq_len

    @staticmethod
    def pad_seq(seq, seq_len):
        if len(seq) < seq_len:
            padding_len = seq_len - len(seq)
            padding_seq = 'X'*padding_len
            seq = seq + padding_seq
        else:
            seq = seq[:seq_len]
        assert len(seq) == seq_len
        return seq

    def seqs_aa2idx(self):
        seqs_idx = []
        for seq in self.seqs:
            seq = self.pad_seq(seq, seq_len=self.seq_len)
            seqs_idx.append([aa_idx[aa] for aa in seq])
        return torch.LongTensor(seqs_idx)

    def label2tensor(self):
        if self.task_type == 'class':
            y = [int(label) for label in self.labels]
            return torch.LongTensor(y)
        elif self.task_type == 'regression':
            return torch.FloatTensor(self.labels)


class RNN_datamodule(pl.LightningDataModule):
    def __init__(self, config, seqs, labels, train_idx, val_idx=None, task_type='class'):
        super().__init__()
        self.batch_size = config['batch_size']
        self.config = config
        self.seqs = seqs
        self.labels = labels
        self.train_idx = train_idx
        self.val_idx = val_idx
        self.task_type = task_type

    def prepare_data(self):
        seqs = self.seqs
        labels = self.labels

        process = Process(seqs, labels, task_type=self.task_type)
        data = process.seqs_aa2idx()
        label = process.label2tensor()
        self.data_train = data[self.train_idx]
        self.label_train = label[self.train_idx]
        if self.val_idx is not None:
            self.data_val = data[self.val_idx]
            self.label_val = label[self.val_idx]
        else:
            self.data_train, self.data_val, self.label_train, self.label_val = train_test_split(
                self.data_train, self.label_train, test_size=0.1, random_state=22)

        self.train_dataset = TensorDataset(self.data_train, self.label_train)
        self.val_dataset = TensorDataset(self.data_val, self.label_val)

    def setup(self, stage):
        pass

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)


class Fusion_dataset(Dataset):
    def __init__(self, cnn_data, rnn_data, label):
        self.cnn_x = torch.FloatTensor(cnn_data)
        self.rnn_x = torch.tensor(rnn_data)
        self.label = torch.tensor(label)
        assert len(cnn_data) == len(rnn_data)

    def __len__(self):
        return len(self.cnn_x)

    def __getitem__(self, index):
        data = {'cnn_input': self.cnn_x[index],
                'rnn_input': self.rnn_x[index], 'label': self.label[index]}
        return data


class Fusion_datamodule(pl.LightningDataModule):
    def __init__(self, config, cnn_data, rnn_data, labels, train_idx, val_idx=None):
        super().__init__()
        self.config = config
        self.batch_size = config['batch_size']
        self.cnn_data = cnn_data
        self.rnn_data = rnn_data
        self.labels = labels
        self.train_idx = train_idx
        self.val_idx = val_idx

    def prepare_data(self):
        cnn_datamod = CNN_datamodule(
            self.config, self.cnn_data, self.labels, self.train_idx, self.val_idx)
        rnn_datamod = RNN_datamodule(
            self.config, self.rnn_data, self.labels, self.train_idx, self.val_idx)
        cnn_datamod.prepare_data()
        rnn_datamod.prepare_data()
        train_labels = rnn_datamod.label_train
        val_labels = rnn_datamod.label_val
        cnn_train = cnn_datamod.data_train
        cnn_val = cnn_datamod.data_val
        rnn_train = rnn_datamod.data_train
        rnn_val = rnn_datamod.data_val

        self.train_dataset = Fusion_dataset(
            cnn_data=cnn_train, rnn_data=rnn_train, label=train_labels)
        self.val_dataset = Fusion_dataset(
            cnn_data=cnn_val, rnn_data=rnn_val, label=val_labels)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)


def parse_pdb(file) -> DataFrame:
    code = os.path.split(file)[-1].split('.')[0]
    p = PDBParser(PERMISSIVE=1)
    s = p.get_structure(code, file)
    model = s[0]

    atoms = unfold_entities(model, 'A')
    atomHetfield = []
    atomNum = []
    atomName = []
    # altLoc = []

    chainID = []
    resName = []
    resNum = []
    X = []
    Y = []
    Z = []

    for atom in atoms:
        atom_hetfield = atom.full_id[3][0].strip()
        atomHetfield.append(atom_hetfield)
        atom_num = atom.serial_number
        atomNum.append(atom_num)
        atom_name = atom.name
        atomName.append(atom_name[0])

        chain_id = atom.full_id[2]
        chainID.append(chain_id)
        res = atom.parent
        res_name = res.resname
        resName.append(res_name)
        res_num = res.id[1]
        resNum.append(res_num)
        coord = atom.coord
        X.append(coord[0])
        Y.append(coord[1])
        Z.append(coord[2])

    data = {
        'Atom_num': atomNum,
        'Atom_hetfield': atomHetfield,
        'Atom_name': atomName,
        'chain_ID': chainID,
        'Res_name': resName,
        'Res_num': resNum,
        'X': X,
        'Y': Y,
        'Z': Z,
    }

    return DataFrame(data)