import interface
import threading

software_list=['octave']
instance_id = 'i-558fe175'
region_name = 'us-east-1'
users 	    = ['ykhalighi']
os 	    = 'dummy' ;

interface.install_software(software_list, users, os, instance_id, region_name)

