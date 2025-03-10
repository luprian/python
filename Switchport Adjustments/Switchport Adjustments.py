## Import modules ##

import netmiko
import logging

from datetime import datetime
from netmiko import ConnectHandler
from getpass4 import getpass

## Logging functionality - uncomment when required ##

#logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

## Connection method to devices ##

user = '### PUT A USER NAME IN HERE ###'
password = getpass('Password: ')

with open('switch_hostnames_test.txt') as switches:
    for hostname in switches:
        Switch = {
            'device_type': 'hp_procurve',
            'host': hostname,
            'username': user,
            'password': password,
            'global_delay_factor': 2,
        }

        start_time = datetime.now()

        print("*** Connecting to", hostname, "***")
        net_connect = ConnectHandler(**Switch)
        show_int_brief = net_connect.send_command("show int brief", use_textfsm=True)
        template = 'hp_procurve_show_vlans_int_XX_detail.textfsm'

## Miscelanneous global variables ##

        show_vlan = net_connect.send_command("show vlans", use_textfsm=True)
        show_int_brief = net_connect.send_command("show int brief", use_textfsm=True)

        create_vlan_commands = ['vlan 999',
                                'name Default',
                                'exit',
                                'primary-vlan 999']

## List to append items to ##

        vlan_999 = []
        ap_int_down = []
        remaining_int_down = []
        access_ports = []
        disabled_ports =[]
        wan_port = [1]

## Check for VLAN 999 config & create VLAN 999 if not present ##

        for vlan in show_vlan:
            vlan_id = vlan['vlan_id']
            if int(vlan_id) == 999:
                vlan_999.append(vlan_id)

        if '999' in vlan_999:
            print('*** VLAN 999 exists ***')
        else:
            print("*** VLAN 999 doesn't exist ***")
            print("*** Creating Default VLAN 999 ***")
            net_connect.send_config_set(create_vlan_commands)

## Check for down interfaces that are enabled on 3-6, 40-52 ##

        for item in show_int_brief:
            if item['status'] == 'Down' and item['enabled'] == 'Yes':
                port = item['port']
                if (3 <= int(port) <= 6):
                    ap_int_down.append(item['port'])

        for item in show_int_brief:
            if item['status'] == 'Down' and item['enabled'] == 'Yes':
                port = item['port']
                if (38 <= int(port) <= 52):
                    remaining_int_down.append(item['port'])

## Check for down interfaces that are already disabled on 40-52 ##

        for item in show_int_brief:
            if item['enabled'] == 'No':
                port = item['port']
                if (40 <= int(port) <= 52):
                    disabled_ports.append(item['port'])

## Add floor ports between 7-40 into list ##

        for item in show_int_brief:
            port = item['port']
            if (7 <= int(port) <= 40):
                access_ports.append(item['port'])

## Check if list is empty ##

        if not ap_int_down:
            print('*** No AP ports in list to be disabled ***')
        if not remaining_int_down:
            print('*** No Infrastructure ports to be disabled ***')
        if not disabled_ports:
            print('*** No disabled ports between 40-52 to add to list ***')

## If ports are in ap_int_down and remaining_int_down, change to VLAN 999 untagged and disable ##

        for ap_port in ap_int_down:
            net_connect.config_mode()
            check_config_mode = net_connect.check_config_mode()
            send_command_disable_port = net_connect.send_command('interface ' + ap_port + ' disable')
#            print(send_command_disable_port)
            print("*** Port", ap_port, "disabled ****")

        for remaining_port in remaining_int_down:
            net_connect.config_mode()
            check_config_mode = net_connect.check_config_mode()
            send_command_dummy_vlan = net_connect.send_command('vlan 999 untagged ' + remaining_port)
            send_command_disable_port = net_connect.send_command('interface ' + remaining_port + ' disable')
#            print(send_command_dummy_vlan)
#            print(send_command_disable_port)
            print("*** Port", remaining_port, "disabled & dummy VLAN applied ****")

## If ports are in disabled_ports and don't have VLAN 999 untagged, apply VLAN 999 untagged ##

        for interface in disabled_ports:
            show_vlan_ports_detail = net_connect.send_command("show vlans ports " + str(interface) + " detail", use_textfsm=True, textfsm_template=template)
            for vlan_id in show_vlan_ports_detail:
                if vlan_id['vlan_id'] != '999' and vlan_id['mode'] == 'Untagged':
                    net_connect.config_mode()
                    check_config_mode = net_connect.check_config_mode()
                    set_vlan_untagged = net_connect.send_command("vlan 999 untagged " + str(interface))
                    print("*** Already disabled interface", interface, "changed to VLAN 999 untagged ***")

## Set WAN port to VLAN 999 untagged ###

        for interface in wan_port:
            show_vlan_ports_detail = net_connect.send_command("show vlans ports " + str(interface) + " detail",
                                                                  use_textfsm=True, textfsm_template=template)
            for vlan_id in show_vlan_ports_detail:
                if vlan_id['vlan_id'] == '999' and vlan_id['mode'] == 'Untagged':
                    print("*** VLAN 999 already untagged on port 1 ***")
                if vlan_id['vlan_id'] != '999' and vlan_id['mode'] == 'Untagged':
                    print("*** VLAN 999 not untagged on port 1 ***")
                    net_connect.config_mode()
                    check_config_mode = net_connect.check_config_mode()
                    set_vlan_untagged = net_connect.send_command("vlan 999 untagged " + str(interface))
                    print("*** Port", interface, "changed to VLAN 999 untagged ***")

## Set floor ports 7-40 to VLAN 999 untagged ##

        for interface in access_ports:
            show_vlan_ports_detail = net_connect.send_command("show vlans ports " + str(interface) + " detail",
                                                                  use_textfsm=True, textfsm_template=template)
            for vlan_id in show_vlan_ports_detail:
                if vlan_id['vlan_id'] == '999' and vlan_id['mode'] == 'Untagged':
                    print("*** VLAN 999 already untagged on port", interface, " ***")
                if vlan_id['vlan_id'] != '999' and vlan_id['mode'] == 'Untagged':
                    print("*** VLAN 999 not untagged on port", interface, " ***")
                    net_connect.config_mode()
                    check_config_mode = net_connect.check_config_mode()
                    set_vlan_untagged = net_connect.send_command("vlan 999 untagged " + str(interface))
                    print("*** Port", interface, "changed to VLAN 999 untagged ***")

        end_time = datetime.now()

        print('*** Script on', hostname, 'has completed ***',)
        print('*** Total time: {} ***'.format(end_time - start_time))

    net_connect.disconnect()
