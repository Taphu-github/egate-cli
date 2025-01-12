from config_util import get_mac_address, get_addr_to, generate_checksum

def set_device_address(new_device_addr, addr_to):
    mac_address=get_mac_address()
    command="00 01 01 05 "+addr_to+" 07 "+new_device_addr+" "+mac_address+ " 00"
    checksum= generate_checksum(command)

    command="AA "+command+" "+checksum
    print(command)

def set_device_group_zone_power_on_delay(group, zone, power_on_delay, addr_to):
    command="00 01 01 0A "+addr_to+" 08 00 "+group+ " "+ zone+ " 00 "+power_on_delay+" 00 00 00"
    checksum= generate_checksum(command)

    command="AA "+command+" "+checksum
    print(command)

def set_device_information_config(json_list):
    addr_to=get_addr_to()
    new_device_address=json_list.get("device_address") or "03"
    group=json_list.get("device_group") or "01"
    zone=json_list.get("zone") or "01"
    power_on_delay=json_list.get("power_on_delay") or "00"
    set_device_address(new_device_addr=new_device_address, addr_to=addr_to)
    set_device_group_zone_power_on_delay(group=group, zone=zone, power_on_delay=power_on_delay, addr_to=addr_to)


