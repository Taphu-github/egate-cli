import time
import json
def get_mac_address():
    return "F0 A1 B4 A5 96 87"

def get_addr_to():
    return "03"

def generate_checksum(data):
    hex_pairs=data.split(" ")

    sums= 0
    for hexi in hex_pairs[1:]:
        sums+=int(hexi, 16)

    hex_val=hex(sums)
    meaningful_val_of_hex=hex_val.split("x")[1]

    if len(meaningful_val_of_hex)==1:
        return ("0"+meaningful_val_of_hex).upper()

    elif len(meaningful_val_of_hex)==2:
        return meaningful_val_of_hex.upper()

    else:
        return meaningful_val_of_hex[-2:].upper()

def convert_deci_to_hex(dec, ln):
    deci=int(dec)
    hex_val=hex(deci)
    meaningful_val_of_hex=hex_val.split("x")[1]
    return_hex=[]
    if len(meaningful_val_of_hex)==1:

        return_hex= ["0"+meaningful_val_of_hex]

    elif len(meaningful_val_of_hex)==2:
        return_hex= [meaningful_val_of_hex]

    else:
        if len(meaningful_val_of_hex)%2==0:
            return_hex= [ meaningful_val_of_hex[i:i+2] for i in range(0, len(meaningful_val_of_hex), 2)]
        else:
            hex_string=["0"+meaningful_val_of_hex[0]]
            meaningful_val_of_hex_even=meaningful_val_of_hex[1:]
            return_hex.extend(hex_string)
            return_hex.extend([ meaningful_val_of_hex_even[i:i+2] for i in range(0, len(meaningful_val_of_hex_even), 2)])

    if ln>len(return_hex):
        for i in range(ln-len(return_hex)):
            return_hex.insert(0,"00")
    elif ln<len(return_hex):
        print("lenght of return hex is much greater")

    return " ".join(return_hex)

def to_int(string):
    try:
        return int(string)
    except Exception:
        return 0

def hex_to_deci(string):
    try:
        return int(string, 16)
    except Exception:
        return 0

def chunk_bytearray(byte_array, chunk_size=16):
    """
    Breaks a byte array into chunks of `chunk_size` bytes each.

    :param byte_array: The byte array to be chunked.
    :param chunk_size: The size of each chunk in bytes.
    :return: List of byte array chunks.
    """
    chunks = [byte_array[i:i + chunk_size] for i in range(0, len(byte_array), chunk_size)]
    # Convert each chunk to a hex string
    hex_chunks = [''.join(f'{byte:02X}' for byte in chunk) for chunk in chunks]

    return hex_chunks

def get_mac_address(ser):
    command="00 01 01 01 00 00 00 00 00 00 00 00 00 00"
    command_check_sum=generate_checksum(command)
    command_hex="AA "+command+" "+command_check_sum

    command_bytes=bytes.fromhex(command_hex)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        # time.sleep(0.2)

    # if not res
    response_chunks = chunk_bytearray(response)

    if not response_chunks:
        print("There has been a problem with the command")
    # print(response_chunks)
    return response_chunks[0][9:15]

def get_device_id(ser):
    command="00 01 01 01 00 00 00 00 00 00 00 00 00 00"
    command_check_sum=generate_checksum(command)
    command_hex="AA "+command+" "+command_check_sum

    command_bytes=bytes.fromhex(command_hex)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        # time.sleep(0.2)

    # if not res
    response_chunks = chunk_bytearray(response)

    if not response_chunks:
        print("There has been a problem with the command")
    # print(response_chunks)
    return response_chunks[0][4:6]

