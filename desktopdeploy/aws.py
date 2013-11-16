#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : June 2013
#
# function calls for managing aws  
# ================================================================
import boto 
import ec2
import time
import sys
import subprocess
import os
import base64
import re

# ----------------------------------------------------------------
# some pre-defined variables. may need to change later on
# ----------------------------------------------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
companies_root = current_dir + '/../../abq_web/site/media/companies'

# ----------------------------------------------------------------
# query shows all the instances that are currently running
# ----------------------------------------------------------------
def query(instances=None,regions='all'):

# loop through all regions   
    regions_ = boto.ec2.regions()
    for region in regions_:

# only connect to the regions listed
        if region.name not in regions and regions is not 'all':
            continue
        conn = region.connect()
        reservations 	= conn.get_all_instances(instances)

# loop through all reservations in a region
        for reservation in reservations:
            instances_	= reservation.instances

# loop through all instances in a reservation
            for instance in instances_ :

# update the instance
                instance.update()

# print all the data
                print '-------------------------------------------------------'
                print 'id   	   ', instance.id
                print 'type        ', instance.instance_type
                print 'region name ', region.name
                print 'reservation ', reservation.id
                print 'public dns  ', instance.public_dns_name
                print 'ip address  ', instance.ip_address
                print 'state       ', instance.state 
                print 'kernel      ', instance.kernel
                print 'launch time ', instance.launch_time
                print 'key name    ', instance.key_name
                print 'image_id    ', instance.image_id

# ----------------------------------------------------------------
# kills all instances
# ----------------------------------------------------------------
def terminate_all(instances=None,regions='all',desired_ami=None):
# loop through all regions   
    regions_ = boto.ec2.regions()
    for region in regions_:
# only connect to the regions listed
        if region.name not in regions and regions is not 'all':
            continue
        conn = region.connect()
        reservations 	= conn.get_all_instances(instances)
# loop through all reservations in a region
        for reservation in reservations:
            instances_	= reservation.instances
# loop through all instances in a reservation
            for instance in instances_ :
# update the instance
                ip_address = instance.ip_address
                ami_id     = instance.image_id
                if ( ami_id == desired_ami) : 
                    print 'killing '+instance.id
                    instance.terminate()
                    try:
                        print 'releasing '+ip_address
                        conn.disassociate_address(ip_address)
                        conn.release_address(ip_address)
                    except:
                        pass

def get_region(region_name):
    
    regions_ = boto.ec2.regions()
    for region in regions_:
# only connect to the region
        if region.name.strip() == region_name.strip():
            return region.connect()
        
# raise error if couldnt find the name
    raise NameError('region '+region_name+' not found')

# ----------------------------------------------------------------
# create a security group
# ----------------------------------------------------------------
def create_security(ports, ip_protocol, security_group_name, region ):

# connect to the region
    conn = region
    
# create the security group
    try:
        conn.create_security_group(security_group_name, 
                                   security_group_name)
    except:
        pass
    
# add security rules
    for port in ports:
        try:
            conn.authorize_security_group(group_name = security_group_name, 
                                          ip_protocol = ip_protocol,
                                          from_port = port,
                                          to_port = port,
                                          cidr_ip = '0.0.0.0/0')
        except:
            pass

# ----------------------------------------------------------------
# revoke security rules
# ----------------------------------------------------------------
def revoke_security(ports, ip_protocol, security_group_name, region ):

# connect to the region
    conn = region
    
# add security rules
    for port in ports:
        try:
            conn.revoke_security_group(group_name = security_group_name, 
                                       ip_protocol = ip_protocol,
                                       from_port = port,
                                       to_port = port,
                                       cidr_ip = '0.0.0.0/0')
        except:
            pass
# ----------------------------------------------------------------
# encode a  key
# ----------------------------------------------------------------
def encode(filename):
    
    keystr = ''
    filenamepub = filename+'.pub'
    with open(filenamepub) as in_file:
        for line in in_file:
            keystr = keystr+line.strip()
      
    #encoded = base64.b64encode(keystr)
    return keystr

# ----------------------------------------------------------------
# remove key
# ----------------------------------------------------------------
def remove_key(key_name, region): 
    
    key_dir  = companies_root+'/'+key_name
    filename = key_dir+'/'+key_name+'.pem' 

# connect to the region
    conn = region

# clean up keys 
    try:
        conn.delete_key_pair(key_name) 
    except:
        pass
    
