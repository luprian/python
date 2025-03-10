from netmiko import ConnectHandler
from getpass4 import getpass
from datetime import datetime
import logging

# Enable debug output for Netmiko
logging.basicConfig(filename='NDC-deployment.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


user = input('Username: ')
password = getpass('Password: ')

with open('switch_hostnames.txt') as switches:
    for hostname in switches:
        Switch = {
            'device_type': 'fortinet',
            'host': hostname,
            'username': user,
            'password': password,
        }

        start_time = datetime.now()

        print("*** Connecting to", hostname, "***")
        net_connect = ConnectHandler(**Switch)
        net_connect.config_mode()
        
        config_commands = [
            'config user group',
                'edit "Network-Switch Operators"',
                    'set group-type firewall',
                    'set authtimeout 0',
                    'set member "RADIUS_Servers"',
                'next',
                'edit "Network-Switch Admins"',
                    'set group-type firewall',
                    'set authtimeout 0',
                    'set member "RADIUS_Servers"',
                'next',
                'edit "Network-Backup Admins"',
                    'set group-type firewall',
                    'set authtimeout 0',
                    'set member "RADIUS_Servers"',
                'next',
                'end',
            'config system accprofile',
                'edit "backup_admin"',
                    'set admingrp read',
                    'set exec-alias-grp read',
                    'set loggrp read',
                    'set mntgrp read',
                    'set netgrp read',
                    'set pktmongrp read',
                    'set routegrp read',
                    'set swcoregrp read',
                    'set swmonguardgrp read',
                    'set sysgrp read',
                    'set utilgrp read',
                'next',
                'edit "read_only_operator"',
                    'set admingrp read',
                    'set exec-alias-grp read',
                    'set loggrp read',
                    'set mntgrp read',
                    'set netgrp read',
                    'set pktmongrp read',
                    'set routegrp read',
                    'set swcoregrp read',
                    'set swmonguardgrp read',
                    'set sysgrp read',
                    'set utilgrp read',
                'next',
                'end',
            'config system admin',
                'edit "RADIUS_Admins"',
                    'set remote-auth enable',
                    'set accprofile "super_admin"',
                    'set wildcard enable',
                    'set remote-group "Network-Switch Admins"',
                    'set accprofile-override enable',
                'next',
                'edit "RADIUS_Operators"',
                    'set remote-auth enable',
                    'set trusthost1 10.255.2.0 255.255.255.0',
                    'set trusthost2 10.200.0.0 255.255.255.0',
                    'set trusthost3 10.200.128.0 255.255.255.0',
                    'set accprofile "read_only_operator"',
                    'set wildcard enable',
                    'set remote-group "Network-Switch Operators"',
                    'set accprofile-override enable',
                'next',
                'edit "RADIUS_Backup_Admins"',
                    'set remote-auth enable',
                    'set trusthost1 172.28.0.13 255.255.255.255',
                    'set trusthost2 172.28.128.13 255.255.255.255',
                    'set trusthost3 10.200.0.0 255.255.255.0',
                    'set trusthost4 10.200.128.0 255.255.255.0',
                    'set accprofile "backup_admin"',
                    'set wildcard enable',
                    'set remote-group "Network-Backup Admins"',
                    'set accprofile-override enable',
                'next',
                'end',
]

        print("*** Sending commands ***")
        net_connect.send_config_set(config_commands)
        print("*** Completed", hostname, "***")
        
        end_time = datetime.now()
        print('*** Total time: {} ***'.format(end_time - start_time))
        
        net_connect.disconnect()