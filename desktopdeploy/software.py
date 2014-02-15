#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : Jan 2014
#
# function calls for managing software
# ================================================================
import os

# ----------------------------------------------------------------
# some pre-defined variables. may need to change later on
# ----------------------------------------------------------------

current_dir  = os.path.dirname(os.path.abspath(__file__))
software_dir = current_dir+'/software'

# ----------------------------------------------------------------
# install a piece of software
# ----------------------------------------------------------------

def install(software_name,connection,users,verbose=0):
    
# get the install script
    script_name	= software_dir+'/'+software_name+'/install.sh'

    try:
        with open(script_name): pass
    except IOError:
        raise NameError('cannot find '+script_name)

# install the script
    connection.run_at(script_name,
                      input_type='script',
                      wait_for_output=True,
                      print_stdout=True )
# copy the application icon to the server
    source 	= software_dir+'/'+software_name+'/'+software_name+'.desktop'
    destination	= '/home/ubuntu/.packages/'
    
    connection.copy_to(source,destination)

# populate the application icon to desktops
    icon     	= destination+software_name+'.desktop'
    command  	= ''
    for uname in users:
        command += 'sudo cp '+icon+' /home/'+uname+'/Desktop/'+' ;'
        command += 'sudo chown '+uname+' /home/'+uname+'/Desktop/'+software_name+'.desktop ;'
    
    connection.run_at(command)


# ----------------------------------------------------------------
# uninstall a piece of software
# ----------------------------------------------------------------

def uninstall(software_name,connection,users,verbose=0):
    
# get the install script
    script_name	= software_dir+'/'+software_name+'/uninstall.sh'

    try:
        with open(script_name): pass
    except IOError:
        raise NameError('cannot find '+script_name)

# install the script
    connection.run_at(script_name,
                      input_type='script',
                      wait_for_output=True,
                      print_stdout=True )

# populate the application icon to desktops
    
    filename    = software_name+'.desktop'
    command  	= 'sudo rm -f /home/ubuntu/.packages/'+filename+' ;'
        
    for uname in users:
        command += 'sudo rm -f /home/'+uname+'/Desktop/'+filename+' ;'
    
    connection.run_at(command)

# ----------------------------------------------------------------
# get software list
# ----------------------------------------------------------------
	
def get_software_list(connection,verbose=0):

# get the command
    command = 'more /home/ubuntu/.packages/installed'

# get the list
    out_lines = connection.run_at(command,
                                  input_type='command',
                                  wait_for_output=True)

# analyze the output
    output_list = [] 
    
    for line in out_lines:
        matchObj = re.search('^package\s(\S+)',line)
        if matchObj:
            output_list.append(matchObj.group(1))
 # return
    return output_list
