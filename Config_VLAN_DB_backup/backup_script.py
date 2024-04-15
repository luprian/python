from netmiko import ConnectHandler
from getpass4 import getpass
import datetime
import logging

# Enable debug output for Netmiko
# logging.basicConfig(level=logging.DEBUG)

user = 'USERNAME'
password = getpass('Password: ')

with open('switch_hostnames.txt') as switches:
    for hostname in switches:
        Switch = {
            'device_type': 'cisco_ios',
            'host': hostname,
            'username': user,
            'password': password,
        }

        # Define TFTP server information
        tftp_server = "10.255.2.9"  # Change this to your TFTP server IP address
        filename_prefix = "backup"

        # Establish SSH connection to the switch
        print("Connecting to the switch", hostname)
        try:
            net_connect = ConnectHandler(**Switch)
        except Exception as e:
            print(f"Failed to connect to the device: {e}")
            exit()

        # Entering enable mode if required
        net_connect.enable()

        # Get the hostname of the switch
        hostname = net_connect.find_prompt().replace('#', '')

        # Backup running configuration via TFTP
        print("Backing up running configuration via TFTP...")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        tftp_command = f"copy running-config tftp://{tftp_server}/{filename_prefix}-{hostname}-{timestamp}-running_config.txt"
        output = net_connect.send_command(
            command_string=tftp_command,
            expect_string=r"Address or name of remote host",
            strip_prompt=False,
            strip_command=False
        )
        output += net_connect.send_command(
            command_string="\n",
            expect_string=r"Destination filename",
            strip_prompt=False,
            strip_command=False
        )
        output += net_connect.send_command(
            command_string="\n",
            expect_string=r"#",
            strip_prompt=False,
            strip_command=False
        )
#        print(output)
        print("Running configuration backup via TFTP complete.")

        # Backup VLAN database (vlan.dat) via TFTP
        print("Backing up VLAN database (vlan.dat) via TFTP...")
        net_connect.enable()
        tftp_command = f"copy flash:vlan.dat tftp://{tftp_server}/{filename_prefix}-{hostname}-{timestamp}-vlan.dat"
        output = net_connect.send_command(
            command_string=tftp_command,
            expect_string=r"Address or name of remote host",
            strip_prompt=False,
            strip_command=False
        )
        output += net_connect.send_command(
            command_string="\n",
            expect_string=r"Destination filename",
            strip_prompt=False,
            strip_command=False
        )
        output += net_connect.send_command(
            command_string="\n",
            expect_string=r"#",
            strip_prompt=False,
            strip_command=False
        )
#        print(output)
        print(hostname, "VLAN database backup via TFTP complete.")

        # Disconnect SSH session
        net_connect.disconnect()
        print("Disconnected from the switch.")
