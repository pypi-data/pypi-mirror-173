import numpy as np
import sys
import gudhi
import os
import logging
import argparse
from .utils import parse_pdb
from itertools import combinations
from typing import List
from collections import defaultdict
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)
warnings.filterwarnings("ignore")

Protein_Atom = ['C', 'N', 'O', 'S']
Ligand_Atom = ['C', 'N', 'O', 'S']
Ligand_Atom_pairs = list(combinations(Ligand_Atom, 2))
aa_list = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'HSE', 'HSD', 'SEC',
           'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL', 'PYL']
sites = [7, 9, 24, 45, 59, 62, 63, 66, 67, 69, 70, 73, 74, 76, 77, 80, 81,
         84, 95, 97, 99, 114, 116, 118, 143, 147, 150, 152, 156, 158, 159, 163, 167, 171]


def get_barcode(dm, pro_num, lig_num, max_length=15.0):
    zero_bar = []
    if pro_num != 0 and lig_num != 0:
        rips_complex = gudhi.RipsComplex(
            distance_matrix=dm, max_edge_length=max_length)
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
        diag = simplex_tree.persistence()

        for j in range(len(diag)):
            temp = [diag[j][1][0], diag[j][1][1]]
            zero_bar.append(temp)
    zero_bar = np.array(zero_bar)
    return zero_bar


def statistic_of_death(bar, left, right):
    t = bar.shape
    if len(bar) == 0:
        return [0, 0, 0, 0, 0, 0]

    dmax = 0
    dmin = 0
    dave = 0
    dstd = 0
    dsum = 0
    dnum = 0
    value = []
    for i in range(t[0]):
        if (bar[i][1] >= left) & (bar[i][1] <= right):
            value.append(bar[i][1])
    if len(value) == 0:
        return [dmax, dmin, dave, dstd, dsum, dnum]
    else:
        dmax = max(value)
        dmin = min(value)
        dave = np.mean(value)
        dstd = np.std(value)
        dsum = sum(value)
        dnum = len(value)
        return [dmax, dmin, dave, dstd, dsum, dnum]


def statistic_of_persistence(bar, left, right):
    t = bar.shape
    if len(bar) == 0:
        return [0, 0, 0, 0, 0, 0]

    pmax = 0
    pmin = 0
    pave = 0
    pstd = 0
    psum = 0
    pnum = 0
    value = []
    for i in range(t[0]):
        if (bar[i][0] >= left) & (bar[i][1] <= right):
            value.append(bar[i][1]-bar[i][0])
    if len(value) == 0:
        return [pmax, pmin, pave, pstd, psum, pnum]
    else:
        pmax = max(value)
        pmin = min(value)
        pave = np.mean(value)
        pstd = np.std(value)
        psum = sum(value)
        pnum = len(value)
        return [pmax, pmin, pave, pstd, psum, pnum]


def get_static_feature(bar, filtration=15.0, unit=0.5):
    column0 = int(filtration/unit)
    N = 6 * 2  # N is the number of statistic features
    feature_matrix = np.zeros((column0, N))
    for n in range(column0):
        death_feature = statistic_of_death(
            bar, unit * n, unit * (n+1))
        persistence_feature = statistic_of_persistence(
            bar, unit * n, unit * (n+1))
        feature_matrix[n, :6] = death_feature
        feature_matrix[n, 6:12] = persistence_feature
    return feature_matrix


def distance(array1, array2):
    assert len(array1) == 3
    assert len(array2) == 3
    return np.linalg.norm(np.array(array1)-np.array(array2))


def get_distance_matrix(pro_atoms, lig_atoms):
    pro_num = len(pro_atoms)
    lig_num = len(lig_atoms)
    assert isinstance(pro_atoms, List)
    assert isinstance(lig_atoms, List)
    all_atoms = np.array(pro_atoms + lig_atoms)
    N = pro_num + lig_num
    dm = np.zeros((N, N))
    pro_inner_dist = 100
    lig_inner_dist = 100
    if pro_num != 0 and lig_num != 0:
        all_atoms = all_atoms[:, :3]
        assert all_atoms.shape[1] == 3
        for i in range(N):
            for j in range(N):
                if i < pro_num:  # pro atom lines
                    if j < pro_num:
                        dm[i, j] = pro_inner_dist
                    else:
                        atom_dist = distance(all_atoms[i], all_atoms[j])
                        dm[i, j] = atom_dist
                else:  # lig atom lines
                    if j >= pro_num:
                        dm[i, j] = lig_inner_dist
                    else:
                        atom_dist = distance(all_atoms[i], all_atoms[j])
                        dm[i, j] = atom_dist
        for i in range(N):
            dm[i, i] = 0
    else:
        pass
    return dm


