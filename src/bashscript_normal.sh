#!/bin/bash
#PBS -l select=10:ncpus=24:mpiprocs=24
#PBS -P CBBI1154
#PBS -q normal
#PBS -l walltime=4:00:00
#PBS -o /mnt/lustre/users/jburgess1/stdOut
#PBS -e /mnt/lustre/users/jburgess1/stdErr
#PBS -m abe
#PBS -N 16_Oct_smp_1_4hours
#PBS -M jeremygburgess@gmail.com

module load chpc/python/3.7.0/

cd /mnt/lustre/groups/CBBI1154/ZINC_20/W312G_ZINC/VINA_Scripts/src/

python3.7 n_main_script_version_2.py

#sh sort_script.sh /mnt/lustre/users/jburgess1/ZINC_DB_Test/AA/AAML
