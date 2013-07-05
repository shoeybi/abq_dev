out_filename = 'output.nxs'
out_file = open(out_filename, 'w')
import re
public_dns = '123456'
user = 'yaser'
password = 'haha'
with open('amazon.nxs') as f:
    for line in f:
        line = re.sub('REPLACE_PUBLIC_DNS',public_dns,line)
        line = re.sub('REPLACE_USER',user,line)
        line = re.sub('REPLACE_PASSWORD',password,line)
        out_file.write(line),
f.close()
out_file.close()

    # line = f.readlines()
   # i = i + 1
   # if i < 2:
   #     print i
        #print line
#import ec2
#import boto
#conn     = boto.ec2.connect_to_region('us-west-1')
#print conn.get_spot_price_history
#print conn.get_all_key_pairs()
#key      = conn.create_key_pair('mynewkey3')
#keyPair2  = conn.get_key_pair('mynewkey5')
#print keyPair2
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
