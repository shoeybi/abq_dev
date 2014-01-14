import interface
import threading

software_list=['openfoam']
instance_id = 'i-3fb4d81f'
region_name = 'us-east-1'
users 	    = ['ykhalighi']

interface.install_software(software_list, users, instance_id, region_name)


