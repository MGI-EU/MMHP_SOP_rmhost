import os
import sys

sample_file = sys.argv[1]
exist_file = sample_file + ".exist"
no_file = sample_file + ".noexist"

f_o = open(exist_file, "w")
f_o2 = open(no_file, "w")

for i in open(sample_file).readlines()[1:]:
    id,fq1,fq2 = i.strip().split("\t")
    if os.path.exists(fq1) and os.path.exists(fq2):
        f_o.write(i)
    else:
        f_o2.write(i)

f_o.close()
f_o2.close()
