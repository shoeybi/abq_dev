def print_box(string):
    print "***************************************"
    print string
    print "***************************************"

import connect
import re

#print "testing query()"
#connect.query()

#print_box("testing query(regions='us-west-1')")
#connect.terminate_all()
#connect.query(regions='us-west-1')

#connect.terminate_instance('i-16d7054d')
#connect.terminate_instance('i-6cd50737')
#connect.terminate_instance('i-8cd507d7')
#connect.terminate_instance('i-60d2013b')

#print_box("starting an instance") 
#(instance_id,region) = connect.launch_instance()
#connect.query(instances=instance_id,regions=region)
#instance_id = 'i-f46db0af'
connect.run_at_instance('i-2e449b75','ls  ~/.NX_setup_complete',wait=False)
#connect.run_at_instance('i-2e449b75','ls  ~/.NX_setup_complete2',verbose=2)
(stdout,stderr) = connect.run_at_instance('i-2e449b75','sudo /usr/NX/bin/nxserver --status',wait=False)
#for line in stdout.readlines():
#    if re.search("^NX>\s110\sNX\sServer\sis\srunning\.$",line):
#        print line,
connect.run_at_instance('i-2e449b75','prepareAWSNX3p5.sh',wait=True)
#connect.run_command_at_instance(instance_id,'ls -altr /tmp')
#connect.query(instances=instance_id,regions=region)

#print_box("testing terminating an instance")
#connect.terminate_instance(instance_id)

#connect.query(regions='us-west-1')
#print_box("testing stopping an instance")
#connect.stop_instance("i-ba5f89e1")


