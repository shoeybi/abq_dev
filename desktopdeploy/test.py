#import connect
import subprocess
#connect.AWSquery2('micro')
#connect.AWSquery2("us-west-1")
p = subprocess.Popen('sleep 3', 
                     shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print line,
retval = p.wait()

