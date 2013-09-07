import sys
import interface
myid = sys.argv[1]
region_name = sys.argv[2]
supported_regions = ['us-west-1','us-west-2','us-east-1']
for i in range(10):
    print interface.instance_status(myid, region_name, supported_regions)

