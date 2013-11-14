#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : June 2013
#
# function calls for connecting to EC2  
# ================================================================
import aws

class Connection:

    def __init__(self,instance_id,region,verbose=0):

# initiate
        self.instance_id     = instance_id
        self.region          = region
	self.verbose         = verbose
        self.shepherd_proc   = None

# check the status of the instance        
        if aws.instance_is_running(instance_id,region,verbose=verbose):
            pass
        else:
            raise NameError('instance '+instance_id+' is down')

# get ip address
        instance 	     = aws.get_instance(instance_id,region=region)
        instance.update()
    	self.ip_address      = instance.public_dns_name.strip()
        self.key_name        = instance.key_name.strip()

# initaite a subprocess ssh connection           
        if aws.ssh_is_running(instance_id,region,verbose):
            self.shepherd_proc   = True
#            self.shepherd_proc   = aws.ssh(instance_id,region,persist=True)

# ----------------------------------------------------------------
# get the state of connection by status of shepherd proc 
# ----------------------------------------------------------------   
    def connected(self):
        
        if self.shepherd_proc is None:
            return False
        else:
            return True
#        if self.shepherd_proc.returncode is None:
#            return True
#        else:
#            return False

# ----------------------------------------------------------------
# connect by initiating a shepherd ssh process 
# ----------------------------------------------------------------   
    def connect(self):
# check if already connected
        if self.connected():
            return

# initaite a subprocess ssh connection
        if aws.ssh_is_running(self.instance_id,self.region,self.verbose):
            self.shepherd_proc = True
#            self.shepherd_proc  = aws.ssh(self.instance_id,self.region,persist=True)

# check if ssh is alive            
        if not self.connected():
            raise NameError('ssh to '+self.instance_id+' died')
            

# ----------------------------------------------------------------
# disconnect by terminating the shepherd process
# ----------------------------------------------------------------   
    def disconnect(self):
# check if already connected
        if not self.connected():
            return
# terminate the current process        

#        self.shepherd_proc.terminate()
#        self.shepherd_proc.wait()
        self.shepherd_proc = None 
# check if ssh is alive            
        if self.connected():
            raise NameError('ssh to '+self.instance_id+' is alive')

# ----------------------------------------------------------------
# reconnect the shepherd process if not alive
# ----------------------------------------------------------------   
    def reconnect(self):       

# terminate the current process 
#        self.shepherd_proc.terminate()
#        self.shepherd_proc.wait()

# reconnect the shepherd if not alive
        if aws.ssh_is_running(self.instance_id,self.region,self.verbose):
#            self.shepherd_proc  = aws.ssh(self.instance_id,self.region,persist=True)    
            self.shepherd_proc  = True
            
# ----------------------------------------------------------------
# run a command or script at node
# ----------------------------------------------------------------   
    def run_at(self,input,input_type='command',wait_for_output=True,print_stdout=False):
# check if connected

        if not self.connected():
            self.connect()
        
# prepare the input command
        if   input_type is 'command' :
            command_prep = ' "'+input+'"'
        elif input_type is 'script' :
            try:
                with open(input): pass
            except IOError:
                raise NameError("cannot find "+input)
            command_prep = ' <'+input
        else :
            raise NameError(input_type+" is not recognized")

# run the command at ssh
        proc = aws.ssh(self.instance_id,self.region,command_prep)

# write the output if needed
        if wait_for_output:
            out_lines = proc.stdout.readlines()
            if print_stdout:
                for line in out_lines:
                    print line,
        else:
            out_lines = []        
        return out_lines
