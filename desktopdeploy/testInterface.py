import interface
company_name = 'myCompany'
region       = 'us-west-1'
interface.make_company(company_name, region) 
id = interface.get_instance_id(region, 'm1.small', 'ubuntu12.04',company_name, 'yaser2', 'yaser2')
#interface.terminate_instance(id ,region) 
print id
