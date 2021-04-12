# merge samples to one kraken2 work shell
# tianliu@genomics.cn
# 2020-05-29
# big memery cluster: -P st_supermem -q st_supermem.q 
# python rules/kraken2_merge.py 0.data/YAK_stools_s50.txt /hwfssz1/ST_META/EE/bin/database/theOneIndexForAll 0.0 1.assay/YAK 8 400 st_supermem st_supermem.q

import sys
import subprocess
import os

if len(sys.argv) != 9:
    print("USAGE")
    print("python kraken2_merge.py sample_lst kraken2_db confidence outdir threads memory(GB) project_ID queue_id")
    print("eg: python kraken2_merge.py sample.txt minikraken_db_8G 0.0 result 8 400 st_supermem st_supermem.q")
    exit()
else:
    sample_lst, kraken2_db, confidence, outdir, cpu, mem, project_id, queue = sys.argv[1:]

if not os.path.exists(outdir):
    os.makedirs(outdir)

### merge
kraken2_sh = os.path.join(outdir, "kraken2_work.sh")

f_o = open(kraken2_sh, "w")

for rec in open(sample_lst):
    ID,r1,r2 = rec.strip().split("\t")
    wk_sh = "kraken2 --paired --use-names --db %s --threads %s --confidence %s --output /dev/null --report %s/%s.kreport %s %s\n" \
    %(kraken2_db, cpu, confidence, outdir, ID, r1, r2)
    f_o.write(wk_sh)

f_o.close()

### qsub
qsub_sh = "qsub -cwd -l vf=%sg,num_proc=%s -P %s -binding linear:%s -q %s -o kraken2.sh.o -e kraken2.sh.e %s" %(mem, cpu, project_id, cpu, queue, kraken2_sh)
try:
    #out_bytes = subprocess.check_output(qsub_sh, shell = True)
    print(qsub_sh)
    print("qsub kraken2_work.sh to cluster")
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    code      = e.returncode   # Return code
    print("error, work closed.")

print("kraken2 finished.")
