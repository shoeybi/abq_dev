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
import sys
#import threading
import os
import time
import shutil
#threading._DummyThread._Thread__stop = lambda x: 42

current_dir     = aws.current_dir
companies_root  = aws.companies_root

def make_AMI(region_name, company_name, ops='ubuntu12.04', instance_type='m1.small'):
    
    ami_dic={('us-east-1','ubuntu12.04') : 'ami-23d9a94a',
             ('us-west-1','ubuntu12.04') : 'ami-c4072e81'}

# get the AMI
    ami 	= ami_dic[(region_name,ops)]
    
# get the region
    region 	= aws.get_region(region_name)

# launch an instance
    
    instance_id = aws.launch(instance_type = instance_type, 
                             ami 	   = ami, 
                             key_name      = company_name, 
                             region        = region )
    
    myconn 	= connect.Connection(instance_id,region,verbose=0)
# prepare nx
    current_dir = os.path.dirname(os.path.abspath(__file__))    
    myconn.run_at(current_dir+'/prepAWS_NX4beta.sh',
                  input_type='script',
                  wait_for_output=True,
                  print_stdout=True )
    
# wait for nx
    nx.wait_for_nx(myconn,verbose=0)

# get instance
    instance    = aws.get_instance(instance_id,region)

# make ami
    ami_id 	= instance.create_image('workstation nx-enabled instance 2')
    
# print
    print 'instance AMI with nx is '+ami_id

# kill instance
#    aws.terminate(instance_id,region)
    return ami_id
    
    
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

# associate ip
#    if aws.instance_is_running(instance_id,region) :
#        region.associate_address(instance_id   = instance_id, 
#                                 public_ip     = ip_address )

    # establish a connection
#    start_time = time.time()
    myconn = connect.Connection(instance_id,region,verbose=1)
#    print 'establish connection',time.time()-start_time
# prepare nx
#    current_dir = os.path.dirname(os.path.abspath(__file__))
#    myconn.run_at(current_dir+'/prepAWS_NX4beta.sh',
#                  input_type='script',
#                  wait_for_output=True,
#                  print_stdout=False )
# wait for nx
#    start_time = time.time()
#    nx.wait_for_nx(myconn,verbose=0)
#    print 'nx wait',time.time()-start_time

# add user 
#    start_time = time.time()

#    print instance_id,region,uname,pswd
    
    nx.add_user(userDic,myconn,webserver='www\.abaqual\.com',verbose=1)


#    print 'add user',time.time()-start_time
# install OpenFoam
#    myconn.run_at('installOpenFoam.sh',
#                  input_type='script',
#                  wait_for_output=True,
#                  print_stdout=False )

# disconnect
    myconn.disconnect()

# ----------------------------------------------------------------
# prepare an instance. This is part of the background in
# get_instance_id
# 
# 
# uname: username of the owner
# pswd:  password of the owner 
#  
# ----------------------------------------------------------------

def add_users(userDic, instance_id, region_name):

# get the region
    region 	= aws.get_region(region_name)

# establish a connection
    myconn = connect.Connection(instance_id,region,verbose=1)

# add user 
    nx.add_users(userDic,myconn,webserver='www\.abaqual\.com',verbose=1)

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
def get_instance_id(region_name, instance_type, os, company_name):
    
# AMI's
    ami_dic={('us-east-1','ubuntu12.04') : 'ami-7f507416',
             ('us-west-1','ubuntu12.04') : 'ami-2e99af6b'}

# get the AMI
    ami 	= ami_dic[(region_name,os)]
    
# get the region
    region 	= aws.get_region(region_name)
    
# launch an instance
#    start_time = time.time()
#    ip_address  = region.allocate_address().public_ip

#    print ip_address
#    print region_name, company_name, os, instance_type
#    sys.stdout.flush()
    instance    = aws.launch(instance_type = instance_type, 
                             ami 	   = ami, 
                             key_name      = company_name, 
                             region        = region )
#    print instance.id
#    print 'launch time',time.time()-start_time
# associate ip_address

# run a thread for instance preparation
#    thread 	= threading.Thread(target = prepare_instance, 
#                              args   = (uname, pswd, instance.id, region))
#    thread.start()
    
#    prepare_instance(uname, pswd, instance.id, region)
    return instance.id,instance.public_dns_name
    
# ----------------------------------------------------------------
# get the status of an instance
# return (status,ip_address,url)
# ----------------------------------------------------------------
def instance_status(instance_id, region_name, uname):

#    print 'in instance status'
# get the region
    region 	= aws.get_region(region_name)
# get the state    
    try: 
        instance 	= aws.get_instance(instance_id,region)
        state    	= instance.state.strip()
        ip_address	= instance.public_dns_name.strip()
#        print ' > state:',state
    except:
#        print ' > could not make it to state'
        return ('terminated','None','None')
    
    if state in ['terminated','shutting-down','invalid'] :
        return ('terminated','None','None')

    if state in ['stopped','stopping'] :
        return ('standby','None','None')
    
    if state =='running':
#        print ' > if state was runnig, should be here'
        if aws.ssh_working_quick_uname(instance_id,region,uname,verbose=0):
#            print '  >> ssh to the instance is working'
            port = '4443' 
            port = '4080' 
            url  = 'http://'+ip_address+':'+port
            return ('ready',ip_address,url)
    
    return ('starting up','None','None')

# ----------------------------------------------------------------
# start an instance
# ----------------------------------------------------------------
def start_instance(instance_id, region_name):

    region = aws.get_region(region_name)
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
def stop_instance(instance_id, region_name):

    region = aws.get_region(region_name)
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
def terminate_instance(instance_id, region_name):
    
    region = aws.get_region(region_name)
    # get the state
    try:
        state      = aws.state(instance_id,region)
        ip_address = aws.ip_address(instance_id,region)
    except:
        return
    
    if state in ['running','pending','stopped','stopping']:
        aws.terminate(instance_id,region)
#        region.disassociate_address(ip_address)
#        region.release_address(ip_address)
    else:
        print 'Warning in terminte_instance! state is '+state

# ----------------------------------------------------------------
# make company
# ----------------------------------------------------------------
def make_company(company_name, supported_regions): 
    
    company_dir = companies_root+'/'+company_name 
    if not os.path.exists(company_dir):
        os.makedirs(company_dir)
    if not os.path.exists(company_dir+'/sessions'):
        os.makedirs(company_dir+'/sessions')
    key_name 	= company_name
    for region_name in supported_regions:
        region   	= aws.get_region(region_name)
        aws.create_key(key_name, region)
# ----------------------------------------------------------------
# remove company
# ----------------------------------------------------------------
def remove_company(company_name, supported_regions): 
    
    key_name 	= company_name
    for region_name in supported_regions:
        region   	= aws.get_region(region_name)
        aws.remove_key(key_name, region)
    
    company_dir = companies_root+'/'+company_name 
    shutil.rmtree(company_dir)

