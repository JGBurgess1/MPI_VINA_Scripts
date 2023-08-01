import os

def split_file(root, filename):
    os.chdir(root)
    os.mkdir("Ligand")
    os.mkdir("Output")
    os.mkdir("ProcessedLigand")
    with open(filename, 'r') as larger_file:
        content = larger_file.read()

    # Split the content by the word "ENDMDL"
    file_parts = content.split("ENDMDL")
    del file_parts[-1] #Removes the trailing end
    #del file_parts[0] #Removes the first, MODEL line
    #file_parts = file_parts[2:]
        #Removes the first and last lines, which are tags for it to be a multi-ligand file.

    file_name_start = filename[:-6]
        #Get to filename without the .pdbqt extension   

    # Save each part to a separate file
    for i, part in enumerate(file_parts):
        # Generate the filename for each part, with pdbqt extension at the end
        ligand_file_name = f'Ligand/{file_name_start}_{i+1}.pdbqt'
        if (i == 0):
            lines = part.splitlines()[1:]
        else:
            lines = part.splitlines()[2:]
        with open(ligand_file_name, 'w') as smaller_file:
            smaller_file.write('\n'.join(lines))

        print(f'Saved {ligand_file_name}')

# this method works for a given directory, and will recursively iterate through all files in the directory, splitting them when possible.
def print_files(directory):
        for root, dirs, files in os.walk(directory):
                for file_path in files:
                        split_file(file_path, 'ENDMDL\n')

# Use the following for standalone execution, not when called from another script.
#def main():
# should now receive system arguments...
# sys arguments are of the form, python_script.py argument1 argument2 argument3 ...
# to access them, you use sys.argv[i], where i = 1 for the first argument, i = 2 for the second argument, etc...
#
#       if len(sys.argv) < 2: # if no arguments passed - only the script itself
#               print("Usage: python script.py argument1 argument2 argument3 ... ")
#       else:
#               file_arg = sys.argv[1] # the first argument passed, is the file here.
#               split_file(file_arg)
