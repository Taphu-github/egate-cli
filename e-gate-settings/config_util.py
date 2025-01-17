import time
import asyncio

def validate_command(command, command_name):
    commad_arr=command.split(" ")
    if len(commad_arr)!=16:
        print(f"the {command_name} command is incomplete")

    for com in commad_arr:
        try:
            int(com, 16)
        except Exception as e:
            print(f"the {command_name} has consists of non-hexadecimal value ")

def generate_checksum(data: str) -> str:
    """
    Generate a checksum for a given space-separated hexadecimal string.

    Args:
        data (str): A string of space-separated hexadecimal pairs (e.g., "12 AB 34").

    Returns:
        str: A two-character hexadecimal checksum in uppercase.

    Raises:
        ValueError: If the input contains invalid hexadecimal pairs.
    """
    try:
        hex_pairs = data.split(" ")
        # Convert each hex pair (skipping the first) to an integer and sum them
        total_sum = sum(int(hexi, 16) for hexi in hex_pairs[1:])
    except ValueError as e:
        raise ValueError(f"Invalid hexadecimal input: {data}") from e

    # Get the last two characters of the hex representation
    return f"{total_sum & 0xFF:02X}"


def convert_deci_to_hex(dec: int, ln: int) -> str:
    """
    Convert a decimal number to a hexadecimal string with specified length.

    Args:
        dec (int): Decimal number to convert.
        ln (int): Desired number of two-character hex pairs in the output.

    Returns:
        str: Space-separated hexadecimal string padded to the desired length.

    Raises:
        ValueError: If `ln` is less than the required length for the hex representation.
    """
    try:
        if dec<0:
            print("NEGATIVE NUMBER IS NOT ALLOWED")
            raise ValueError

        # Convert decimal to hexadecimal and remove the '0x' prefix
        hex_val = f"{int(dec):X}"

        # Ensure hex representation has an even number of characters
        if len(hex_val) % 2 != 0:
            hex_val = "0" + hex_val

        # Split into pairs of two characters
        hex_pairs = [hex_val[i:i + 2] for i in range(0, len(hex_val), 2)]

        # Check and adjust length
        if ln > len(hex_pairs):
            # Prepend "00" to pad to the desired length
            hex_pairs = ["00"] * (ln - len(hex_pairs)) + hex_pairs
        elif ln < len(hex_pairs):
            raise ValueError("Specified length is less than the required length for the hex value.")

        return " ".join(hex_pairs)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input: {dec}, {ln}") from e


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
    chunks = [
        byte_array[i : i + chunk_size] for i in range(0, len(byte_array), chunk_size)
    ]
    # Convert each chunk to a hex string
    hex_chunks = ["".join(f"{byte:02X}" for byte in chunk) for chunk in chunks]

    return hex_chunks


def get_mac_address(ser):
    command = "00 01 01 01 00 00 00 00 00 00 00 00 00 00"

    command_check_sum = generate_checksum(command)
    command_hex = "AA " + command + " " + command_check_sum

    command_bytes = bytes.fromhex(command_hex)
    # print(command_hex)
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
    # "AA 00 02 11 01 00 08 A1 02 F0 A1 B4 A5 96 87 C6"
    arranged_response = [response_chunks[0][i : i + 2] for i in range(0, 32, 2)]
    # print(arranged_response)
    mac_address = " ".join(arranged_response[9:15])
    # print(mac_address)
    return mac_address


def get_device_id(ser):
    command = "00 01 01 01 00 00 00 00 00 00 00 00 00 00"
    command_check_sum = generate_checksum(command)
    command_hex = "AA " + command + " " + command_check_sum

    command_bytes = bytes.fromhex(command_hex)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        # time.sleep(0.2)

    # if not res
    response_chunks = chunk_bytearray(response)
    "AA 00 02 11 01 00 08 A102F0A1B4A59687C6"
    arranged_response = [
        response_chunks[0][i : i + 2]
        for i in range(0, (len(response_chunks[0])), 2)
    ]
    # print(arranged_response)
    if not response_chunks:
        print("There has been a problem with the command")
    print(arranged_response[2])
    return arranged_response[2]


async def run_command(ser, command_arr):
    all_response = []

    for com in command_arr:
        command_bytes = bytes.fromhex(com)
        ser.write(command_bytes)

        start_time = time.time()
        response = bytearray()

        while time.time() - start_time < 0.05:
            if ser.in_waiting > 0:
                response.extend(ser.read(ser.in_waiting))

        response_chunks = chunk_bytearray(response)

        if not response_chunks:

            print("There has been a problem with the command")
            print("The command is ", com)
        else:
            all_response.extend(response_chunks)

    return all_response


OPTIONS_MAPPING = {
    "ir_sensor_type": {"pnp (hi trig)": "00", "npn (lo trig)": "01"},
    "ir_logic": {
        "disabled": "00",
        "local interface": "01",
        "external for entry": "40",
        "external for exit": "80",
        "external for both": "c0",
    },
    "relay_for_passed_counter": {
        "entry": "01",
        "disabled": "00",
        "exit": "02",
        "both": "03",
    },
    "barriers_count": {"single": "01", "double": "00"},
    "normally_open_direction": {"entry": "00", "exit": "10"},
    "action_on_power_lost": {
        "none": "00",
        "closed": "01",
        "always open for entry": "02",
        "always open for exit": "03",
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
        "normally open, entry card & exit reject": "0D",
    },
    "authorized_with_memory": {
        "both disabled": "00",
        "entry allowed": "01",
        "exit allowed": "02",
        "both allowed": "03",
    },
    "authorized_in_lane": {"on": "01", "off": "00"},
    "automatic_report_state": {"on": "01", "off": "00"},
    "passage_end_ir_check_at": {"exit": "00", "safety": "01"},
    "intrusion_alarm": {"none": "00", "alarm": "01", "alarm and close door": "02"},
    "reverse_alarm": {"none": "00", "alarm": "01", "alarm and close door": "02"},
    "tailing_alarm": {"none": "00", "alarm": "01", "alarm and close door": "02"},
    "power_on_self_check": {"on": "01", "off": "00"},
    "switch_options": {
        "on_trigger": {
            "none": "00",
            "idle (default state)": "01",
            "open for entry": "02",
            "always open for entry": "03",
            "close for entry": "04",
            "open for exit": "05",
            "always open for exit": "06",
            "close for exit": "07",
        },
        "on_release": {
            "none": "00",
            "idle (default state)": "10",
            "open for entry": "20",
            "always open for entry": "30",
            "close for entry": "40",
            "open for exit": "50",
            "always open for exit": "60",
            "close for exit": "70",
        },
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
        "d4+d3+d2+d1": "0F",
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
        "white(r+g+b)": "07",
    },
    "relay": {"none": "F0", "all opened": "00", "relay 1 closed": "01"},
    "voice_module": {
        "none": "F0",
        "n9200": "01",
        "by-f610v1.2": "02",
        "by-f610v1.3": "03",
    },
}
