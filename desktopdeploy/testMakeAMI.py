import interface
company_name = 'someCompany2'
supported_regions = ['us-west-1','us-west-2','us-east-1']
print 'making company'
interface.make_company(company_name, supported_regions) 
id1 = interface.make_AMI('us-west-1', company_name)
print 'us-west-1 ',id1
#id2 = interface.make_AMI('us-east-1', company_name)
#print 'us-east-1 ',id2
print 'removing company'
#interface.remove_company(company_name, supported_regions) 
#interface.terminate_instance(id ,region) 


