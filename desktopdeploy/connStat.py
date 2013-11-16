import sys
import interface
myid = sys.argv[1]
region_name = sys.argv[2]
uname = sys.argv[3]
supported_regions = ['us-west-1','us-west-2','us-east-1']
for i in range(10):
    print interface.instance_status(myid, region_name, uname)

