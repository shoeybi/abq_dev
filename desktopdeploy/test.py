import aws
import connect
import nx

def print_box(string):
    print '***************************************'
    print string
    print '***************************************'


test_aws        = False
test_connection = False
test_nx         = True

region = 'us-west-1'
if False:
    print_box("query(regions='us-west-1')")
    aws.query(regions=region)

if test_aws:
    print_box('testing query()')
    aws.query()
    
    print_box('starting an instance') 
    instance_id = aws.launch(instance_type = 't1.micro', 
                             ami = 'ami-fe002cbb', 
                             key_name = 'abaqual_key', 
                             region = region )
    
    print_box('testing the query at the specific instance')
    aws.query(instance_id,region)
    
    print_box('wait for the instance to start')
    if aws.instance_is_running(instance_id,region):
        print_box('get the query and show its running')
        aws.query(instance_id,region)

    print_box('stop the instance')
    aws.stop(instance_id,region)
    
    print_box('wait for the instance to stop')
    if aws.instance_is_at_state('stopped',instance_id,region):
        print_box('print the state of instance')
        print aws.state(instance_id,region)
    
    print_box('start the instance')
    aws.start(instance_id,region)

    print_box('wait for the instance to start')
    if aws.instance_is_running(instance_id,region):
        print_box('print the state of instance')
        print aws.state(instance_id,region)

    print_box('terminate the instance')
    aws.terminate(instance_id,region)
    
    print_box("query(regions='us-west-1')")
    aws.query(regions=region)


instance_id_up = 'i-2e449b75'
if test_connection:
    myconn = connect.Connection(instance_id_up,region)
    for i in range(20):
        print '------------------------------------------------',i
        out_lines = myconn.run_at('ls',wait_for_output=True,print_stdout=False)
    myconn.disconnect()
    for i in range(20):
        print '------------------------------------------------',i
        out_lines = myconn.run_at('ls',wait_for_output=True,print_stdout=False)
    myconn.disconnect()

if test_nx:
    myconn = connect.Connection(instance_id_up,region)
    uname1 = 'yaser'
    pswd1 = 'hahaha' 
    uname2 = 'mohammad'
    pswd2 = 'haqwe_haha'
    uname3 = 'abbas'
    pswd3 = 'asdlkjasd' 
    uname4 = 'ahmad'
    pswd4 = 'asdlkjaasdasd' 

    print_box('getting userlist')
    print nx.user_list(myconn,verbose=0)
        
    print_box('delete a user')
    print nx.del_user(uname4,myconn,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(myconn,verbose=0)
        
    print_box('add a user')
    print nx.add_user(uname1,pswd1,myconn,verbose=0)
    
    print_box('add another user')
    print nx.add_user(uname2,pswd2,myconn,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(myconn,verbose=0)
    
    print_box('delete all users')
    nx.del_all_users(myconn,verbose=0)

    print_box('add another user')
    print nx.add_user(uname4,pswd4,myconn,verbose=0)
    
    print_box('getting userlist')
    print nx.user_list(myconn,verbose=0)

    myconn.disconnect()
