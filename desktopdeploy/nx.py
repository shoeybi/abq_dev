#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : June 2013
#
# function calls for managing nx 
# ================================================================
import connect
import aws
import re
import scramble
import time
import sys

# ----------------------------------------------------------------
# is nx server working?
# ----------------------------------------------------------------   
def working(connection,verbose=0):    

# run the nx command
    out_lines = connection.run_at('sudo /usr/NX/bin/nxserver --status')

# analyze the output 
    working = False
    for line in out_lines:
        if re.search("^NX>\s110\sNX\sServer\sis\srunning\.$",line):
            working = True

# write the output if needed
    if not working and (verbose > 0) :
        print "nx is not working, the output is:"
        for line in out_lines:
            print line,

# return  
    return working

# ----------------------------------------------------------------
# wait for nx server to work?
# ----------------------------------------------------------------   
def wait_for_nx(connection,verbose=0):    

# wait for instance to run
    if aws.instance_is_running(connection.instance_id,connection.region) is not True:
        raise NameError('instance '+connection.instance_id+' is not running')

# wait for nx to run    
    i = 0
    while working(connection,verbose=verbose) is not True:    
        i = i + 1       
        if i == 1:
            print 'waiting for nx to get ready',
        
        time.sleep(10)
        print '.',
        sys.stdout.flush()
        
        if i > 60 :
            raise NameError('after 10 mins, nx is not working on ',connection.instance_id)
    
    if i > 1:
        print ''
    
# ----------------------------------------------------------------
# run an nx command
# ----------------------------------------------------------------   
def run_nxcommand(command,connection,verbose=0):
    
# set the vebosity
    if verbose > 0 :
        print_stdout=True 
    else: 
        print_stdout=False 

# run ssh command
    out_lines = connection.run_at('sudo /usr/NX/bin/nxserver --'+command,\
                                   print_stdout=print_stdout)

# return    
    return out_lines

# ----------------------------------------------------------------
# check if username is valid
# ----------------------------------------------------------------   
def user_is_valid(uname,connection,verbose=0):
  
# prepare nx command    
    nxcommand = 'usercheck '+uname

# run the nxcommand
    out_lines = run_nxcommand(nxcommand,connection,verbose=verbose)

# analyze the output
    success = False
    for line in out_lines:
        if re.search('^NX>\s900\sPublic\skey\sauthentication\ssucceeded\.$', line):
            success = True
            
# write output if needed
    if not success and (verbose > 0) :
        print 'user '+uname+' is not working'

# return
    return success

# ----------------------------------------------------------------
# get the userlist
# ----------------------------------------------------------------   
def user_list(connection,verbose=0):
    
# prepare nx command
    nxcommand = 'userlist'
    out_lines = run_nxcommand(nxcommand,connection,verbose=verbose)
    
# analyze the output
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

# return
    return output_list

# ----------------------------------------------------------------
# write nxs file
# ----------------------------------------------------------------   
def write_nxs_file(uname,pswd,connection):

# get file names
    session_dir = './sessions'
    master_file = './amazon.nxs'
    session_file_name = session_dir+'/'+connection.instance_id+'_'+uname+'.nxs'

#   open an output file
    out_file    = open(session_file_name, 'w')

# get public_dns
    public_dns  = connection.public_dns

# put the public DNS and PASSWORD in the file
    with open(master_file) as in_file:
        for line in in_file:
            line = re.sub('REPLACE_PUBLIC_DNS',public_dns,line)
            line = re.sub('REPLACE_USER',uname,line)
            if re.search('REPLACE_PASSWORD',line):
                while True: 
                    try:
# scrable the password
                        scrambled   = scramble.scrambleString(pswd)
                        newline     = re.sub('REPLACE_PASSWORD',scrambled,line)
                        break
                    except:
                        print 'bad scramble-->',scrambled
                line = newline

# write in the output file
            out_file.write(line),

# close both files
    in_file.close()
    out_file.close()

# ----------------------------------------------------------------
# add a user
# ----------------------------------------------------------------   
def add_user(uname,pswd,connection,verbose=0):

# set the vebosity
    if verbose > 0 :
        print_stdout=True 
    else: 
        print_stdout=False 

# prepare a command
    command = 'echo -e \''+pswd+'\\n'+pswd+\
        '\' | sudo /usr/NX/bin/nxserver --system --useradd '+uname
   
# run the command
    out_lines = connection.run_at(command,print_stdout=print_stdout)
    
# check if the user is added
    success = False    
    for line in out_lines:
        if re.search('^NX>\s301\sUser:\s'+uname+'\senabled\sin\sthe\sNX\suser\sDB\.$', \
                         line):
            success = True

    if not success and (verbose > 0) :
        print 'user '+uname+' could not be added' 

# write the nxs file           
    if success:
        write_nxs_file(uname,pswd,connection)

    return success

# ----------------------------------------------------------------
# delete a user
# ----------------------------------------------------------------   
def del_user(uname,connection,verbose=0):

# set the vebosity
    if verbose > 0 :
        print_stdout=True 
    else: 
        print_stdout=False 

# kill sessions
    out_lines = run_nxcommand('kill '+uname,connection,verbose=verbose)

# delete user on system
    out_lines = connection.run_at('sudo userdel -rf '+uname,print_stdout=print_stdout)

# delete user on nx
    out_lines = run_nxcommand('userdel '+uname,connection,verbose=verbose)
    
# check if the use is removed
    success = False        
    for line in out_lines:
        if re.search('^NX>\s303\sPassword\sfor\suser:\s'+uname+\
                     '\sremoved\sfrom\sthe\sNX\spassword\sDB\.$', line):
            success = True
    if not success and (verbose > 0) :
        print 'user '+uname+' cannot be removed'

# return    
    return success

# ----------------------------------------------------------------
# delete all users
# ----------------------------------------------------------------   
def del_all_users(connection,verbose=0):

# loop through usernames and delete them 
    for uname in user_list(connection,verbose=verbose):
        if not del_user(uname,connection,verbose=verbose):
            raise NameError('could not delete user '+uname)
        else:
            if verbose > 0 :
                print 'user '+uname+' was deleted'
    return True

