# VINA_Scripts
Python scripts─ for use of mpiVina and the ZINC20 database.

Requirements:
<br>(1) You have downloaded the zipped pdbqt files from the ZINC20 database.

Steps:
<br>(1) Copy the 7 files from this directory to your main ZINC20 Database directory.
<br>(2) Go to n_main_script.py, and edit the line
<br>
<br>10 input_directory = "path to main ZINC directory"
<br>
<br>to include your own ZINC directory.

(3) Create a template folder with the structure:
<br> - conf.txt           (your vina config file, with receptor and grid co-ordinates and sizes)
<br> - receptor.pdbqt     (your receptor file, ready for docking)
<br> - vina.exe           (the vina executable file, found in the main github directory)

(4)
