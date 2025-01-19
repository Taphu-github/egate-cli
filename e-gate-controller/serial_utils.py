from aioserial import AioSerial
import serial.tools.list_ports
import time
from command_utils import generate_checksum

SERIAL_PORT = "COM3"
BAUD_RATE = 38400
TIMEOUT = 0.5

def get_port():
    ports=serial.tools.list_ports.comports()
    serial_ports=[]

    for port in ports:
        serial_ports.append(port.device)

    return serial_ports[0] if len(serial_ports)!=0 else None

def connect_to_serial():
    try:
        ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Could'nt connect to {SERIAL_PORT} at {BAUD_RATE} baud.")
        return None

    return ser

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

def run_command(ser, command):

    command_bytes = bytes.fromhex(command)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 0.2:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))

    response_chunks = chunk_bytearray(response)

    if len(response_chunks)==0:
        return None
    print(response_chunks)
    return response_chunks

def get_addr_to(ser):
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
    arranged_response = [
        response_chunks[0][i : i + 2]
        for i in range(0, (len(response_chunks[0])), 2)
    ]
    # print(arranged_response)
    if not response_chunks:
        print("There has been a problem with the command")
    # print(arranged_response[2])
    return arranged_response[2]


