import sys
import interface
myid = sys.argv[1]
region_name = 'us-west-1'
for i in range(10):
    print interface.instance_status(myid, region_name)

