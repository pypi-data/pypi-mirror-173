import sys
import os.path as osp
import mdtraj as md
import os
import logging
import argparse
from subprocess import run

tri2single = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C', 'Gln': 'Q', 'Glu': 'E', 'Gly': 'G', 'His': 'H', 'Ile': 'I',
              'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V'}
DEFAULT_DIR = osp.dirname(osp.realpath(__file__))
WORK_DIR = os.getcwd()
APE_LOCATION = osp.join(DEFAULT_DIR, 'APE-Gen')
ROSETTA_LOCATION = osp.join(DEFAULT_DIR, 'mhc-pep-threader')
template_dic = {}
with open(osp.join(DEFAULT_DIR, 'templates.txt')) as f:
    for line in f:
        ls = line.split()
        template_dic[ls[0]] = ls[1]
with open(osp.join(DEFAULT_DIR, 'supported_alleles.txt')) as f:
    supported_hlas = f.read().splitlines()


parser = argparse.ArgumentParser(
    description="Peptide-MHC complex structure Generator", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--software', default='APE-Gen', choices=[
                    'APE-Gen', 'RosettaMHC'], help="Software used for pMHC structure generation, defaults to 'APE-Gen'")
parser.add_argument('peptide_input', type=str,
                    nargs=1, help='Sequence of peptide')
parser.add_argument('receptor_class', type=str,
                    nargs=1, help='MHC class I allele')
parser.add_argument('--output_dir', type=str, default='structures',
                    help="Output PDB file saved path")
parser.add_argument('--filename', type=str, default='pmhc001',
                    help="Saved PDB file name,e.g.,default='pmhc001', and the output file will be like 'pmhc001.pdb'")
parser.add_argument('--list_supported_hlas', action='store_true',
                    help="List all the supported 110 HLA alleles")

rosetta_args = parser.add_argument_group(title="RosettaMHC simple arguments")
rosetta_args.add_argument(
    "--template_pdb", help="Provide template structure in PDB to perform threading")
rosetta_args.add_argument("--mhc_chain", type=str, default='A',
                          help="HLA chain in the template PDB file")
rosetta_args.add_argument("--peptide_chain", type=str, default='C',
                          help="Peptide chain in the template PDB file")


def check_hlas(hlas):
    for hla in hlas:
        if hla not in supported_hlas:
            raise (ValueError(
                f"Unrecognized hla {hla} for SETTMHC, use '--list_supported_hlas' for more details"))


def run_APE(peptide, hla, outputdir, filename):
    cmd = f"python {APE_LOCATION}/APE_Gen.py {peptide} {hla} --output_dir {outputdir} --filename {filename} --no_progress"
    run(cmd, shell=True)


def run_RosettaMHC(peptide, hla, outputdir, filename, template_pdb, mhc_chain='A', pep_chain='C'):
    with open('./pep_list', 'w') as f:
        f.write(f'>{filename}' + '\n' + peptide + '\n')
    with open('./mhc_list', 'w') as f:
        f.write(hla.split('HLA-')[-1] + '\n')
    template_name = osp.split(template_pdb)[-1].split('.')[0]
    cmd = f"python {ROSETTA_LOCATION}/main.py -relax_after_threading -template_pdb {template_pdb} -mhcs mhc_list -peptides pep_list \
        -mhc_chain {mhc_chain} -peptide_chain {pep_chain} -pep_start_index 181 -interface_cutpoint 180"
    run(cmd, shell=True)
    hla_header = hla.split('HLA-')[-1]
    rosetta_output = f'{hla_header}_none_{filename}_none_none_on_{template_name}.pdb'
    run(f"cp {rosetta_output} {outputdir}/{filename}.pdb", shell=True)


def check_structure(file, true_pep, is_ape=True):
    is_passed = True
    pdb = md.load_pdb(file)
    top = pdb.topology
    table, _ = top.to_dataframe()
    if is_ape:
        pep_sele = top.select('chainid 2')
    else:
        pep_sele = top.select(f'resid 180 to 200')
    table2 = table.loc[pep_sele]
    pep_table = table2.drop_duplicates('resSeq')
    pep_names = pep_table['resName']
    ls = []
    for aa in pep_names:
        aa_one = tri2single.get(aa.capitalize(), 'X')
        ls.append(aa_one)
    pdb_pep = ''.join(ls)
    if pdb_pep != true_pep:
        is_passed = False
    return is_passed


def structure_generator(argv=sys.argv[1:]):
    args = parser.parse_args(argv)
    if args.list_supported_hlas:
        print(supported_hlas)
        return
    check_hlas(hlas=[args.receptor_class])

    software = args.software
    outputdir = args.output_dir
    outputdir = osp.realpath(outputdir)
    filename = args.filename
    output_file = osp.join(outputdir, f'{filename}.pdb')
    peptide = args.peptide_input[0]
    hla = args.receptor_class[0]
    if not osp.exists(outputdir):
        os.mkdir(outputdir)
    if software == 'APE-Gen':
        ape_dir = 'ape_workdir'
        ape_dir = osp.realpath(ape_dir)
        if not osp.exists(ape_dir):
            os.mkdir(ape_dir)
        os.chdir(ape_dir)
        run_APE(peptide, hla, outputdir, filename)
        is_passed = check_structure(output_file, peptide, is_ape=True)
    elif software == 'RosettaMHC':
        template_pdb = osp.realpath(args.template_pdb)
        rosetta_dir = 'rosetta_workdir'
        rosetta_dir = osp.realpath(rosetta_dir)
        if not osp.exists(rosetta_dir):
            os.mkdir(rosetta_dir)
        os.chdir(rosetta_dir)
        run_RosettaMHC(peptide, hla, outputdir, filename,
                       template_pdb, args.mhc_chain, args.peptide_chain)
        is_passed = check_structure(output_file, peptide, is_ape=False)
    if not is_passed:
        print(f"Check for {peptide}_{hla} complex failed")


def make_structure(peptide, hla, anno, structure_dir=None):
    if structure_dir is None:
        structure_dir = 'structures'
    structure_dir = osp.realpath(structure_dir)
    if not osp.exists(structure_dir):
        os.mkdir(structure_dir)
    rosetta_dir = 'rosetta_workdir'
    rosetta_dir = osp.realpath(rosetta_dir)
    if not osp.exists(rosetta_dir):
        os.mkdir(rosetta_dir)
    ape_dir = 'ape_workdir'
    ape_dir = osp.realpath(ape_dir)
    if not osp.exists(ape_dir):
        os.mkdir(ape_dir)

    is_passed = False
    # run APE-Gen
    output_file = osp.join(structure_dir, f'{anno}.pdb')
    os.chdir(ape_dir)
    run_APE(peptide, hla, structure_dir, anno)
    if osp.exists(output_file):
        is_passed = check_structure(output_file, peptide, is_ape=True)
    if not is_passed or not osp.exists(output_file):
        # run RosettaMHC
        os.chdir(rosetta_dir)
        template_pdb = template_dic[hla]
        template_pdb_file = osp.join(APE_LOCATION, f'templates/{template_pdb}')
        run_RosettaMHC(peptide, hla, structure_dir, anno, template_pdb_file)
        is_passed = check_structure(output_file, peptide, is_ape=False)
        if not is_passed:
            logging.error(
                f"Generation for {peptide}_{hla} pMHC structure failed! This pair will show scores '0' in the results")
            run(f"rm {structure_dir}/{anno}.pdb", shell=True)

    os.chdir(WORK_DIR)
    if is_passed:
        return output_file
