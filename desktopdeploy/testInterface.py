import interface
company_name = 'lala'
supported_regions = ['us-west-1','us-west-2','us-east-1']
interface.make_company(company_name, supported_regions) 
id1 = interface.get_instance_id('us-west-1', 'm1.small', 'ubuntu12.04',company_name, 'yaser2', 'yaser2')
#interface.terminate_instance(id ,region) 
print id1

