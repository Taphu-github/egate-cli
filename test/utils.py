import time

def get_command(command_name):
    pass

def chunk_bytearray(byte_array, chunk_size=16):
    # print(byte_array)
    chunks = [
        byte_array[i : i + chunk_size] for i in range(0, len(byte_array), chunk_size)
    ]
    # Convert each chunk to a hex string
    hex_chunks = ["".join(f"{byte:02X}" for byte in chunk) for chunk in chunks]

    return hex_chunks
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

#AA 00 01 01 11 02 08 00 03 00 00 00 00 00 00 20
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

#AA 00 01 01 11 02 08 00 03 00 00 00 00 00 00 20
def get_max_passage_time(ser):
    command = "00 01 01 11 02 08 00 03 00 00 00 00 00 00"
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
    arranged_response = [
        response_chunks[0][i : i + 2]
        for i in range(0, (len(response_chunks[0])), 2)
    ]
    # print(arranged_response)
    if not response_chunks:
        print("There has been a problem with the command")


    return int(arranged_response[10],16)