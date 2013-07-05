#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : June 2013
#
# function calls for managing nx 
# ================================================================
import connect
import re
import scramble
def working(instanceId,region='us-west-1',verbose=0):    
    working = False
    (stdout,stderr) = connect.run_at('sudo /usr/NX/bin/nxserver --status',\
                                         instanceId,wait=False)
    for line in stdout.readlines():
        if re.search("^NX>\s110\sNX\sServer\sis\srunning\.$",line):
            working = True
    if not working and (verbose > 0) :
        print "nx is not workin, the output is:"
        for line in stdout.readlines():
            print line,
    return working

def run_nxcommand(command,instanceId,region='us-west-1',verbose=0):
    (stdout,stderr) = connect.run_at('sudo /usr/NX/bin/nxserver --'+command,\
                                         instanceId,wait=False)
    if verbose > 1: 
        for line in stdout.readlines():
            print line,
    return (stdout,stderr)
    
def add_user(uname,pswd,instanceId,region='us-west-1',verbose=0):
    
    if not working(instanceId):
        raise nameError("nx is not working")
    command = 'echo -e \''+pswd+'\\n'+pswd+\
        '\' | sudo /usr/NX/bin/nxserver --system --useradd '+uname
    (stdout,stderr) = connect.run_at(command,instanceId,wait=True,verbose=0)
    return (stdout,stderr)

def write_nxs_file(uname,pswd,instanceId,region='us-west-1'):
#get file names
    session_dir = './sessions'
    session_file_name = session_dir+'/'+instanceId+'_'+uname+'.nxs'
    master_file = './amazon.nxs'
    out_file    = open(session_file_name, 'w')
#scrable the password
    scrambled   = scramble.scrambleString(pswd)
#get public_dns
    instance    = connect.get_instance(instanceId,region)
    public_dns  = instance.public_dns_name
    with open(master_file) as in_file:
        for line in in_file:
            line = re.sub('REPLACE_PUBLIC_DNS',public_dns,line)
            line = re.sub('REPLACE_USER',uname,line)
            line = re.sub('REPLACE_PASSWORD',scrambled,line)
            out_file.write(line),
    in_file.close()
    out_file.close()
