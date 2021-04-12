if [ ! -d 1.assay/cluster_logs ];then mkdir -p 1.assay/cluster_logs;fi

snakemake \
--snakefile rules/profile.smk \
--configfile config.yaml \
--cluster-config cluster.yaml \
--jobs 100 \
--keep-going \
--rerun-incomplete \
--latency-wait 360 \
--cluster "qsub -S /bin/bash -cwd -q {cluster.queue} -P {cluster.project} -l vf={cluster.mem},p={cluster.cores} -binding linear:{cluster.cores} -o {cluster.output} -e {cluster.error}"