OPTIONS_MAPPING={
        "ir_sensor_type": {
            "pnp (hi trig)": "00",
            "npn (lo trig)": "01"
        },
        "ir_logic": {
            "disabled": "00",
            "local interface": "01",
            "external for entry": "40",
            "external for exit": "80",
            "external for both": "c0"
        },
        "relay_for_passed_counter": {
            "entry": "01",
            "disabled": "00",
            "exit": "02",
            "both": "03"
        },
        "barriers_count": {
            "single": "01",
            "double": "00"
        },
        "normally_open_direction": {
            "entry": "00",
            "exit": "10"
        },
        "action_on_power_lost": {
            "none": "00",
            "closed": "01",
            "always open for entry": "02",
            "always open for exit": "03"
        },
        "gate_mode": {
            "normally closed, both card": "01",
            "normally closed, both free": "02",
            "normally closed, both reject": "03",
            "normally closed, entry card & exit free": "04",
            "normally closed, entry card & exit reject": "05",
            "normally closed, entry free & exit card": "06",
            "normally closed, entry free & exit reject": "07",
            "normally closed, entry reject & exit free": "08",
            "normally closed, entry reject & exit card": "09",
            "normally open, both free": "0A",
            "normally open, both card": "0B",
            "normally open, entry free & exit card": "0C",
            "normally open, entry card & exit reject": "0D"
        },
        "authorized_with_memory": {
            "both disabled": "00",
            "entry allowed": "01",
            "exit allowed": "02",
            "both allowed": "03"
        },
        "authorized_in_lane": {
            "on": "01",
            "off": "00"
        },
        "automatic_report_state": {
            "on": "01",
            "off": "00"
        },
        "passage_end_ir_check_at": {
            "exit": "00",
            "safety": "01"
        },
        "intrusion_alarm": {
            "none": "00",
            "alarm": "01",
            "alarm and close door": "02"
        },
        "reverse_alarm": {
            "none": "00",
            "alarm": "01",
            "alarm and close door": "02"
        },
        "tailing_alarm": {
            "none": "00",
            "alarm": "01",
            "alarm and close door": "02"
        },
        "power_on_self_check": {
            "on": "01",
            "off": "00"
        },
        "switch_options":{
            "on_trigger":{
                "None":"00"
                ,"Idle (Default State)":"01"
                ,"Open For Entry":"02"
                ,"Always Open For Entry":"03"
                ,"Close For Entry":"04"
                ,"Open For Exit":"05"
                ,"Always Open For Exit":"06"
                ,"Close For Exit":"07"
            },
            "on_release":{
                "None":"00"
                ,"Idle (Default State)":"10"
                ,"Open For Entry":"20"
                ,"Always Open For Entry":"30"
                ,"Close For Entry":"40"
                ,"Open For Exit":"50"
                ,"Always Open For Exit":"60"
                ,"Close For Exit":"70"
            },
        },
        "entrance_indicator":{
            "None":"F0"
            ,"Black(All Off)":"00"
            ,"D1":"01"
            ,"D2":"02"
            ,"D2+D1": "03"
            ,"D3":"04"
            ,"D3+D1":"05"
            ,"D3+D2":"06"
            ,"D3+D2+D1":"07"
            ,"D4":"08"
            ,"D4+D1":"09"
            ,"D4+D2":"0A"
            ,"D4+D2+D1":"0B"
            ,"D4+D3":"0C"
            ,"D4+D3+D1":"0D"
            ,"D4+D3+D2":"0E"
            ,"D4+D3+D2+D1":"0F"
        },
        "rgb_led":{
            "None":"F0"
            ,"Black(All Off)":"00"
            ,"Red":"01"
            ,"Green":"02"
            ,"Yellow(R+G)":"03"
            ,"Blue":"04"
            ,"Magenta(R+B)":"05"
            ,"Cyan(G+B)":"06"
            ,"White(R+G+B)":"07"
        },
        "relay":{
            "None":"F0"
            ,"All Opened":"00"
            ,"Relay 1 Closed":"01"
        },
        "voice_module":{
            "None":"F0"
            ,"N9200":"01"
            ,"BY-F610V1.2":"02"
            ,"BY-F610V1.3":"03"
        }

    }