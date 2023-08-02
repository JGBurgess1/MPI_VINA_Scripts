import os

def split_file(root, filename):
    """This works similarly to Vina_Split. 
       Need to include the ability to process single files as well, however. [later date]."""
    os.chdir(root)
    os.mkdir("Ligand")
    os.mkdir("Output")
    os.mkdir("ProcessedLigand")
    with open(filename, 'r') as larger_file:
        content = larger_file.read()
    # Reads entire file, saving it to a list, but splitting it around the keyword 'ENDMDL'
    file_parts = content.split("ENDMDL")
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
        print(f'Saved {ligand_file_name}')