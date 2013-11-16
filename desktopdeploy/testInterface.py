import interface
import threading
company_name = 'kaka'
supported_regions = ['us-west-1','us-west-2','us-east-1']
interface.make_company(company_name, supported_regions)
region_name = 'us-west-1'; 
id1 = interface.get_instance_id(region_name, 'm1.small', 'ubuntu12.04',company_name)[0]
userDic    = {'ykhalighi':( '4c9e3d9fd64bcd070af7177e130139e65046eacd', True),
              'mammad':( 'akjshdkjashdkjas', False) }

thread     = threading.Thread(target = interface.add_users,
                              args = (userDic, id1, region_name) )
thread.start()

print id1


