import os

def process(directory):
    line2, line3 = "","" 
    new_file_line = ""
    os.chdir(directory)
    for file in os.listdir("Output/"):
        if file[-5:] == "pdbqt":
            for i, line in enumerate(file):
                print(line)
                if i == 0:
                    continue
                if i == 1:
                    line2 = line
                if i == 2:
                    line3 = line
                else:
                    break
# only record the values of the second and third line.
# then strip and split them, to get to the values of (a) in line 2, the Vina score, and (b) in line 3, the ZINC full ligand name.
# put them together with the filename beginning, onto a new line in the results.txt file.
            line4 = line2.strip().split()
            line5 = line3.strip().split()
            file_name = file[:-12] # gets the basename of the file. same as $(basename ${file} .pdbqt.pdbqt)
            print(line2, line3, file_name)
################ ERROR HERE IN LINE FOLLOWING - FIX WHEN POSSIBLE ##########################
            new_file_line = [file_name, line5[3], line4[3]] #### FIX THE ERROR - HERE. ARRAY OUT OF BOUNDS..... ######
            new_file_line = ",".join(new_file_line)
            with open("Output/results.txt", "a") as results_file:
                results_file.write(new_file_line + "\n")
            os.remove(file)
            os.remove(file[:-6]+".txt")
# remove the file and the summarized results file from the directory, leaving only the top score and name in the 'results.txt' file.
