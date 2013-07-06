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
    (out_lines,err_lines) = connect.run_at('sudo /usr/NX/bin/nxserver --status',\
                                         instanceId,wait=False,verbose=0)
    for line in out_lines:
        if re.search("^NX>\s110\sNX\sServer\sis\srunning\.$",line):
            working = True
    if not working and (verbose > 0) :
        print "nx is not working, the output is:"
        for line in out_lines:
            print line,
    return working

def run_nxcommand(command,instanceId,region='us-west-1',verbose=0):
    (out_lines,err_lines) = connect.run_at('sudo /usr/NX/bin/nxserver --'+command,\
                                         instanceId,wait=False,verbose=verbose)
    return (out_lines,err_lines)
    
def user_is_valid(uname,instanceId,region='us-west-1',verbose=0):
  
    success = False
    
    if not working(instanceId):
        raise nameError("nx is not working")
    
    nxcommand = 'usercheck '+uname
    (out_lines,err_lines) = run_nxcommand(nxcommand,instanceId,region,verbose=verbose)
    for line in out_lines:
        if re.search('^NX>\s900\sPublic\skey\sauthentication\ssucceeded\.$', line):
            success = True
    
    if not success and (verbose > 0) :
        print 'user '+uname+' is not working'

    return success

def user_list(instanceId,region='us-west-1',verbose=0):
    
    if not working(instanceId):
        raise nameError("nx is not working")

    command = 'userlist'
    (out_lines,err_lines) = run_nxcommand(command,instanceId,verbose=verbose)
    
    output_list = []
    
    start_reading = False
    for line in out_lines:
        if re.search('NX>\s999\sBye\.$',line):
            break
        if start_reading :
            matchObj = re.search('^(\S+)$',line)
            if matchObj:
                output_list.append(matchObj.group(1))
        if re.search('^--------------------------------$',line):
            start_reading = True
    return output_list
    

def add_user(uname,pswd,instanceId,region='us-west-1',verbose=0):
    
    if not working(instanceId):
        raise nameError("nx is not working")
    command = 'echo -e \''+pswd+'\\n'+pswd+\
        '\' | sudo /usr/NX/bin/nxserver --system --useradd '+uname
    (out_lines,err_lines) = connect.run_at(command,instanceId,wait=True,verbose=verbose)
    
    success = False
    
    for line in out_lines:
        if re.search('^NX>\s301\sUser:\s'+uname+'\senabled\sin\sthe\sNX\suser\sDB\.$', \
                         line):
            success = True
            
    if not success and (verbose > 0) :
        print 'user '+uname+' could not be added'
    
    return success

def del_user(uname,instanceId,region='us-west-1',verbose=0):
    
    if not user_is_valid(uname,instanceId,region,verbose=verbose):
        return True

    if not working(instanceId):
        raise nameError("nx is not working")
    
    command = 'userdel '+uname+' --system'
    (out_lines,err_lines) = run_nxcommand(command,instanceId,verbose=verbose)
    
    success = False
        
    for line in out_lines:
        if re.search('^NX>\s307\sUser:\s'+uname+'\sremoved\sfrom\sthe\ssystem\.$', line):
            success = True
    if not success and (verbose > 0) :
        print 'user '+uname+' cannot be removed'
    
    return success

def del_all_users(instanceId,region='us-west-1',verbose=0):
    for uname in user_list(instanceId,region,verbose=verbose):
        if not del_user(uname,instanceId,region,verbose=verbose):
            raise nameError('could not delete user '+uname)
    return True

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
