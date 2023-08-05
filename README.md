# VINA_Scripts
Python scripts─ for use of mpiVina and the ZINC20 database.

Requirements:
<br>(1) You have downloaded the zipped pdbqt files from the ZINC20 database.

Steps:
<br>(1) Copy the 6 files from the src directory to your main ZINC20 Database directory.
<br>(2) Go to n_main_script.py, and edit the line
<br>
<br>10 input_directory = "path to main ZINC directory"
<br>
<br>to your own ZINC directory path.

(3) Copy the Vina folder also to your main ZINC directory.
<br> edit the conf file with your own vina configuration file parameters.
<br> replace the 'QcAB.pdbqt' file with your own receptor file.
<br> - conf.txt           (your vina config file, with receptor and grid co-ordinates and sizes)
<br> - receptor.pdbqt     (your receptor file, ready for docking)
<br> - vina.exe           (the vina executable file)

(4) Go to the file mpi_run_script.sh
<br> go to the line
<br> 12 cp -r /mnt/.../Vina/* ./Vina/
<br> and change the Vina folder path to the path of your own Vina folder, described in (3).

(5) modify the file 'bash_script.sh' to your own PBS job scheduling commands, and
<br> change the cd "path to main ZINC directory" line to your own ZINC main directory
<br> try a short walltime initially, to make sure the file works as expected.
<br> once you are happy with the results, increase the walltime e.g. to 48hours for normal queue, or 96 hours for large queue.

Bugs - 
stopped after a single 100 000 file, now it continues.
Aware of one issue (5 Aug) that after almost 300 000 files it also stops processing, but will check later with the output/error logs.