# ----------------------------------------------------------------
# create company key
# ----------------------------------------------------------------
def create_key(key_name, region): 
    
    key_dir  = companies_root+'/'+key_name
    filename = key_dir+'/'+key_name+'.pem' 
        
# connect to the region
    conn = region

#if key_file does not exist, make it
    try:
        with open(filename): pass
    except IOError:
        command = '/usr/bin/ssh-keygen -N "" -m PEM -f '+filename+' ;'+'chmod 400 '+filename+' ;'
        proc  = subprocess.Popen(command,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        out_lines = proc.stdout.readlines()
    encoded_key = encode(filename) 

#if key exists, just import it
    try:
        conn.import_key_pair(key_name, encoded_key)
    except:
        conn.delete_key_pair(key_name) 
        conn.import_key_pair(key_name, encoded_key)
    
# ----------------------------------------------------------------
# launch an instance
# ----------------------------------------------------------------
def launch(instance_type, ami, key_name, region ):

# connect to the region
    conn = region
    
# launch the instance
    try:
        security_group_name = 'abaqual_security_group' ;
        instance = conn.run_instances(ami,
                                      instance_type=instance_type,
                                      security_groups=
                                      [security_group_name],
                                      key_name=key_name).instances[0]
    except:
# create security then launch
        create_security([22,80,4000,4080,4443,8080], 
                        'tcp', 
                        security_group_name, 
                        region			)
    
        create_security([-1], 
                        'icmp', 
                        security_group_name, 
                        region 			)

        instance = conn.run_instances(ami,
                                      instance_type=instance_type,
                                      security_groups= 
                                      [security_group_name],
                                      key_name=key_name).instances[0]

# return the id and regionn
    return instance

# ----------------------------------------------------------------
# get the instance given its id and region
# ----------------------------------------------------------------
def get_instance(instance_id,region):

# get the connection to the region
    conn     = region
    if len(instance_id) < 5 :
        raise NameError('instance id '+instance_id+' is invalid')
# get the instance 
    try:
        instance = conn.get_all_instances(
            instance_ids=instance_id
            )[0].instances[0]
    except (boto.exception.EC2ResponseError,IndexError):
        raise NameError('instance id '+instance_id+' was not found')

# return the instance
    return instance 

# ----------------------------------------------------------------
# stop an instance using the instance_id
# ----------------------------------------------------------------
def stop(instance_id,region):
# get connection    
    conn     = region

# stop the instance
    try:
        result = conn.stop_instances(instance_ids=instance_id)
    except boto.exception.EC2ResponseError:
        raise NameError('could not stop instance '+instance_id)

# check if it is stopped
    if (result[0].id != instance_id):
        raise NameError('could not stop instance '+instance_id)

# ----------------------------------------------------------------
# terminate instance(s) using the instance_id(s)
# ----------------------------------------------------------------
def terminate(instance_ids,region):
# get connection    
    conn     = region

# terminate the instance

    try:
        result = conn.terminate_instances(instance_ids=instance_ids)
    except boto.exception.EC2ResponseError:
        raise NameError('could not terminate instances ')

# ----------------------------------------------------------------
# start an instance using the instance_id
# ----------------------------------------------------------------
def start(instance_id,region):
# get connection    
    conn     = region

# start the instance    
    try:
        result = conn.start_instances(instance_ids=instance_id)
    except boto.exception.EC2ResponseError:
        raise NameError('could not start instance '+instance_id)

# check if it is started
    if (result[0].id != instance_id):
        raise NameError('could not start instance '+instance_id)

# ----------------------------------------------------------------
# get the state of an instance using the instance_id
# ----------------------------------------------------------------
def state(instance_id,region):
# get connection
    try:
        instance = get_instance(instance_id,region=region)
        instance.update()
        return instance.state.strip()

    except NameError:
        return 'invalid'

# ----------------------------------------------------------------
# get the ip address of an instance using the instance_id
# ----------------------------------------------------------------
def ip_address(instance_id,region):
# get connection
    try:
        instance = get_instance(instance_id,region=region)
        instance.update()
        return instance.public_dns_name.strip()

    except NameError:
        return 'invalid'


# ----------------------------------------------------------------
# wait for an instance to run
# ----------------------------------------------------------------
def instance_is_running(instance_id,region,verbose=0):
    
    # get the instance
    instance = get_instance(instance_id,region)

    i = 0
    while i < 60 :
        state_ = state(instance_id,region)
        i = i + 1
        if (state_ == 'pending'):
            if i == 1:
                if verbose:
                    print 'waiting for instance '+instance_id+' to get ready',
            if verbose:
                print '.',
                sys.stdout.flush()
            time.sleep(5)
        elif (state_ == 'running'):
            if i > 1:
                if verbose:
                    print 'running! ip =',ip_address(instance_id,region)
                    sys.stdout.flush()
            return True
        else:
            if verbose:
                print ''
            return False
    if verbose:
        print ''
    return False

# ----------------------------------------------------------------
# wait for an instance to be at given state
# ----------------------------------------------------------------
def instance_is_at_state(desired_state,instance_id,region,verbose=0):
    
    i = 0
    while i < 60 :
        state_ = state(instance_id,region=region)
        i = i + 1
        if (state_ == desired_state.strip()):
            if i > 1:
                if verbose:
                    print 'instance is now '+desired_state
            return True
        else: 
            if i == 1:
                if verbose:
                    print 'waiting for instance '+instance_id,
            if verbose:
                print '.',
                sys.stdout.flush()
            time.sleep(5)
    if verbose:
        print ''
    return False

# ----------------------------------------------------------------
# ssh at the node
# ----------------------------------------------------------------
def ssh(instance_id,region,command='',time_out=10,persist=False):

# get the instance
    instance = get_instance(instance_id,region)

# get key and ip address
    ip_address    = instance.public_dns_name
    key_name      = instance.key_name
    key_dir  	  = companies_root+'/'+key_name
    key_filename  = key_dir+'/'+key_name+'.pem'
    try:
        with open(key_filename): pass
    except IOError:
        raise NameError('cannot find '+key_filename)

# prepare ssh command
    uname = 'ubuntu' 
    account  = uname+'@'+ip_address
    # persist
    if persist:
        persist_ = '-o "ControlPersist 600" '
    else: 
        persist_ = ''
    ssh_command = \
        'ssh -o "GSSAPIAuthentication no" -o "StrictHostKeyChecking no" '+\
        '-o "UserKnownHostsFile /dev/null" '+\
        '-o "ConnectTimeout '+str(time_out)+'" '+persist_+\
        '-i '+key_filename+' '+account
#        '-o "LogLevel QUIET" '+\
#        '-o "ControlMaster auto" -o "ControlPath ~/.ssh/'+account+'" '+\
# launch a ssh subprocess 
    print ssh_command+' '+command
    sys.stdout.flush()
    proc  = subprocess.Popen(ssh_command+' '+command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

# return the Popen object    
    return proc

# ----------------------------------------------------------------
# wait for an instance to run
# ----------------------------------------------------------------
def ssh_is_running(instance_id,region,verbose=0):
    
    i = 0
    while i < 60 :
        i = i + 1
        if (i == 1) and verbose:
            print 'waiting for ssh ',
        proc = ssh(instance_id,region,command='echo working')
        out_lines = proc.stdout.readlines()
        print out_lines
        time.sleep(10)
        try:
            out_phrase = out_lines[-1].strip()
        except:
            out_phrase = 'not working'
        if out_phrase == 'working':
            if verbose:
                print ' '
                sys.stdout.flush()
            return True
        else: 
            if verbose:
                print '.',
                sys.stdout.flush()

        
    return False

# ----------------------------------------------------------------
# wait for an instance to run
# ----------------------------------------------------------------
def ssh_working_quick(instance_id,region,verbose=0):

# initialize if needed
#    if not hasattr(ssh_working_quick, "last_time"):
#        ssh_working_quick.last_time = time.time()
         
# intervals for establishing conn is 500 sec
    update_time  = 500

# initialize if needed
#    if ( not hasattr(ssh_working_quick, "last_time") or  (time.time() - ssh_working_quick.last_time) > update_time ) : 

#        proc0 = ssh(instance_id,region,
#                    command='exit',time_out=1,persist=True)
#        ssh_working_quick.last_time = time.time()

# ssh
    proc = ssh(instance_id,region,
               command='echo working',time_out=10)
    out_lines = proc.stdout.readlines()
#    print "outlines:", out_lines
    try:
#        print '>stripping'
        out_phrase = out_lines[-1].strip()
#        print "out_phrase", out_phrase
    except:
        out_phrase = 'not working'

    if out_phrase == 'working':
        return True
    else: 
        return False
