import connect
import nx


def print_box(string):
    print "***************************************"
    print string
    print "***************************************"

#print "testing query()"
#connect.query()

#print_box("testing query(regions='us-west-1')")
#connect.terminate_all()
#connect.query(regions='us-west-1')

#connect.terminate_instance('i-16d7054d')

#print_box("starting an instance") 
#(instance_id,region) = connect.launch_instance()


#instance_id = 'i-f46db0af'
#connect.run_at_instance('i-2e449b75','ls  ~/.NX_setup_complete',wait=False)
#connect.run_at_instance('i-2e449b75','ls  ~/.NX_setup_complete',verbose=2)
#(stdout,stderr) = connect.run_at('df -h','i-2e449b75',verbose=2)


#connect.run_at('prepareAWSNX3p5.sh','i-2e449b75',input_type='script',verbose=0)
#if (nx.working('i-2e449b75')):
#    nx.run_nxcommand('userlist','i-2e449b75',region='us-west-1',verbose=2)
#connect.run_command_at_instance(instance_id,'ls -altr /tmp')


#connect.terminate_instance('i-ead50fb1')
#connect.query(regions=region)
#connect.query(instances=instance_id,regions=region)

#print_box("testing terminating an instance")
#connect.terminate_instance(instance_id)

#connect.query(regions='us-west-1')
#print_box("testing stopping an instance")
#connect.stop_instance("i-ba5f89e1")

if True:
    instanceId = 'i-2e449b75'
    uname = 'yaser'
    pswd = 'hahaha' 
    print_box('getting userlist')
    print nx.user_list(instanceId,verbose=0)
        
    print_box('delete a user')
    print nx.del_user(uname,instanceId,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(instanceId,verbose=0)
        
    print_box('add a user')
    print nx.add_user(uname,pswd,instanceId,verbose=0)
    
    print_box('add another user')
    print nx.add_user('johndoe','aslkjd',instanceId,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(instanceId,verbose=0)

    print_box('delete all users')
    nx.del_all_users(instanceId,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(instanceId,verbose=0)
    
    

