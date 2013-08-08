#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : Aug 2013
#
# interface to the web server
# ================================================================
import aws
import connect
import nx
import threading

# ----------------------------------------------------------------
# prepare an instance. This is part of the background in
# get_instance_id
# 
# 
# uname: username of the owner
# pswd:  password of the owner 
#  
# ----------------------------------------------------------------

def prepare_instance(uname, pswd, instance_id, region):

# establish a connection
    myconn = connect.Connection(instance_id,region)
    
# prepare nx
    myconn.run_at('prepAWS_NX4beta.sh',
                  input_type='script',
                  wait_for_output=True,
                  print_stdout=False )
# wait for nx
    nx.wait_for_nx(myconn)

# add user 
    nx.add_user(uname,pswd,myconn,sudoer=True,verbose=0)

# install OpenFoam
    myconn.run_at('installOpenFoam.sh',
                  input_type='script',
                  wait_for_output=True,
                  print_stdout=False )

# disconnect
    myconn.disconnect()

# ----------------------------------------------------------------
# launch an prepare an instance, then return the instance id
# 
# supported OS's are: 
#   - ubuntu12.04
#
# supported regions are:
#   - us-east-1
#   - us-west-1
# 
# supported instance_types are the same as amazon nodes such as
# m1.medium, t1.micro, etc
# 
# company_name is required to make a key 
# 
# uname: username of the owner
# pswd:  password of the owner 
#  
# ----------------------------------------------------------------
def get_instance_id(region, instance_type, os, company_name, uname, pswd):
    
# supported lists
    supported_os_list     = ['ubuntu12.04'] 
    supported_region_list = ['us-east-1', 
                             'us-west-1'] 
    supported_instance_type_list = ['t1.micro', 
                                    'm1.small',
                                    'm1.medium',
                                    'm1.large',
                                    'c1.medium',
                                    'c1.xlarge'] 
                          
# AMI's
    ami_dic={('us-east-1','ubuntu12.04') : 'ami-23d9a94a',
             ('us-west-1','ubuntu12.04') : 'ami-c4072e81'}

# error checks
    if region not in supported_region_list :
        raise NameError('region '+region+' is not supported') 

    if os not in supported_os_list :
        raise NameError('os '+os+' is not supported') 

    if instance_type not in supported_instance_type_list :
        raise NameError('instnace_type '+instance_type+' is not supported') 
    
# get the AMI
    ami = ami_dic[(region,os)]

# launch an instance
    instance_id = aws.launch(instance_type = instance_type, 
                             ami 	   = ami, 
                             key_name      = company_name, 
                             region        = region )
    
    thread = threading.Thread(target = prepare_instance, 
                              args   = (uname, pswd, instance_id, region))
    thread.start()
    return instance_id
    
# ----------------------------------------------------------------
# get the status of an instance
# ----------------------------------------------------------------
def instance_status(instance_id, region):

# get the state    
    try: 
        state = aws.state(instance_id,region)
    except:
        return 'terminated'

    if state in ['terminated','shutting-down'] :
        return 'terminated'

    if state in ['stopped','stopping'] :
        return 'standby' 
    
    if state =='running':
        myconn = connect.Connection(instance_id,region)
        if nx.working(myconn):
            return 'ready'
        myconn.disconnect()
    
    return 'starting up'

# ----------------------------------------------------------------
# start an instance
# ----------------------------------------------------------------
def start_instance(instance_id, region):

    # get the state
    try:
        state = aws.state(instance_id,region)
    except:
        return
    
    if state=='stopped':
        aws.start(instance_id,region)
    else:
        print 'Warning in start_instance: cannot start! state is '+state

# ----------------------------------------------------------------
# stop an instance
# ----------------------------------------------------------------
def stop_instance(instance_id, region):

    # get the state
    try:
        state = aws.state(instance_id,region)
    except:
        return
    
    if state=='running':
        aws.stop(instance_id,region)
    else:
        print 'Warning in stop_instance: cannot stop! state is '+state    
# ----------------------------------------------------------------
# terminte an instance
# ----------------------------------------------------------------
def terminate_instance(instance_id, region):

    # get the state
    try:
        state = aws.state(instance_id,region)
    except:
        return
    
    if state in ['running','pending','stopped','stopping']:
        aws.terminate(instance_id,region)
    else:
        print 'Warning in terminte_instance! state is '+state
# ----------------------------------------------------------------
# get public dns
# ----------------------------------------------------------------
def get_public_dns(instance_id, region):
    
    # get status
    status = instance_status(instance_id, region)
    
    if status=='ready' :
        instance   = aws.get_instance(instance_id,region)
        public_dns = instance.public_dns_name
        return public_dns
    else :
        return 'None'

# ----------------------------------------------------------------
# get public dns
# ----------------------------------------------------------------
def get_url(instance_id, region):
    
    port = '4443' 
    # get status
    status = instance_status(instance_id, region)
    
    if status=='ready' :
        instance   = aws.get_instance(instance_id,region)
        public_dns = instance.public_dns_name
        return 'https://'+public_dns+':'+port
    else :
        return 'None'

