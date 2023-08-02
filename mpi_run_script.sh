#!/bin/bash
# include parent directory as argument 1

module load chpc/autodock_vina/1.1.2/gcc-6.1.0
module load chpc/autodock/mpi-vina/openmpi-4.0.0/gcc-7.3.0
module unload chpc/openmpi/4.0.0/gcc-7.3.0
module load chpc/openmpi/4.1.1/gcc-7.3.0

cd $1

mkdir Vina
cp -r /mnt/lustre/users/jburgess1/template_folder/Vina/* ./Vina/

NP=$(cat ${PBS_NODEFILE} | wc -l )

ls > ligandlist ./Ligand
mpirun --mca btl '^openib' -np $NP --machinefile $PBS_NODEFILE mpiVINA

#cd ../ProcessedLigand/
#rm *


