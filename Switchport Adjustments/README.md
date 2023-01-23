Script will iterate through switch and perform the following:

Check for VLAN 999 config & create VLAN 999 if not present. Then set this as the primary VLAN <br />
Check for down interfaces that are enabled on 3-6, 40-52 <br />
Check for down interfaces that are already disabled on 40-52 <br />
If ports are in ap_int_down and remaining_int_down, change to VLAN 999 untagged and disable <br />
If ports are in disabled_ports and don't have VLAN 999 untagged, apply VLAN 999 untagged <br />
Set WAN port to VLAN 999 untagged <br />
Set floor ports 7-40 to VLAN 999 untagged if not already <br />
