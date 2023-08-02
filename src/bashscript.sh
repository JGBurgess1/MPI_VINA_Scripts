#!/bin/bash
#PBS -l select=25:ncpus=24:mpiprocs=24
#PBS -P CBBI1154
#PBS -q large
#PBS -l walltime=24:00:00
#PBS -o /mnt/lustre/users/jburgess1/02082023_2050.out
#PBS -e /mnt/lustre/users/jburgess1/02082023_2050.err
#PBS -m abe
#PBS -M jeremygburgess@gmail.com

module load chpc/python/3.7.0/

cd /mnt/lustre/users/jburgess1/ZINC_DB_Test/

python3.7 n_main_script.py

#sh sort_script.sh /mnt/lustre/users/jburgess1/ZINC_DB_Test/AA/AAML
