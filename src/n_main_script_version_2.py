import os
import subprocess
import gzip
import shutil
import n_split_files as nsf
import n_process_results as npr

# declared variables

ZINC_DIRECTORY = "/mnt/lustre/groups/CBBI1154/ZINC_20/ZINC_DB/"
SRC_DIRECTORY = "/mnt/lustre/groups/CBBI1154/ZINC_20/W312G_ZINC/VINA_Scripts/src"

def main():
    
    for root, dirs, files in os.walk(ZINC_DIRECTORY):
        #At the beginning of each batch:
        if os.path.exists(root + "/DONE.txt"):
            continue
        # checking in a moment. ^^^^

        ###### \/ \/ \/ \/

        for file in files:
            # Check if the ligand file is gzipped.
            if file[-8:]=="pdbqt.gz":
                # Then unzip it
                unzip(root, file) 
                split(root, file[:-3])
            elif file[-5:]=="pdbqt":
                split(root, file)
            # should now just skip the file if it doesn't have a pdbqt extension.
            else:
                continue
            # Then process each ligand file using the MPI-VINA script.
            MPI_Vina(root)
            getScores(root)
            sortScores(root)
            file_path = root + "/" + file
            file_path_done = root + "/" + file + "DONE"
            subprocess.run(['mv',file_path,file_path_done])

        #At the end of the batch:
        #Remove all tag files, then create a DONE tag file.
        #subprocess.run(["rm", root + "/STARTED.txt", root + "/SPLIT.txt", root + "/MPI_STEP.txt", root + "/RESULTS_PROCESSED.txt", root + "/RESULTS_SORTED.txt"])

        doneFilePath = root + "/DONE.txt"
        subprocess.run(['touch',doneFilePath])

def unzip(root, file):
    subprocess.run(['gunzip', root+"/"+file])

def split(root, file):
    nsf.split_file(root, file)

def MPI_Vina(root):
    try:
        subprocess.run(['bash',SRC_DIRECTORY+'/mpi_run_script.sh',root], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

def getScores(root):
    npr.process(root)

def sortScores(root, file):
    try:
        result2 = subprocess.run(['bash',SRC_DIRECTORY+'/sort_script.sh',root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

main()        


