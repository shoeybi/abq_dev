#!/usr/bin/env python
# ================================================================
# Author : Yaser Khalighi
# Date : June 2013
#
# function calls for managing and connecting to EC2  
# ================================================================
import boto 
import ec2
import time
import sys
import subprocess
# a key dir
key_dir = '/Users/khalighi/Projects/Abaqual/keys'
# a security group
scg = ['quicklaunch-0']
# AWSquery shows all the instances that are currently running
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

# kills all the instances that are currently available
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

def launch_instance(instance_type='t1.micro',\
                        ami      ='ami-fe002cbb',\
                        key_name ='abaqual_key',\
                        region   ='us-west-1'):
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
    return instance.id,region

def get_instance(instanceId,region='us-west-1'):

# get the connection to the region
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# get the instance 
    try:
        instance = conn.get_all_instances(
            instance_ids=instanceId
            )[0].instances[0]
    except (boto.exception.EC2ResponseError,IndexError):
        raise NameError("instance id "+instanceId+" was not found")

# return the instance
    return instance 

def stop_instance(instanceId,region='us-west-1'):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# stop the instance
    try:
        result = conn.stop_instances(instance_ids=instanceId)
    except boto.exception.EC2ResponseError:
        raise NameError("could not stop instance "+instanceId)

# check if it is stopped
    if (result[0].id != instanceId):
        raise NameError("could not stop instance "+instanceId)

def terminate_instance(instanceId,region='us-west-1'):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# terminate the instance
    try:
        result = conn.terminate_instances(instance_ids=instanceId)
    except boto.exception.EC2ResponseError:
        raise NameError("could not terminate instance "+instanceId)

# check if it is terminated
    if (result[0].id != instanceId):
        raise NameError("could not terminate instance "+instanceId)

def start_instance(instanceId,region='us-west-1'):
# get connection    
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")

# start the instance    
    try:
        result = conn.start_instances(instance_ids=instanceId)
    except boto.exception.EC2ResponseError:
        raise NameError("could not start instance "+instanceId)

# check if it is started
    if (result[0].id != instanceId):
        raise NameError("could not start instance "+instanceId)

def state_instance(instanceId,region='us-west-1'):
# get connection
    try:
        instance = get_instance(instanceId,region=region)
        instance.update()
        return instance.state
    except NameError:
        return "invalid"

def instance_is_running(instanceId,region='us-west-1'):
    
    i = 0
    while i < 60 :
        state = state_instance(instanceId,region=region)
        i = i + 1
        if (state == "pending"):
            if i == 1:
                print "waiting for instance "+instanceId+" to get ready",
            print ".",
            sys.stdout.flush()
            time.sleep(5)
        elif (state == "running"):
            if i > 1:
                print "running! waiting for another 30 sec"
                time.sleep(30)
            return 1
        else:
            print ""
            return 0
        
    print ""
    return 0

def run_at(input,instanceId,input_type='command',\
               wait=False,region='us-west-1',verbose=0):
# get connection
    conn     = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")
#get instance and check if it is running    
    instance = get_instance(instanceId,region=region)
    if not instance_is_running(instanceId,region):
        raise NameError("cannot connect to instance "+instanceId)
#get key and ip address
    instance.update()
    public_dns    = instance.public_dns_name
    key_name      = instance.key_name
    key_filename = key_dir+"/"+key_name+'.pem'
    try:
        with open(key_filename): pass
    except IOError:
        raise NameError("cannot find "+filename)
#prepare the input command
    if   input_type is 'command' :
        command_prep = ' "'+input+'"'
    elif input_type is 'script' :
        try:
            with open(input): pass
        except IOError:
            raise NameError("cannot find "+input)
        command_prep = ' <'+input
    else :
        raise nameError(input_type+" is not recognized")
#prepare the ssh command
    uname = 'ubuntu'
    ssh_command = \
        'ssh  -o "GSSAPIAuthentication no" -o "StrictHostKeyChecking no" -i '+\
        key_filename+' '+uname+'@'+public_dns
#run the command
    if verbose > 0: 
        print "running at instance : "+ssh_command+command_prep  
    p = subprocess.Popen(ssh_command+command_prep,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
#write the output
    if verbose > 1: 
        for line in p.stdout.readlines():
            print line,
#wait for the command to finish
    if wait:
        for line in p.stdout.readlines():
            pass
#return the output
    return (p.stdout,p.stderr)

            
            
