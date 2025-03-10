## Import modules ##

import netmiko
import logging

from datetime import datetime
from netmiko import ConnectHandler
from getpass4 import getpass

## Logging functionality ##

#logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

## Connection method to devices ##

user = 'Enter Username Here'
password = getpass('Password: ')

with open('switch_hostnames_test.txt') as switches:
    for hostname in switches:
        Switch = {
            'device_type': 'hp_procurve',
            'host': hostname,
            'username': user,
            'password': password,
        }

        start_time = datetime.now()

        print("*** Connecting to", hostname, "***")
        net_connect = ConnectHandler(**Switch)

        wr_mem = net_connect.send_command("write memory")

        print(wr_mem)
        print("*** Configuration Saved ***")

        end_time = datetime.now()

        print('*** Total time: {} ***'.format(end_time - start_time))

        net_connect.disconnect()
