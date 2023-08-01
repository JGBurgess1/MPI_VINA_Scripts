import os
import subprocess
import gzip
import shutil
import n_split_files as nsf
import n_process_results as npr

def main():
    #input_directory = sys.argv[1]
    input_directory = "/mnt/lustre/users/jburgess1/ZINC_DB_Test"
    root_dir = "/mnt/lustre/users/jburgess1/ZINC_DB_Test/AA/AAML"
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file[-8:]=="pdbqt.gz":
                with gzip.open(root+"/"+file, 'rb') as f_in:
                    with open(root+"/"+file[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                #print(file)
                nsf.split_file(root, file[:-3])
                try:
                    result = subprocess.run(['bash',input_directory+'/mpi_run_script_long.sh',root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(e.stderr)
                #npr.process(root)
		# for when we want to improve the way that the results are tallied, we can use our own python method/
                #exit()
		# for when you want to do debugging, use the exit() to stop after one iteration of the loop
            else:
                continue
main()        


