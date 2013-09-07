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
import os
import time
import shutil
threading._DummyThread._Thread__stop = lambda x: 42

current_dir     = aws.current_dir
companies_root  = aws.companies_root
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
#    start_time = time.time()
    myconn = connect.Connection(instance_id,region,verbose=0)
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
    nx.add_user(uname,pswd,myconn,sudoer=True,verbose=0)
#    print 'add user',time.time()-start_time
# install OpenFoam
#    myconn.run_at('installOpenFoam.sh',
#                  input_type='script',
#                  wait_for_output=True,
#                  print_stdout=False )

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
def get_instance_id(region_name, instance_type, os, company_name, uname, pswd='1234'):
    
# AMI's

#    ami_dic={('us-east-1','ubuntu12.04') : 'ami-23d9a94a',
#             ('us-west-1','ubuntu12.04') : 'ami-c4072e81'}
# ami-d8fdd79d is a prepared west UBUNTU, replacing ami-c4072e81
    
    ami_dic	={('us-west-1','ubuntu12.04') : 'ami-d8fdd79d',
                  ('us-east-1','ubuntu12.04') : 'ami-23d9a94a'}

# get the AMI
    ami 	= ami_dic[(region_name,os)]
    
# get the region
    region 	= aws.get_region(region_name, supported_regions)
    
# launch an instance
#    start_time = time.time()
    instance_id = aws.launch(instance_type = instance_type, 
                             ami 	   = ami, 
                             key_name      = company_name, 
                             region        = region )
    
#    print 'launch time',time.time()-start_time

    thread 	= threading.Thread(target = prepare_instance, 
                              args   = (uname, pswd, instance_id, region))
    thread.start()
    return instance_id
    
# ----------------------------------------------------------------
# get the status of an instance
# return (status,public_dns,url)
# ----------------------------------------------------------------
def instance_status(instance_id, region_name, supported_regions):

# get the region
    region 	= aws.get_region(region_name, supported_regions)
# get the state    
    try: 
        instance 	= aws.get_instance(instance_id,region)
        state    	= instance.state.strip()
        public_dns	= instance.public_dns_name.strip()
    except:
        return ('terminated','None','None')
    
    if state in ['terminated','shutting-down','invalid'] :
        return ('terminated','None','None')

    if state in ['stopped','stopping'] :
        return ('standby','None','None')
    
    if state =='running':
        if aws.ssh_working_quick(instance_id,region):
            port = '4443' 
            url  = 'https://'+public_dns+':'+port
            return ('ready',public_dns,url)
    
    return ('starting up','None','None')

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
def terminate_instance(instance_id, region_name, supported_regions):
    
    region = aws.get_region(region_name, supported_regions)
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

