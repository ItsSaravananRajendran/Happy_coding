import subprocess
import sys


file = sys.argv[1]
args = ['python','-u',file]
output = subprocess.Popen(args=args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
print output
output = output.split('\n')
error = output[len(output)-2]
replace = error.split('\'')
error = error.replace(replace[1],'')
print error
