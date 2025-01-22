import json
import time

with open("command_mapping.json", "r") as file:
    COMMANDS = json.load(file)

if not COMMANDS:
    print("Please Check If the 'commands.json' file exists")
    exit()


def get_command(command_name):
    for command in COMMANDS:
        if command.get("command") and command.get("command")==command_name:
            return command
    return {}

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

def create_command(command_structure,addr_to):
    commands=[]
    cid1=command_structure.get("cid1")
    cid2=command_structure.get("cid2")
    data_length=command_structure.get("data_length")
    multiple=command_structure.get("multiple")
    data=command_structure.get("data")
    structure=command_structure.get("structure")
    addr_src="01"


    if not cid1 or not cid2 or not data_length:
        print("The Structure of the command is wrong as cid1 or cid2 or datalenght doesn't exist")

    if multiple and len(multiple)!=0:
        #build for multiple structure
        mutiple_command=[ "AA 00 "+addr_src+" "+cid1+" "+cid2+" "+addr_to+" "+data_length+" "+cmd for cmd in multiple]
        commands.extend(mutiple_command)

    elif data:
        #build if data is already present
        data_command="AA 00"+" "+addr_src+" "+cid1+" "+cid2+" "+addr_to+" "+data_length+" "+data
        commands.append(data_command)

    elif structure:
        #build the command for structure
        pass

    return [cm + " " + generate_checksum(cm) for cm in commands]

def get_and_create_command(command_name,addr_to):
    command_structure=get_command(command_name)
    if not command_structure:
        print("There is no command structure which matches '{}'".format(command_name))

    commands=create_command(command_structure=command_structure, addr_to=addr_to)
    if not commands:
        print("Something went wrong in the generation of your command")

    return commands

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

def get_semi_complete_command(command_structure, addr_to):
    commands=[]
    cid1=command_structure.get("cid1")
    cid2=command_structure.get("cid2")
    data_length=command_structure.get("data_length")
    multiple=command_structure.get("multiple")
    data=command_structure.get("data")
    structure=command_structure.get("structure")
    addr_src="00"

    datas=[
            structure.get("data_0"),
            structure.get("data_1"),
            structure.get("data_2"),
            structure.get("data_3"),
            structure.get("data_4"),
            structure.get("data_5"),
            structure.get("data_6"),
            structure.get("data_7"),

            ]

    command_str="AA 00 01 "+cid1+" "+cid2+" "+addr_to+" "+data_length

    return command_str, datas


def chunk_bytearray(byte_array, chunk_size=16):
    """
    Breaks a byte array into chunks of `chunk_size` bytes each.

    :param byte_array: The byte array to be chunked.
    :param chunk_size: The size of each chunk in bytes.
    :return: List of byte array chunks.
    """
    print(byte_array)
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
    print(f"Command: {command_arr}")

    for com in command_arr:
        command_bytes = bytes.fromhex(com)
        ser.write(command_bytes)

    #     start_time = time.time()
    #     response = bytearray()

    #     while time.time() - start_time < 6:
    #         if ser.in_waiting > 0:
    #             response.extend(ser.read(ser.in_waiting))

    #     response_chunks = chunk_bytearray(response)

    #     if not response_chunks:

    #         print("There has been a problem with the command")
    #         print("The command is ", com)
    #     else:
    #         all_response.extend(response_chunks)

    # print(f"Response: {str(all_response)}")
    # return all_response
