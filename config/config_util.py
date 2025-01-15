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
  "switch_options": {
    "on_trigger": {
      "none": "00",
      "idle (default state)": "01",
      "open for entry": "02",
      "always open for entry": "03",
      "close for entry": "04",
      "open for exit": "05",
      "always open for exit": "06",
      "close for exit": "07"
    },
    "on_release": {
      "none": "00",
      "idle (default state)": "10",
      "open for entry": "20",
      "always open for entry": "30",
      "close for entry": "40",
      "open for exit": "50",
      "always open for exit": "60",
      "close for exit": "70"
    }
  },
  "entrance_indicator": {
    "none": "F0",
    "black(all off)": "00",
    "d1": "01",
    "d2": "02",
    "d2+d1": "03",
    "d3": "04",
    "d3+d1": "05",
    "d3+d2": "06",
    "d3+d2+d1": "07",
    "d4": "08",
    "d4+d1": "09",
    "d4+d2": "0A",
    "d4+d2+d1": "0B",
    "d4+d3": "0C",
    "d4+d3+d1": "0D",
    "d4+d3+d2": "0E",
    "d4+d3+d2+d1": "0F"
  },
  "rgb_led": {
    "none": "F0",
    "black(all off)": "00",
    "red": "01",
    "green": "02",
    "yellow(r+g)": "03",
    "blue": "04",
    "magenta(r+b)": "05",
    "cyan(g+b)": "06",
    "white(r+g+b)": "07"
  },
  "relay": {
    "none": "F0",
    "all opened": "00",
    "relay 1 closed": "01"
  },
  "voice_module": {
    "none": "F0",
    "n9200": "01",
    "by-f610v1.2": "02",
    "by-f610v1.3": "03"
  }
}
