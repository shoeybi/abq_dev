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

# ----------------------------------------------------------------
# some pre-defined variables. may need to change later on
# ----------------------------------------------------------------

# a key dir
key_dir = '/Users/khalighi/Projects/Abaqual/keys'
# a security group
scg = ['quicklaunch-0']

# ----------------------------------------------------------------
# query shows all the instances that are currently running
# ----------------------------------------------------------------
def query(instances=None,regions="all"):

# loop through all regions   
    regions_ = boto.ec2.regions()
    for region in regions_:

# only connect to the regions listed
        if region.name not in regions and regions is not "all":
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
                print "-------------------------------------------------------"
                print "id   	   ", instance.id
                print "type        ", instance.instance_type
                print "region name ", region.name
                print "reservation ", reservation.id
                print "public dns  ", instance.public_dns_name
                print "state       ", instance.state 
                print "kernel      ", instance.kernel
                print "launch time ", instance.launch_time
                print "key name    ", instance.key_name
                print "image_id    ", instance.image_id

# ----------------------------------------------------------------
# kills all instances
# ----------------------------------------------------------------
def terminate_all(instances=None,regions="all"):
# loop through all regions   
    regions_ = boto.ec2.regions()
    for region in regions_:
# only connect to the regions listed
        if region.name not in regions and regions is not "all":
            continue
        conn = region.connect()
        reservations 	= conn.get_all_instances(instances)
# loop through all reservations in a region
        for reservation in reservations:
            instances_	= reservation.instances
# loop through all instances in a reservation
            for instance in instances_ :
# update the instance
                instance.terminate()

# ----------------------------------------------------------------
# launch an instance
# ----------------------------------------------------------------
def launch(instance_type, ami, key_name, region ):

# connect to the region
    conn = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# create the key if needed
    if conn.get_key_pair(key_name) is None:
        key      = conn.create_key_pair(key_name)
        try:
            key.save( key_dir )
        except:
            raise NameError("could not save the key "+key_name)
    else:
        filename = key_dir+"/"+key_name+'.pem'
        try:
            with open(filename): pass
        except IOError:
            raise NameError("cannot find "+filename)
        
# launch the instance
    instance = conn.run_instances(ami,
                                  instance_type=instance_type,
                                  security_groups=scg,
                                  key_name=key_name).instances[0]
    if instance is None :
        raise NameError("instance could not be launched")

# return the id and regionn
    return instance.id

# ----------------------------------------------------------------
# get the instance given its id and region
# ----------------------------------------------------------------
def get_instance(instance_id,region):

# get the connection to the region
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# get the instance 
    try:
        instance = conn.get_all_instances(
            instance_ids=instance_id
            )[0].instances[0]
    except (boto.exception.EC2ResponseError,IndexError):
        raise NameError("instance id "+instance_id+" was not found")

# return the instance
    return instance 

# ----------------------------------------------------------------
# stop an instance using the instance_id
# ----------------------------------------------------------------
def stop(instance_id,region):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# stop the instance
    try:
        result = conn.stop_instances(instance_ids=instance_id)
    except boto.exception.EC2ResponseError:
        raise NameError("could not stop instance "+instance_id)

# check if it is stopped
    if (result[0].id != instance_id):
        raise NameError("could not stop instance "+instance_id)

# ----------------------------------------------------------------
# terminate instance(s) using the instance_id(s)
# ----------------------------------------------------------------
def terminate(instance_ids,region):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# terminate the instance

    try:
        result = conn.terminate_instances(instance_ids=instance_ids)
    except boto.exception.EC2ResponseError:
        raise NameError("could not terminate instances ")

# ----------------------------------------------------------------
# start an instance using the instance_id
# ----------------------------------------------------------------
def start(instance_id,region):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# start the instance    
    try:
        result = conn.start_instances(instance_ids=instance_id)
    except boto.exception.EC2ResponseError:
        raise NameError("could not start instance "+instance_id)

# check if it is started
    if (result[0].id != instance_id):
        raise NameError("could not start instance "+instance_id)

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
        return "invalid"

# ----------------------------------------------------------------
# wait for an instance to run
# ----------------------------------------------------------------
def instance_is_running(instance_id,region):
    
    i = 0
    while i < 60 :
        state_ = state(instance_id,region=region)
        i = i + 1
        if (state_ == 'pending'):
            if i == 1:
                print 'waiting for instance '+instance_id+' to get ready',
            print '.',
            sys.stdout.flush()
            time.sleep(5)
        elif (state_ == 'running'):
            if i > 1:
                print 'running! waiting for another 10 sec'
                time.sleep(10)
            return True
        else:
            print ''
            return False
        
    print ''
    return False

# ----------------------------------------------------------------
# wait for an instance to be at given state
# ----------------------------------------------------------------
def instance_is_at_state(desired_state,instance_id,region):
    
    i = 0
    while i < 60 :
        state_ = state(instance_id,region=region)
        i = i + 1
        if (state_ == desired_state.strip()):
            if i > 1:
                print 'instance is now '+desired_state
            return True
        else: 
            if i == 1:
                print 'waiting for instance '+instance_id,
            print '.',
            sys.stdout.flush()
            time.sleep(5)
    print ""
    return False

# ----------------------------------------------------------------
# ssh at the node
# ----------------------------------------------------------------
def ssh(instance_id,region,command=''):

# get the instance
    instance = get_instance(instance_id,region)

# get key and ip address
    public_dns    = instance.public_dns_name
    key_name      = instance.key_name
    key_filename  = key_dir+"/"+key_name+'.pem'
    try:
        with open(key_filename): pass
    except IOError:
        raise NameError("cannot find "+filename)

# prepare ssh command
    uname = 'ubuntu' 
    account  = uname+'@'+public_dns
    ssh_command = \
        'ssh -o "GSSAPIAuthentication no" -o "StrictHostKeyChecking no" '+\
        '-o "ControlMaster auto" -o "ControlPath ~/.ssh/'+account+'" -i '+\
        key_filename+' '+account

# launch a ssh subprocess    
    proc  = subprocess.Popen(ssh_command+' '+command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

# return the Popen object    
    return proc
