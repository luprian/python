Script will iterate through switch and perform the following:

## Check for VLAN 999 config & create VLAN 999 if not present. Then set this as the primary VLAN ##
## Check for down interfaces that are enabled on 3-6, 40-52 ##
## Check for down interfaces that are already disabled on 40-52 ##
## If ports are in ap_int_down and remaining_int_down, change to VLAN 999 untagged and disable ##
## If ports are in disabled_ports and don't have VLAN 999 untagged, apply VLAN 999 untagged ##
## Set WAN port to VLAN 999 untagged ###
## Set floor ports 7-40 to VLAN 999 untagged if not already ##
