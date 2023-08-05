import torch
import os.path as osp
import pandas as pd
import re
from tqdm import tqdm
from .utils import Process
from .structure_modeling import make_structure
from .pshm import parse_pdbdata

DEFAULT_DIR = osp.dirname(osp.realpath(__file__))
re_hla = re.compile(r'(HLA\-[ABC])(.*)')
hla_table = pd.read_table(osp.join(DEFAULT_DIR, 'MHC_pseudo.dat'))
hla_dict = {}
for tup in hla_table.itertuples():
    hla = tup.HLA
    seq = tup.sequence
    if re_hla.match(hla):
        hla = re_hla.match(hla).group(1) + '*' + re_hla.match(hla).group(2)
        hla_dict[hla] = seq


def make_annotations(nums):
    return ['pmhc'+str(i).zfill(len(str(nums))) for i in range(1, nums+1)]


def make_sequence_tensor(peptide, hla):
    hla_seq = hla_dict[hla]
    seq = hla_seq + peptide
    process = Process(seqs=[seq])
    return process.seqs_aa2idx()


def make_data_from_pdb(peptide, hla, pdb_file, protein='A', ligand='C'):
    cnn_data = torch.Tensor(parse_pdbdata(
        pdb_file, protein, ligand)).reshape((1, 16, 360))
    rnn_data = make_sequence_tensor(peptide, hla)
    return cnn_data, rnn_data


def make_data_from_csv(df, sequence_only=False):
    peptides = df['peptide']
    hlas = df['HLA']
    annos = df['Annotation']
    cnn_datas = torch.zeros((len(peptides), 1, 16, 360))
    rnn_datas = torch.zeros((len(peptides), 49)).long()
    skipped_idx = []
    if not sequence_only:
        i = 0
        pbar = tqdm(total=len(df), desc="Preprocessing")
        for peptide, hla, anno in zip(peptides, hlas, annos):
            output_pdb = make_structure(
                peptide, hla, anno, structure_dir='structures')
            if output_pdb is not None:
                cnn_data, rnn_data = make_data_from_pdb(
                    peptide, hla, output_pdb)
                cnn_datas[i] = cnn_data
                rnn_datas[i] = rnn_data
            else:
                skipped_idx.append(i)
            i += 1
            pbar.update(1)
        pbar.close()
    else:
        i = 0
        pbar = tqdm(total=len(df), desc="Preprocessing")
        for peptide, hla, anno in zip(peptides, hlas, annos):
            rnn_datas[i] = make_sequence_tensor(peptide, hla)
            i += 1
            pbar.update(1)
        pbar.close()
    return cnn_datas, rnn_datas, skipped_idx
