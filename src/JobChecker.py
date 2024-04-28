# Code to check whether the running jobs are idle or not.
#
#

import subprocess

result = subprocess.run(['qstat','large','|','grep','jburgess1'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

output = result.stdout

print(output)