import ec2
import boto
conn     = boto.ec2.connect_to_region('us-west-1')
print conn.get_all_key_pairs()
#key      = conn.create_key_pair('mynewkey3')
keyPair2  = conn.get_key_pair('mynewkey5')
print keyPair2
#help(keyPair2)
#keyPair2.save('/tmp')

#import subprocess
#connect.AWSquery2('micro')
#connect.AWSquery2("us-west-1")
#p = subprocess.Popen('ls -altr', 
#                     shell=True, 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    print line,
#retval = p.wait()

#if 0 :
#    print "haha"
#if 1 :
#    print "hoojp"
