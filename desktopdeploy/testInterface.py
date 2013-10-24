import interface
company_name = 'lala'
supported_regions = ['us-west-1','us-west-2','us-east-1']
interface.make_company(company_name, supported_regions) 
id1 = interface.get_instance_id('us-west-1', 'm1.small', 'ubuntu12.04',company_name, 'ybro', '1534a48d06f8cd7322a1c0725ae437826324dc8f')
#interface.terminate_instance(id ,region) 
print id1

