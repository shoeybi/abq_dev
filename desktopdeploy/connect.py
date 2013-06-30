import boto 
import ec2
# a key
key = 'AWS_desktop_hosts'
# a security group
scg = ['quicklaunch-0']
# an AMI
ami = 'ami-fe002cbb'
# supported instance types
INSTANCE_TYPES = {'micro':'t1.micro', 
                  'small' :'m1.small',
                  'medium':'m1.medium',
                  'large ':'m1.large',
                  }
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

def launch_instance(type='micro',region='us-west-1'):
# connect to the region
    conn = boto.ec2.connect_to_region(region)
    if conn is None :
        raise NameError("region "+region+" is invalid")
# get the instance type based on type
    try:
        instance_type = INSTANCE_TYPES[type]
    except:
        print "instance type "+type+" is not supported"
        raise
# launch the instance
    instance = conn.run_instances(ami,
                                  instance_type=instance_type,
                                  security_groups=scg,
                                  key_name=key).instances[0]
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
        instance = conn.get_all_instances(instance_ids=instanceId)[0].instances[0]
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
        return instance.state
    except NameError:
        return "invalid"
    
def run_at_instance(instanceId,region='us-west-1'):
# get instance
    instance = get_instance(instanceId,region=region)
    
    if instance.state
