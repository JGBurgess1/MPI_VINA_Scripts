# Code to check whether the running jobs are idle or not.
#
#

import subprocess

result = subprocess.run(['qstat','large'],stdout=subprocess.PIPE)
output = result.stdout

print(output)