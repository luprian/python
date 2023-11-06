from datetime import datetime
from getpass4 import getpass
from netmiko import ConnectHandler

user = 'brodie.dickerson_adm'
password = getpass('Password: ')

with open('switch_hostnames_test.txt') as switches:
    for hostname in switches:
        Switch = {
            'device_type': 'cisco_ios',
            'host': hostname,
            'username': 'USERNAME IN HERE',
            'password': password,
        }

        start_time = datetime.now()

        print("*** Connecting to", hostname, "***")
        net_connect = ConnectHandler(**Switch)
        net_connect.config_mode()
        change_password = net_connect.send_command("username DUMMY USERNAME privilege 15 secret 0 ++PUT PASSWORD IN HERE+++")
        print("*** Password on", hostname, "changed ***")

        end_time = datetime.now()

        print('*** Total time: {} ***'.format(end_time - start_time))

    net_connect.disconnect()
