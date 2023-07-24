# Startup Script to initialise files for mpi-vina run, starting from an unzipped ligand file.
# Assumes you have a config file, and receptor file, for running the job.

#
# 1. THIS IS A LONG SCRIPT, I WILL TRY TO MAKE IT CLEARER IN THE COMMENTS
#


module load chpc/autodock_vina/1.1.2/gcc-6.1.0
module load chpc/autodock/mpi-vina/openmpi-4.0.0/gcc-7.3.0

#
# 2. THIS PART CREATES THE DIRECTORY STRUCTURE IN THE TARGET FOLDER WHICH MPI-VINA NEEDS
#

mkdir Output Ligand Vina ProcessedLigand

NP=$(cat ${PBS_NODEFILE} | wc -l )

if [ $NP -eq 240 ]; then
     $NP=120
fi

cp -r /mnt/lustre/users/jburgess1/template_folder/Vina ./

#
# 3. THIS PART FINDS ALL PDBQT FILES. 
#    FOR FILES WITH A SINGLE LIGAND, IT PROCESSES THEM SEPARATELY FROM FILES WITH MULTIPLE LIGANDS
#    FOR MULTI-LIGAND FILES, IT USES VINA-SPLIT TO SPLIT FILES INTO INDIVIDUAL LIGAND FILES
#    IT GENERATES A LIST OF THE INDIVIDUAL LIGAND FILES AND SUBMITS THIS TO MPI-VINA.  
#    MPI-VINA RUNS USING ALL AVAILABLE CORES. LIGANDS PROCESSED ARE THEN MOVED TO THE 'PROCESSED_LIGANDS' 
#    FOLDER. THE VINA OUTPUT LIGAND CO-ORDINATES AND SUMMARY SCORES ARE DEPOSITED IN THE FOLDER 
#    'OUTPUT/' FOLDER. EACH LIGAND'S TOP BINDING SCORE IS SAVED TO A FILE CALLED 'RESULT'.
#    THIS RESULT FILE IS SORTED NUMERICALLY, AND SAVED AS 'SORTEDRESULT' WHICH SHOWS THE TOP SCORING LIGANDS.
#

for file in ./*.pdbqt;
do
	if ! grep -q "MODEL" $file; then     ### SINGLE-LIGAND FILES DO NOT HAVE 'MODEL' OR 'ENDMDL' KEYWORDS IN THEM [THEY ONLY EXIST IN MULTI-LIGAND PDBQT FILES]
		mv $file /Ligand/
		echo $file > ligandlist

		mpirun -np 2 mpiVINA>Output/MpiVina_$(basename ${file} .pdbqt).log	

	else
		vina_split --input ${file} --ligand ./Ligand/$(basename ${file} .pdbqt)
		# stores all split ligand files in the Ligands/ directory
		ls > ligandlist ./Ligand
		echo "there are:  $(wc -l ligandlist) ligands in this directory"

		mpirun -np $NP mpiVINA>Output/MpiVina_$(basename ${file} .pdbqt).log
	fi
done

#
# 4. NOW STORE THE RESULTS OF THE VINA DOCKING IN A SINGLE FILE, AND SORT IT NUMERICALLY, FROM HIGHEST TO LOWEST SCORES.
#

cd Output/
grep "  1 " *.txt | cut -c1-15,35-42 > result
sort -n +1 -2 result -o SortedResult

