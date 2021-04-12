#############################################
### merge fq.gz
### tianliu@genomics.cn
### 2020-06-08
### 这一步还是加到自动识别的好，否则很麻烦。
#############################################

# python merge_multi_fq.py sample_dup.txt sample_dup_merge.txt

import sys
import os

if len(sys.argv) != 3:
    print("Usage: python rules/merge_multi_fq.py sample_dup.txt sample_dup_merge.txt")
    print("Sample with mulit_library will be merged into 1.assay/00.tmp")
    exit()
else:
    infile = sys.argv[1]
    outfile = sys.argv[2]

if not os.path.exists("1.assay/00.tmp"):
    os.system("mkdir -p 1.assay/00.tmp")
else:
    if len(os.listdir("1.assay/00.tmp")) > 0:
        print('Warning: "1.assay/00.tmp" is not null.')
        print("Please avoid files with the same name as the id in sample_dup.txt")

f_o = open(outfile, "w")
f_o.write("id\tfq1\tfq2\n")

path_set = set()
rmhost_done_n = 0
f_i = open(infile).readlines()

for i in f_i[1:]:
    sample, r1, r2 = i.strip().split("\t")
    merge_path = "%s\t1.assay/00.tmp/%s.1.fq.gz\t1.assay/00.tmp/%s.2.fq.gz\n" %(sample, sample, sample)
    path_set.add(merge_path)
    r1_rmhost = "1.assay/02.rmhost/%s.rmhost.1.fq.gz" %(sample)

    if os.path.exists(r1_rmhost):
        print("%s have rmhost reads, pass" %(sample))
        path_set.remove(merge_path)
        rmhost_done_n += 1
        continue
    else:
        os.system("cat %s >> 1.assay/00.tmp/%s.1.fq.gz" %(r1, sample))
        os.system("cat %s >> 1.assay/00.tmp/%s.2.fq.gz" %(r2, sample))

for path in path_set:
    f_o.write(path)
f_o.close()

print("merge %s records to %s samples" %(len(f_i[1:]) - rmhost_done_n, len(path_set)))
