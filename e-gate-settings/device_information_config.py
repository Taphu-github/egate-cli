from config_util import generate_checksum, convert_deci_to_hex

def set_device_address(new_device_addr, addr_to, mac_address):
    command="00 01 01 05 "+addr_to+" 07 "+new_device_addr+" "+mac_address+ " 00"
    checksum= generate_checksum(command)

    command="AA "+command+" "+checksum
    return command

def set_device_group_zone_power_on_delay(group, zone, power_on_delay, addr_to):
    group=convert_deci_to_hex(int(group), 1)
    zone=convert_deci_to_hex(int(zone), 1)
    power_on_delay=convert_deci_to_hex(int(power_on_delay), 1)
    command="00 01 01 0A "+addr_to+" 08 00 "+group+ " "+ zone+ " 00 "+power_on_delay+" 00 00 00"
    checksum= generate_checksum(command)

    command="AA "+command+" "+checksum
    return command

def set_device_information_config(json_list, addr_to, mac_address):
    new_device_address=json_list.get("device_address") or "03"
    group=json_list.get("device_group") or "01"
    zone=json_list.get("zone") or "01"
    power_on_delay=json_list.get("power_on_delay") or "00"
    com1=set_device_address(new_device_addr=new_device_address, addr_to=addr_to, mac_address=mac_address)

    com2=set_device_group_zone_power_on_delay(group=group, zone=zone, power_on_delay=power_on_delay, addr_to=addr_to)
    return [com1, com2]


