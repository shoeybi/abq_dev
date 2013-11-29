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
import os

current_dir 	= aws.current_dir
companies_root 	= aws.companies_root
# ----------------------------------------------------------------
# is nx server working?
# ----------------------------------------------------------------   
def working(connection,verbose=0):    

# run the nx command
    out_lines = connection.run_at('sudo /usr/NX/bin/nxserver --status')

# analyze the output 
    working = False
    for line in out_lines:
#oldNx  if re.search("^NX>\s110\sNX\sServer\sis\srunning\.$",line):
        if re.search("NX>\s161\sEnabled\sservice:\snxhtd\.$",line):
            working = True

# write the output if needed
    if not working and verbose:
        print 'nx is not working, the output is:'
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
            if verbose:
                print 'waiting for nx to get ready',
        
        time.sleep(10)
        if verbose:
            print '.',
            sys.stdout.flush()
        
        if i > 60 :
            raise NameError('after 10 mins, nx is not working on ',connection.instance_id)
    
    if i > 1:
        if verbose:
            print ''
    
# ----------------------------------------------------------------
# run an nx command
# ----------------------------------------------------------------   
def run_nxcommand(command,connection,verbose=0):
    
# set the vebosity
    if verbose:
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
    if not success and verbose:
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
#oldNX      if re.search('NX>\s999\sBye\.$',line):
#oldNX           break
        if start_reading :
            matchObj = re.search('^(\S+)',line)
            if matchObj:
                output_list.append(matchObj.group(1))
        if re.search('^Username\s+Redirected\sto$',line):
            start_reading = True

# return
    return output_list

# ----------------------------------------------------------------
# write nxs file
# ----------------------------------------------------------------   
def write_nxs_file(uname,pswd,connection,width='1280',height='800',window_mode='fullscreen'):
    
# scramble password
    while True: 
        try:
            scrambled   = scramble.scrambleString(pswd)
            newline     = re.sub('TEST',scrambled,'_TEST_')
            break
        except:
            print 'bad scramble-->',scrambled

# replace attributes
    replace_items={
        'REPLACE_USER'       : uname,
        'REPLACE_PASSWORD'   : scrambled,
        'REPLACE_PUBLIC_DNS' : connection.ip_address,
        'REPLACE_WINDOW_MODE': window_mode,
        'REPLACE_WIDTH'      : width,
        'REPLACE_HEIGHT'     : height
      }
# get file names
    session_dir = companies_root+'/'+connection.key_name+'/sessions'
    master_file = current_dir+'/model.nxs'
    session_file_name = session_dir+'/'+connection.instance_id+'_'+uname+'.nxs'

#   open an output file
    out_file    = open(session_file_name, 'w')

# put the public DNS and PASSWORD in the file
    with open(master_file) as in_file:
        for line in in_file:
            for key in replace_items:
                line = re.sub(key,replace_items[key],line)
   
# write in the output file
            out_file.write(line),

# close both files
    in_file.close()
    out_file.close()

# ----------------------------------------------------------------
# add a user
# ----------------------------------------------------------------   
def add_user(uname,pswd,connection,sudoer=False,webserver='abaqual\.com',verbose=0):

# set the vebosity
    if verbose:
        print_stdout=True 
    else: 
        print_stdout=False

    '''
# add user to system
    command 		= '(sleep 2; echo '+pswd+'; sleep 2; echo '+pswd+\
        ' ) | sudo adduser --gecos \'\' --shell /bin/bash '+uname    
    dummy_lines        	= connection.run_at(command,print_stdout=print_stdout)
        
# add user to NX
    command 		= 'sudo /usr/NX/bin/nxserver --useradd '+uname    
    out_lines 		= connection.run_at(command,print_stdout=print_stdout)
        
# change the default to bash
#    command		= 'sudo chsh -s /bin/bash '+uname
#    dummy_lines 	= connection.run_at(command,print_stdout=print_stdout)

# copy the authorized keys
#    command		= 'sudo cp /home/ubuntu/.ssh/authorized_keys /home/'+uname+'/.ssh;'+\
#                          'sudo chown '+uname+':'+uname+' /home/'+uname+'/.ssh/authorized_keys'
#    dummy_lines 	= connection.run_at(command,print_stdout=print_stdout)

# add as a sudoer    
    if sudoer:
        command 	= 'sudo usermod -aG sudo '+uname
        dummy_lines 	= connection.run_at(command,print_stdout=print_stdout)
        
# make a .bashrc file
    command 		= 'sudo cp ~/.bashrc /home/'+uname+'/.bashrc;'+\
                          'sudo chown '+uname+':'+uname+' /home/'+uname+'/.bashrc'
    dummy_lines 	= connection.run_at(command,print_stdout=print_stdout)

# add the bashrccommon
#    command 		= 'sudo echo "#! /bin/bash" > ~/.bashrccommon;'+\
#                          'sudo echo ". /home/ubuntu/.bashrccommon" >> '+'/home/'+uname+'/.bashrc'
#    dummy_lines 	= connection.run_at(command,print_stdout=print_stdout)

    '''

