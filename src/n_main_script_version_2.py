import os
import subprocess
import gzip
import shutil
import n_split_files as nsf
import n_process_results as npr

#### gmail app attempt################################################################################################################

import smtplib
from email.mime.text import MIMEText

subject = "Results"
body = "Email sent from the program when the MPI is complete."
sender = "jeremygburgess@gmail.com"
recipients = "jeremygburgess@gmail.com"
password = "dhzi cupg lbau cysj"

######################################################################################################################################

# declared variables

ZINC_DIRECTORY = "/mnt/lustre/groups/CBBI1154/ZINC_20/ZINC_DB/"
SRC_DIRECTORY = "/mnt/lustre/groups/CBBI1154/ZINC_20/W312G_ZINC/VINA_Scripts/src"

def main():

    for root, dirs, files in os.walk(ZINC_DIRECTORY):
        #At the beginning of each batch:
        if os.path.exists(root + "/DONE.txt"):
            continue
        if os.path.exists(root + "/STARTED.txt"):
##### ########
##### ########  PUT CODE here - what to do if it _is_ busy, but not sure whether the directory is being actively worked on or not.
##### ########
            continue
            
            if not os.path.exists(root + "/SPLIT.txt"):
                pass
        elif not os.path.exists(root + "/STARTED.txt"):
            subprocess.run(["touch", root + "/STARTED.txt"])

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
            
            # Then process each ligand file using the MPI-VINA script.
            MPI_Vina(root)
            getScores(root)
            # send scores to me by email??

            subprocess.run(['touch', root + "/RESULTS_PROCESSED.txt"])
            try:
                result2 = subprocess.run(['bash',SRC_DIRECTORY+'/sort_script.sh',root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                subprocess.run(['touch', root + "/RESULTS_SORTED.txt"])
            except subprocess.CalledProcessError as e:
                print(e.stderr)
            
           
        
                file_path = root + "/" + file
                file_path_done = file_path + "DONE"
                subprocess.run(['mv',file_path,file_path_done])
            else:
                continue

        #At the end of the batch:
        #Remove all tag files, then create a DONE tag file.
        subprocess.run(["rm", root + "/STARTED.txt", root + "/SPLIT.txt", root + "/MPI_STEP.txt", root + "/RESULTS_PROCESSED.txt", root + "/RESULTS_SORTED.txt"])

        doneFilePath = root + "/DONE.txt"
        subprocess.run(['touch',doneFilePath])

def unzip(root, file):
    subprocess.run(['gunzip', root+"/"+file])

def split(root, file):
    nsf.split_file(root, file)

def MPI_Vina(root):
    try:
        subprocess.run(['bash',SRC_DIRECTORY+'/mpi_run_script.sh',root], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # could make this into python at some point??!
    except subprocess.CalledProcessError as e:
        print(e.stderr)

def getScores(root):
    npr.process(root)

def sortScores(root, file):
    pass

######################################################################################################################################################
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")






######################################################################################################################################################

send_email(subject, body, sender, recipients, password)
#main()        


