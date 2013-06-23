import boto 
import ec2
def AWSquery():
    regions = boto.ec2.regions()
    for region in regions:
        conn = region.connect()
        reservations 	= conn.get_all_instances()
#    images = conn.get_all_images()
#    for image in images:
        for reservation in reservations:
            instances	= reservation.instances
            for instance in instances :
                instance.update()
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

def AWSrun(region='us-west-1',type='micro'):
    conn = boto.ec2.connect_to_region(region)
    key = 'AWS_desktop_hosts'
    if ( type == 'micro' ) :
        conn.run_instances('ami-fe002cbb',instance_type='t1.micro',key_name=key)
    if ( type == 'small' ) :
        conn.run_instances('ami-fe002cbb',instance_type='m1.small',key_name=key)
    if ( type == 'medium' ) :
        conn.run_instances('ami-fe002cbb',instance_type='m1.medium',key_name=key)
    if ( type == 'large' ) :
        conn.run_instances('ami-fe002cbb',instance_type='m1.large',key_name=key)
        