def parse_pdbdata(pdb_file, pro_chain, lig_chain, save_barcode=False, cutoff=10, max_length=15, filtration=15.0, unit=0.5):

    save_path = os.getcwd()
    code = os.path.split(pdb_file)[-1].split('.')[0]
    logging.info(f'Start parse the file {pdb_file}...')
    data = parse_pdb(file=pdb_file)
    Protein_chain = pro_chain
    Ligand_chain = lig_chain

    # split data into protein_data and ligand_data
    cond = data.chain_ID.isin([Protein_chain])
    pro_data = data[cond]
    cond = pro_data.Atom_name.isin(Protein_Atom)
    pro_data = pro_data[cond]
    cond = pro_data.Res_name.isin(aa_list)
    pro_data = pro_data[cond]
    cond = (pro_data.Atom_hetfield == '')
    pro_data = pro_data[cond]
    pro_resnum = len(np.unique(pro_data.Res_num))
    # assert pro_resnum == pro_data.Res_num.max()
    cond = pro_data.Res_num.isin(sites)  # binding sites
    pro_data = pro_data[cond]
    pro_resnum = len(np.unique(pro_data.Res_num))
    if pro_resnum < 34:
        logging.warning(f'Not enough interface residues in HLA for {code}!')
        return

    cond = data.chain_ID.isin([Ligand_chain])
    lig_data = data[cond]
    cond = lig_data.Atom_name.isin(Ligand_Atom)
    lig_data = lig_data[cond]
    cond = (lig_data.Atom_hetfield == '')
    lig_data = lig_data[cond]

    protein = defaultdict(list)
    ligand = defaultdict(list)
    for tup in pro_data.itertuples():
        atom = tup.Atom_name
        if atom in Protein_Atom:
            protein[atom].append([tup.X, tup.Y, tup.Z])
    for tup in lig_data.itertuples():
        atom = tup.Atom_name
        if atom in Ligand_Atom:
            ligand[atom].append([tup.X, tup.Y, tup.Z])

    total_features = []
    for pro_atom in Protein_Atom:
        pro_atom_ls = protein[pro_atom]

        for lig_atom in Ligand_Atom:
            lig_atom_ls = ligand[lig_atom]
            # protein atom filtered by distance cutoff
            filtered_pro_atoms = []
            for proatom_coord in pro_atom_ls:
                for ligatom_coord in lig_atom_ls:
                    dist = distance(proatom_coord, ligatom_coord)
                    if dist <= cutoff:
                        filtered_pro_atoms.append(proatom_coord)
                        break

            # pro_num = len(protein[pro_atom])
            pro_num = len(filtered_pro_atoms)
            lig_num = len(lig_atom_ls)
            # if pro_num == 0:
            #     logging.warning(
            #         f'Protein has no {pro_atom} in {pro_atom}_{lig_atom} pair!')
            # if lig_num == 0:
            #     logging.warning(
            #         f'Ligand has no {lig_atom} in {pro_atom}_{lig_atom} pair!!')
            total_num = pro_num + lig_num

            all_atoms = np.zeros([total_num, 3])
            if pro_num:
                all_atoms[:pro_num, :] = np.array(filtered_pro_atoms)
            if lig_num:
                all_atoms[pro_num:, :] = np.array(lig_atom_ls)

            dm = get_distance_matrix(filtered_pro_atoms, lig_atom_ls)
            # atom Euclidean distance feature
            zero_bar = get_barcode(
                dm=dm, pro_num=pro_num, lig_num=lig_num, max_length=max_length)
            feature_matrix = get_static_feature(
                bar=zero_bar, filtration=filtration, unit=unit)
            if save_barcode:
                barfile = os.path.join(
                    save_path, f'{code}_{pro_atom}_{lig_atom}_zerobar.csv')
                np.savetxt(barfile, zero_bar, delimiter=',')

            pair_feature = np.array(feature_matrix).reshape(-1,)
            assert pair_feature.shape[0] == 360
            total_features.append(pair_feature)

    total_features = np.array(total_features)
    assert total_features.shape[0] == 16
    assert total_features.shape[1] == 360

    return total_features


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='A persistent homology method for pMHC interface structure feature generation', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input', help='Input file for structure feature generation', required=True)
    parser.add_argument(
        '-o', '--output', help='Output file for pshm results containing the 16×360 feature matrix')
    parser.add_argument('-l', '--length', default=15,
                        type=float, help='Max length for RipsComplex')
    parser.add_argument('-f', '--filtration', default=15, type=float,
                        help='Max length for filtration process, usually the same as RipsComplex max length')
    parser.add_argument('-u', '--unit', default=0.5, type=float,
                        help='Filtration unit (length for each filtration shell)')
    parser.add_argument('-c', '--cutoff', default=10, type=float,
                        help='HLA and peptide atom distance cutoff for HLA atoms filter')
    parser.add_argument('--protein', default='A',
                        help='HLA chain in the PDB file')
    parser.add_argument('--ligand', default='C',
                        help='Peptide chain in the PDB file')
    args = parser.parse_args()
    max_length = args.length
    filtration = args.filtration
    unit = args.unit
    cutoff = args.cutoff
    pro_chain = args.protein
    lig_chain = args.ligand
    features = parse_pdbdata(pdb_file=args.input, pro_chain=pro_chain, lig_chain=lig_chain,
                             cutoff=cutoff, max_length=max_length, filtration=filtration, unit=unit)

    np.savetxt(args.output, features, delimiter=',')
