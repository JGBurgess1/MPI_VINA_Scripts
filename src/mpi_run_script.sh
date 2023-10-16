#!/bin/bash

cd $1

cp -r /mnt/lustre/groups/CBBI1154/ZINC_20/W312G_ZINC/VINA_Scripts/Vina ./

NP=$(cat ${PBS_NODEFILE} | wc -l )

ls > ligandlist ./Ligand
mpirun --mca btl '^openib' -np $NP --machinefile $PBS_NODEFILE mpiVINA

### Then back to script n_main once finished with the MPI_RUN.


