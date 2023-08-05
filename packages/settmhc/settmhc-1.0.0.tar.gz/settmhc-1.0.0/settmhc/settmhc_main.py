import argparse
import logging
import torch
import time
import os
import os.path as osp
import sys
import yaml
import numpy as np
import pandas as pd
import itertools
from subprocess import run
from appdirs import user_data_dir
from tqdm import tqdm
from tempfile import NamedTemporaryFile
from copy import deepcopy
from urllib.request import urlretrieve
from .fusion_model import PL_fusion
from .rnn_model import PL_Sequence
from .preprocess import make_data_from_pdb, make_data_from_csv, make_annotations
from .structure_modeling import check_hlas, supported_hlas

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
DEFAULT_DIR = osp.dirname(osp.realpath(__file__))
MODEL_DIR = os.environ.get("SETTMHC_MODEL_DIR")
if MODEL_DIR is None:
    MODEL_DIR = user_data_dir("settmhc")
if not osp.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)
with open(osp.join(DEFAULT_DIR, 'hparams.yaml')) as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--peptides', nargs='*', metavar='FSDVGEVPY',
                    help="Peptides for SETTMHC prediction, length from 8-11")
parser.add_argument('--hlas', nargs='*', metavar='HLA-A*02:01',
                    help="HLA alleles for SETTMHC prediction")
parser.add_argument('-i', '--input', metavar='input.csv',
                    help="Input file for prediction, see demo/demo.csv")
parser.add_argument('-o', '--output', metavar='output.csv',
                    help="Output file for results")
parser.add_argument('--sequence_only', action='store_true',
                    help="Use only sequence model to predict, but it's not recommended")
parser.add_argument('--download', action='store_true',
                    help="Download model files from Zenodo, default download to 'user_data_dir'")
parser.add_argument('--list_supported_hlas', action='store_true',
                    help="List all the supported 110 HLA alleles.")

pdb_args = parser.add_argument_group(
    title="Input single PDB file for prediction")
pdb_args.add_argument(
    '--pdb', help=" Single PDB/ent file for pMHC complex structure ('--peptides' and '--hlas' should also be given)")
pdb_args.add_argument('--protein', help='Protein chain in the input PDB file')
pdb_args.add_argument('--ligand', help='Ligand chain in the input PDB file')


def predict(cnn_data, rnn_data, skipped_idx):
    test_preds = np.zeros((5, len(cnn_data)))
    for i in range(1, 6):
        ckpt_path = osp.join(MODEL_DIR, f'model/Fusion/model{i}.ckpt')
        model = PL_fusion.load_from_checkpoint(
            checkpoint_path=ckpt_path, config=CONFIG, total_steps=8888, strict=False, map_location=DEVICE)
        model.eval()
        with torch.no_grad():
            pred = model(cnn_data, rnn_data)
            test_preds[i-1] = pred.squeeze().numpy()
    test_preds[:, skipped_idx] = 0
    preds = np.mean(test_preds, axis=0)
    return preds


def seq_predict(rnn_data):
    test_preds = np.zeros((5, len(rnn_data)))
    for i in range(1, 6):
        ckpt_path = osp.join(MODEL_DIR, f'model/RNN/model{i}.ckpt')
        model = PL_Sequence.load_from_checkpoint(
            checkpoint_path=ckpt_path, config=CONFIG, total_steps=8888, strict=False, map_location=DEVICE)
        model.eval()
        with torch.no_grad():
            pred = model(rnn_data)
            test_preds[i-1] = pred.squeeze().numpy()
    preds = np.mean(test_preds, axis=0)
    return preds


class DownloadBar(tqdm):
    def download_update(self, blocknum=1, blocksize=1, totalsize=None):
        if totalsize is not None:
            self.total = totalsize
        self.update(blocknum * blocksize - self.n)


def download_models():
    MODEL_URL = 'https://zenodo.org/record/7226854/files/model.tar.gz?download=1'
    temp = NamedTemporaryFile(delete=False, suffix='.tar.gz')
    print(f"Download model file in {temp.name}")

    urlretrieve(MODEL_URL, temp.name, reporthook=DownloadBar(
        unit='B', unit_scale=True).download_update)
    temp.close()
    run(f"tar -xf {temp.name} -C {MODEL_DIR}", shell=True)
    print(
        f'Extracted {temp.name} to {MODEL_DIR}, you may delete the temp file manually')


def check_models():
    return osp.exists(osp.join(MODEL_DIR, 'model'))


def main(argv=sys.argv[1:]):
    args = parser.parse_args(argv)
    if args.download:
        download_models()
        already_download = check_models()
        if not already_download:
            print(
                "Downloads for models failed. May visit https://zenodo.org/record/7226854 manually")
        return
    else:
        already_download = check_models()
        if not already_download:
            print(
                f"There is no file in {MODEL_DIR}. Must use --download to get models for the first application")
            return

    if args.list_supported_hlas:
        print(supported_hlas)
        return

    if args.pdb:
        if args.sequence_only:
            parser.error(
                "If a PDB file is specified, sequence_only must not be specified")
        if not args.peptides or not args.hlas:
            parser.error(
                "If a PDB file is specified, peptide and hla must be given")
        check_hlas(args.hlas)
        cnn_data, rnn_data = make_data_from_pdb(
            args.peptides[0], args.hlas[0], args.pdb, args.protein, args.ligand)
        cnn_data = cnn_data.unsqueeze(0)
        df = pd.DataFrame({'peptide': args.peptides, 'HLA': args.hlas})
    elif args.input:
        if args.peptides or args.hlas:
            parser.error(
                "If an input csv file is specified, peptides or hlas should not be specified")
        df = pd.read_csv(args.input)
        check_hlas(df['HLA'])
        annos = df['Annotation'] if 'Annotation' in df.columns else make_annotations(
            len(df))
        df['Annotation'] = annos
        cnn_data, rnn_data, skipped_idx = make_data_from_csv(
            df, sequence_only=args.sequence_only)
    else:
        if not args.peptides or not args.hlas:
            parser.error(
                "Either specify an input csv file or peptides and hlas")
        check_hlas(args.hlas)
        ls = list(itertools.product(args.peptides, args.hlas))
        df = pd.DataFrame(ls, columns=['peptide', 'HLA'])
        annos = df['Annotation'] if 'Annotation' in df.columns else make_annotations(
            len(df))
        df['Annotation'] = annos
        cnn_data, rnn_data, skipped_idx = make_data_from_csv(
            df, sequence_only=args.sequence_only)

    # make predictions
    if args.sequence_only:
        preds = seq_predict(rnn_data)
    else:
        preds = predict(cnn_data, rnn_data, skipped_idx)

    output_df = deepcopy(df)
    output_df['Prediction_scores'] = preds
    if not args.output:
        now = time.strftime("%Y%m%d-%H_%M", time.localtime(time.time()))
        output_file = f'{now}_predictions.csv'
        logging.warning(
            f'Output file is not specified, the results will be saved in {output_file}')
    else:
        output_file = args.output
    output_df.to_csv(output_file, index=False)
