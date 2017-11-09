import subprocess
import sys


file = sys.argv[1]
args = ['python','-u',file]
output = subprocess.Popen(args=args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
print output
output = output.split('\n')
error = output[len(output)-2]
if "NameError" not  in error:
    quote_count = error.count('\'')
    if quote_count > 0:
        single_split = error.split('\'')
        error = error.replace(single_split[1],'')
if "File" in  output[0]:
    print output[0]
print error
