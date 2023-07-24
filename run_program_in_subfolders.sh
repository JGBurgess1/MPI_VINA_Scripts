#!/bin/bash

#
# 1. THIS PART TAKES EACH SUBFOLDER AS AN ARGUMENT, AND SENDS IT TO THE SCRIPT WHICH RUNS MPI_VINA IN THAT DIRECTORY
#

process_subfolder() {
# RECEIVE SUBFOLDER AS ARGUMENT 1    
local subfolder="$1"

cd "$subfolder"

cp ~/lustre/template_folder/mpi_vina_script_ZINCDB.sh .

# add 'busy' tag

add_tag_busy $subfolder

sh mpi_vina_script_ZINCDB.sh

add_tag_complete $subfolder 

cd $parent_directory
}

#
# 2. THIS PART ADDS TAGS TO EACH SUBFOLDER SUPPLIED AS AN ARGUMENT
#
add_tag_busy(){

local subfolder="$1"

if [ $PWD!=$subfolder ]; then
	cd $subfolder
fi

touch BUSY.txt
}

#
# 3. THIS PART ADDS TAGS TO SAY COMPLETE
#
add_tag_complete(){

local subfolder="$1"

if [ $PWD!=$subfolder ]; then
	cd $subfolder
fi

if [ -e $subfolder/BUSY.txt ]; then
	rm $subfolder/BUSY.txt
fi

touch COMPLETE.txt
}

#
# 4. THIS PART CHECKS IF FOLDER BUSY 
#
check_busy(){

local subfolder="$1"

if [ $PWD!=$subfolder ]; then
        cd $subfolder
fi

# IF 'BUSY.txt' EXISTS THEN RETURN TRUE
if [ -e "$subfolder/BUSY.txt" ]; then
	return 1
elif [ ! -e "$subfolder/BUSY.txt" ]; then
	return 0
fi

}

#
# 5. THIS PART CHECKS IF FOLDER IS COMPLETE
#
check_complete(){
local subfolder="$1"

if [ $PWD!=$subfolder ]; then
	cd $subfolder
fi

# IF COMPLETE.TXT EXISTS, RETURN TRUE
if [ -e "$subfolder/COMPLETE.txt" ]; then
	return 1
elif [ ! -e "$subfolder/COMPLETE.txt" ]; then
	return 0
fi

}

#
# 6. THIS PART REMOVES THE BUSY TAG
#
remove_tag_busy(){
local subfolder="$1"

if [ $PWD!=$subfolder ]; then
	cd $subfolder
fi

if [ -e "$subfolder/BUSY.txt" ]; then
	rm $subfolder/BUSY.txt
else 
	echo "There is no BUSY.txt file in the directory ${subfolder}"
fi
}

#
# 7. THIS PART REMOVES THE COMPLETE TAG
#
remove_tag_complete(){
local subfolder="$1"

if [ $PWD!="$subfolder" ]; then
	cd $subfolder
fi

if [ -e "$subfolder/COMPLETE.txt" ]; then
	rm $subfolder/COMPLETE.txt
else
	echo "There is no COMPLETE.txt file in the directory ${subfolder}"
fi
}

#
# 8. THIS PART LOOPS THROUGH EACH DIRECTORY IN THE MAIN DIRECTORY AND ONLY GIVES BACK THE 2ND LEVEL DIRECTORIES
#

# CHOOSE PARENT DIRECTORY
parent_directory="/mnt/lustre/users/jburgess1/ZINC_DB"

# LIST SUBFOLDERS IN DIRECTORY
subfolders=$(find "$parent_directory" -maxdepth 2 -mindepth 2 -type d)
 
for subfolder in $subfolders; do
	
	check_busy $subfolder
	busy=$?
	
	check_complete $subfolder
	complete=$?

        if [ $busy -eq 1 ]; then
		continue
	else
		if [ $complete -eq 1 ]; then
			continue
	
		else
			
			process_subfolder "$subfolder"
		fi
	fi
done