# add user to system
    command  = ''
    command += '(sleep 2; echo '+pswd+'; sleep 2; echo '+pswd+\
        ' ) | sudo adduser --gecos \'\' --shell /bin/bash '+uname+' ;'    
        
# add user to NX
    command  += 'sudo /usr/NX/bin/nxserver --useradd '+uname+' ;'     
        
    if sudoer:
        command += 'sudo usermod -aG sudo '+uname+' ;'
        command += 'sudo sed -i s/abaqual\.com/'+webserver+'/g /usr/NX/share/htdocs/nxwebplayer/html/template.html ;'
        
# make a .bashrc file
    command 	+= 'sudo cp ~/.bashrc /home/'+uname+'/.bashrc;'+\
                          'sudo chown '+uname+':'+uname+' /home/'+uname+'/.bashrc'
    out_lines 	= connection.run_at(command,print_stdout=print_stdout)

# check if the user is added

    success = False    
    for line in out_lines:
        if re.search('^NX>\s301\sUser:\s'+uname+'\senabled\sin\sthe\sNX\suser\sDB\.$', \
                         line):
            success = True

    if not success and verbose:
        print 'user '+uname+' could not be added' 
    
# write the nxs file           
    if success:
        write_nxs_file(uname,pswd,connection)

    return success

# ----------------------------------------------------------------
# add a user
# ----------------------------------------------------------------   
def add_users(userDic,connection,webserver='abaqual\.com',verbose=0):

# set the vebosity
    if verbose:
        print_stdout=True 
    else: 
        print_stdout=False

# add user to system
    command  = ''
    command += 'sudo sed -i s/abaqual\.com/'+webserver+'/g /usr/NX/share/htdocs/nxwebplayer/html/template.html ;'

    for uname in userDic:
        pswd     = userDic[uname][0] 
        sudoer   = userDic[uname][1] 
        command += '(sleep 2; echo '+pswd+'; sleep 2; echo '+pswd+\
            ' ) | sudo adduser --gecos \'\' --shell /bin/bash '+uname+' ;'    
        
# add user to NX
        command  += 'sudo /usr/NX/bin/nxserver --useradd '+uname+' ;'     
# make a .bashrc file
        command  += 'sudo cp ~/.bashrc /home/'+uname+'/.bashrc;'+\
                          'sudo chown '+uname+':'+uname+' /home/'+uname+'/.bashrc ;'
# add to crontab        
        command  += 'echo \'*  *    * * *   '+uname+' export DISPLAY=:1001; scrot --thumb 160x90 /usr/NX/share/htdocs/nxwebplayer/desktops/disp.jpg; chmod a+r /usr/NX/share/htdocs/nxwebplayer/desktops/disp-thumb.jpg\' | sudo tee -a /etc/crontab ;'

        if sudoer:
            command += 'sudo usermod -aG sudo '+uname+' ;'

    out_lines 	= connection.run_at(command,print_stdout=print_stdout)

# check if the user is added
    
    success_all = True
    for uname in userDic:
        success = False    
        for line in out_lines:
            if re.search('^NX>\s301\sUser:\s'+uname+'\senabled\sin\sthe\sNX\suser\sDB\.$', \
                         line):
                success = True

        if not success and verbose:
            print 'user '+uname+' could not be added' 
    
# write the nxs file           
        if success:
            pswd  = userDic[uname][0] 
            write_nxs_file(uname,pswd,connection)
        
        success_all = success_all and success
        
    return success_all


# ----------------------------------------------------------------
# delete a user
# ----------------------------------------------------------------   
def del_user(uname,connection,verbose=0):

# set the vebosity
    if verbose:
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
                     '\shas\sbeen\sdeleted\sfrom\sthe\sNX\spassword\sDB\.$', line):
            success = True
    if not success and verbose:
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
            if verbose:
                print 'user '+uname+' was deleted'
    return True

