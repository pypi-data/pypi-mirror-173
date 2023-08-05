# SETTMHC
SETTMHC is a peptide-MHC class I binding predictor software based on multimodal sequence-structure information.

SETTMHC also includes other two modules: pMHC complex structure mdeling and a persistent homology method to analysis pMHC complex surface topology features as structure representations.


# Installation

## System
Linux

## One-step installation
Befor using the `environment.yaml`, make sure the [Pyrosetta](https://www.pyrosetta.org/downloads/) download channel is modified in the file.

Using conda, just run `conda env create -n SETTMHC -f environment.yaml`, but it may cause some dependencies issues.

## Build step by step
Due to the two structure modeling methods, the environment build may be cumbersome.

python > 3.7

### 1. Requirements for **APE-Gen**

#### 1.1 Conda packages
- `conda install -c bioconda smina`
- `conda install -c omnia pdbfixer`
- `conda install -c conda-forge mdtraj`
- `conda install -c schrodinger pymol` or `conda install -c conda-forge pymol-open-source`
- `conda install -c bioconda autodock-vina`
- `conda install -c conda-forge openmm=7.5.1`

1.2 Install RCD
- Download RCD v1.4 from https://chaconlab.org/modeling/rcd/rcd-download
- Add `xxxx/RCD_v1.40_Linux_20190228/bin` to PATH to make 'rcd' command available
- Make sure the lib path containing 'libmkl_intel_lp64.so' is added to LD_LIBRARY_PATH, you may get the lib path by `find /home -name libmkl_intel_lp64.so`. If there is no such object, run `conda install -c intel mkl` and add the lib path to LD_LIBRARY_PATH.


### 2. Requirements for **RosettaMHC**
- Download [Pyrosetta](https://www.pyrosetta.org/downloads/)
- `conda install biopython`
- Download [Clustal omega](http://www.clustal.org/omega/) and add it to PATH

### 3. Install SETTMHC from pip
Before install settmhc, you may install **pytorch 1.9.0** (cpu only or with cuda) manually depending on your device.
```
pip install settmhc
```

# Usage
## SETTMHC binding prediction for pMHC
Download the model files first, defaluts to `~/.local/share/settmhc/`, or you can add `export SETTMHC_MODEL_DIR="path you like"` to your `~/.bashrc` beforehand.
```
settmhc --download
```

You can run prediction with peptides and hlas input:
```
settmhc --peptides KELEGILLL ALLGLTLGV --hlas HLA-A*02:01 HLA-A*11:01 -o output.csv
```

Or just input a csv file contains HLA and peptides, for more details in input.csv, see demo/demo.csv, which **Annotation** column is optional.
```
settmhc -i input.csv -o output.csv
```

Or specify a pMHC complex PDB file 
```
settmhc -pdb 1DUZ.pdb --protein A --peptide C
```

See `settmhc -h` for more argument information.


## pMHC complex structre modeling
```
usage: pmhc-model [-h] [--software {APE-Gen,RosettaMHC}] [--output_dir OUTPUT_DIR] [--filename FILENAME]
                  [--list_supported_hlas] [--template_pdb TEMPLATE_PDB] [--mhc_chain MHC_CHAIN]
                  [--peptide_chain PEPTIDE_CHAIN]
                  peptide_input receptor_class

Peptide-MHC complex structure Generator

positional arguments:
  peptide_input         Sequence of peptide
  receptor_class        MHC class I allele

optional arguments:
  -h, --help            show this help message and exit
  --software {APE-Gen,RosettaMHC}
                        Software used for pMHC structure generation, defaults to 'APE-Gen' (default: APE-Gen)
  --output_dir OUTPUT_DIR
                        Output PDB file saved path (default: structures)
  --filename FILENAME   Saved PDB file name,e.g.,default='pmhc001', and the output file will be like 'pmhc001.pdb'
                        (default: pmhc001)
  --list_supported_hlas
                        List all the supported 110 HLA alleles (default: False)

RosettaMHC simple arguments:
  --template_pdb TEMPLATE_PDB
                        Provide template structure in PDB to perform threading (default: None)
  --mhc_chain MHC_CHAIN
                        HLA chain in the template PDB file (default: A)
  --peptide_chain PEPTIDE_CHAIN
                        Peptide chain in the template PDB file (default: C)
```
To model pMHC structure, only input one pair of peptide and HLA allele at a time.
```
pmhc-model KELEGILLL HLA-A*02:01 
```

## Persistent homology method for structure analysis
```
usage: pshm [-h] -i INPUT [-o OUTPUT] [-l LENGTH] [-f FILTRATION] [-u UNIT] [-c CUTOFF] [--protein PROTEIN]
            [--ligand LIGAND]

A persistent homology method for pMHC interface structure feature generation

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file for structure feature generation (default: None)
  -o OUTPUT, --output OUTPUT
                        Output file for pshm results containing the 16×360 feature matrix (default: None)
  -l LENGTH, --length LENGTH
                        Max length for RipsComplex (default: 15)
  -f FILTRATION, --filtration FILTRATION
                        Max length for filtration process, usually the same as RipsComplex max length (default: 15)
  -u UNIT, --unit UNIT  Filtration unit (length for each filtration shell) (default: 0.5)
  -c CUTOFF, --cutoff CUTOFF
                        HLA and peptide atom distance cutoff for HLA atoms filter (default: 10)
  --protein PROTEIN     HLA chain in the PDB file (default: A)
  --ligand LIGAND       Peptide chain in the PDB file (default: C)
```
The default arguments for RipsComplex building are used for SETTMHC training.
```
pshm -i 1DUZ.pdb -o 1duz_features.csv --protein A --ligand -C
```

# Potential issues
An error may occur during the application `AttributeError: module 'distutils' has no attribute 'version'` due to the high version of setuptools.

You can fix this by `pip install setuptools==59.5.0`