import os
import subprocess

def split_file(root, filename):
    """This works similarly to Vina_Split."""
    os.chdir(root)
    if not os.path.exists(f'{root}/Ligand'):
        os.mkdir("Ligand")
        os.mkdir("Output")
        os.mkdir("ProcessedLigand")
        
    with open(filename, 'r') as larger_file:
        content = larger_file.read()
    # Reads entire file, saving it to a list, but splitting it around the keyword 'ENDMDL'
    file_parts = content.split("ENDMDL")
    if len(file_parts == 1): # i.e. a single ligand file
        # just move it into the Ligand directory
        subprocess.run(['mv',root+"/"+filename, root+"/Ligand/"+filename])
    else:
        del file_parts[-1] 
        #Removes the trailing empty line.
        file_name_start = filename[:-6]
        #Returns filename base
        # Save each part to a separate file
        for i, part in enumerate(file_parts):
            # Generate the filename for each part, with pdbqt extension at the end
            ligand_file_name = f'Ligand/{file_name_start}_{i+1}.pdbqt'
            if (i == 0):
                #For the first ligand, only return from the second line
                lines = part.splitlines()[1:]
            else:
                #For all other ligands, return from the third line
                lines = part.splitlines()[2:]
            with open(ligand_file_name, 'w') as smaller_file:
                smaller_file.write('\n'.join(lines))
                #Write each ligand to its own file.
        #    print(f'Saved {ligand_file_name}')
