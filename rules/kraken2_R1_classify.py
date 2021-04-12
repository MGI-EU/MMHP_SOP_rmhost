### kraken2 R1 classify
### tianliu@genomics.cn
### 2020-07-13

import argparse
import sys
import os

parser = argparse.ArgumentParser( 
    prog = "kraken2_R1_classify.py",
    description = "merge kraken2 report",
    usage = "kraken2_R1_classify.py *.kk2.report > kraken2_R1.report.txt")

parser.add_argument( 
    "infiles", 
    metavar = "input.txt", 
    nargs = "+", 
    help = "One or more kraken2 report to join" )


def merge(infile_lst):
    R1_lst = ["unclassified", "Bacteria", "Fungi", "Unclassified_Eukaryota", "Archaea", "Metazoa", "Viruses"]
    print("sample\tratio\tall_reads\tmapped_reads\trank\tNCBI_ID\tclassified")
    for f in infile_lst:
        sample_id = os.path.split(os.path.basename(f))[1].replace('.kreport','')
        with open(f) as f_i:
            for rec in f_i:
                item = rec.strip().split()
                if item[-1] in R1_lst:
                    print("%s\t%s" %(sample_id, "\t".join(item)))

def _main():
    args = parser.parse_args()
    merge(args.infiles)

if __name__ == "__main__":
    _main()