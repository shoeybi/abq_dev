import interface
company_name = 'kaka'
supported_regions = ['us-west-1','us-west-2','us-east-1']
interface.make_company(company_name, supported_regions) 
id1 = interface.get_instance_id('us-west-1', 'm1.small', 'ubuntu12.04',company_name, 'ykhalighi', 'a676e45cc256155eb294bc491c8727d2380183fb')
#interface.terminate_instance(id ,region) 
print id1

