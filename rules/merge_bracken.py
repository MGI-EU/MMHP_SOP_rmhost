### merge bracken profile
### tianliu@genomics.cn
### 2020-07-06

import sys
import pandas as pd
import os

if len(sys.argv) != 4:
    print('Usage: python merge_bracken.py bracken_dir bracken_suffix outfile')
else:
    bracken_dir = sys.argv[1]
    bracken_suff = sys.argv[2]
    outfile = sys.argv[3]

#bracken_dir = "test"
#bracken_suff = ".bracken.profile"
bk_file_lst = [bk_file for bk_file in os.listdir(bracken_dir) if bk_file.endswith(bracken_suff)]

df = pd.read_table(os.path.join(bracken_dir, bk_file_lst[0]))
file_id = bk_file_lst[0].replace(bracken_suff,'')

df = df[['name', 'new_est_reads']]
df.rename(columns = {'new_est_reads':file_id}, inplace = True)

for file in bk_file_lst[1:]:
    file_id = file.replace(bracken_suff, "")
    df_tmp = pd.read_table(os.path.join(bracken_dir, file))
    df_tmp = df_tmp[['name', 'new_est_reads']]
    df_tmp.rename(columns = {'new_est_reads':file_id}, inplace = True)
    df = pd.merge(df, df_tmp, how = 'outer')

df = df.fillna(0)
df.to_csv(outfile, sep = "\t", index = False)
