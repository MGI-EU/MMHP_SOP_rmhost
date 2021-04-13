# MMHP - Standard Operating Procedure - Removing Host Sequence

The "remove-host" standard operating procedure in MMHP (The Million Microbiome of Humans Project). This repository is the standard pipeline for removing human genome sequence from metagenome data.

## Notification

Current version only supports [PBS job management](https://albertsk.files.wordpress.com/2011/12/pbs.pdf) (`qsub`, `qstat`) and Paired-end reads analyss.

## 1. Introduction

The pipeline in this repository is part of the Standard Operation Procedure (SOP) of MMHP. The function of this repository is metagenome raw data trimming and removing human genome sequence.

Project/Repository Structure:

- Main project: The Million Microbiome of Humans Project
- Sub-project: Standard Operating Procedure (SOP)
- Procedure: Removing Host (human) Sequence

The pipeline includes three main steps:

1. Quality control / Sequence filteration of raw metagenome fastq data.
2. Removing host sequence (human genome) from trimmed metagenome fastq data.
3. Profiling host-seq-removed reads.

The pipeline is extracted and modified from [ohmeta/metapi](https://github.com/ohmeta/metapi).

## 2. Requirements

PBS jobs management (`qsub`, `qstat`) with the help of [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management for current version.

### 2.1. Software (Tested version)

- Python: v3.6.13
  - Packages: [metaphlan](https://github.com/biobakery/MetaPhlAn): v3.0.7
  - Packages: snakemake: >=v6.0.0
- Perl: >=v5.26.2

- Softwares for data trimming:  
  - fastp: v0.20.1 (<https://github.com/OpenGene/fastp>)
  - ~~cutadapt: v3.3 (<https://cutadapt.readthedocs.io/en/stable/>)~~

- Software for removing host sequence:
  - bowtie2: >=v2.3.5.1 (<http://bowtie-bio.sourceforge.net/bowtie2/index.shtml>)
  - samtools: v1.11 (<https://github.com/samtools/samtools>)

- Software for report:
  - seqkit: v0.15.0

### 2.2. Database

- Human reference (for bowtie2 index):
  - [CHM13](https://github.com/nanopore-wgs-consortium/CHM13)
  - [Hg38](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.39/)
- MetaPhlAn3 index ([new version](https://github.com/biobakery/MetaPhlAn/wiki/MetaPhlAn-3.0)):
  - mpa_v30_CHOCOPhlAn_201901
  - [more db version](https://drive.google.com/drive/folders/1_HaY16mT7mZ_Z8JtesH8zCfG9ikWcLXG)

## 3. Installation

It's recommended to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to simplify the installation.

```shell
conda create -n mmhp_sop_rmhost python=3.6.13
conda activate mmhp_sop_rmhost
conda install -c bioconda bowtie2=2.3.5.1
conda install -c bioconda samtools=1.11
conda install -c bioconda seqkit fastp
# conda install -c bioconda cutadapt
pip3 install snakemake
pip3 install metaphlan
git clone https://github.com/MGI-EU/MMHP_SOP_rmhost.git
cd MMHP_SOP_rmhost
```

## 4. Usage

### 4.1. Database Preparation

For human genome reference:

```shell
#cd MMHP_SOP_rmhost
mkdir -p database/human_genome/
wget --continue -q https://s3.amazonaws.com/nanopore-human-wgs/chm13/assemblies/chm13.draft_v1.0.fasta.gz

########
## Users would better add chromosome Y from Hg38 to CHM13 reference because CHM13 doesn't contain chrY.
## For chrY, users could manually download Hg38.p13 chromosome Y sequence from https://www.ncbi.nlm.nih.gov/nuccore/CM000686.2?report=fasta 
## After downloading, change the chromosome name to ">chrY"
## Assume that the chrY sequence file has been named to hg38.chrY.fasta
########

gzip -dc chm13.draft_v1.0.fasta.gz > database/human_genome/human_reference.fasta
cat hg38.chrY.fasta >> database/human_genome/human_reference.fasta

#conda activate mmhp_sop_rmhost
bowtie2-build -f --threads 4 database/human_genome/human_reference.fasta database/human_genome/human_reference
```

For MetaPhlAn3.0 refernece:

```shell
########
## MetaPhlAn provides the function to automatically download and build reference
## We can choose the reference version through --index option.
########
mkdir -p database/metaphlan_database/
metaphlan --install --index mpa_v30_CHOCOPhlAn_201901 --bowtie2db ./database/metaphlan_database
```

### 4.2. Configuration Preparation

Please edit `sample.txt`, `config.yaml`, `cluster.yaml` files in `MMHP_SOP_rmhost` folder according to users' needs.

The most important parameters to edit:

- `sample.txt`: tab-delimited file path
- `config.yaml`:
  - `fastp`: adapter_r1, adapter_r2
  - `rmhost`: bowtie2_index
  - `metaphlan3`: bowtie2db, index 
- `cluster.yaml`:
  - `__default__`: queue, project
  - others: mem, cores

Note:

- `rmhost.bowtie2_index` should be the same as `bowtie2-build` output in human genome reference preparation step
- `metaphlan3.bowtie2db` should be the same as `--bowtie2db` in metaphlan reference preparation step
- `metaphlan3.index` should be the same as `--index` in metaphlan reference preparation step

### 4.3. Run

```shell
#conda activate mmhp_sop_rmhost

sh work.sh &>work.out &
```

## 5. Updates

April 12th, 2021

1. Create repository.
2. Only support PBS commands in this version.

## 6. Analysis Plan

### Todo

- assembled contigs test
- min_len test
- add more test details and results (1000 genome samples)
- rgi

### Complete

- cutadapt test
- fastp parameters test
- bowtie2 parameters test
- CHM13 and Hg38 reference test

## Reference

- <https://github.com/ohmeta/metapi>

## Acknowledgement

- Mathieu Almeida
- Liu Tian, BGI
- Bochen Cheng, MGI
- Jie Zhu, BGI

## License
