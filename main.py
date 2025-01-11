from utils import generate_checksum, chunk_bytearray, get_device_id, replace_values
import json
import time
import serial
from parse_response import parse

SERIAL_PORT = "COM3"
BAUD_RATE = 38400
TIMEOUT = 0.5
ADR_T="00"

with open("commands.json", "r") as file:
    data = json.load(file)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# ADR_T=get_device_id(ser)


com=[
"AA 00 01 01 11 09 08 00 00 00 00 00 00 00 00 24",
"AA 00 01 01 11 09 08 00 01 00 00 00 00 00 00 25",
"AA 00 01 01 11 09 08 00 02 00 00 00 00 00 00 26",
"AA 00 01 01 11 09 08 00 03 00 00 00 00 00 00 27" ,
"AA 00 01 01 11 09 08 00 04 00 00 00 00 00 00 28" ,
"AA 00 01 01 11 09 08 01 00 00 00 00 00 00 00 25" ,
"AA 00 01 01 11 09 08 01 01 00 00 00 00 00 00 26" ,
"AA 00 01 01 11 09 08 01 02 00 00 00 00 00 00 27" ,
"AA 00 01 01 11 09 08 01 03 00 00 00 00 00 00 28" ,
"AA 00 01 01 11 09 08 01 04 00 00 00 00 00 00 29" ,
"AA 00 01 01 11 09 08 02 00 00 00 00 00 00 00 26" ,
"AA 00 01 01 11 09 08 02 01 00 00 00 00 00 00 27" ,
"AA 00 01 01 11 09 08 02 02 00 00 00 00 00 00 28" ,
"AA 00 01 01 11 09 08 02 03 00 00 00 00 00 00 29" ,
"AA 00 01 01 11 09 08 02 04 00 00 00 00 00 00 2A" ,
"AA 00 01 01 11 09 08 03 00 00 00 00 00 00 00 27" ,
"AA 00 01 01 11 09 08 03 01 00 00 00 00 00 00 28" ,
"AA 00 01 01 11 09 08 03 02 00 00 00 00 00 00 29" ,
"AA 00 01 01 11 09 08 03 03 00 00 00 00 00 00 2A" ,
"AA 00 01 01 11 09 08 03 04 00 00 00 00 00 00 2B" ,
"AA 00 01 01 11 09 08 04 00 00 00 00 00 00 00 28" ,
"AA 00 01 01 11 09 08 04 01 00 00 00 00 00 00 29" ,
"AA 00 01 01 11 09 08 04 02 00 00 00 00 00 00 2A" ,
"AA 00 01 01 11 09 08 04 03 00 00 00 00 00 00 2B" ,
"AA 00 01 01 11 09 08 04 04 00 00 00 00 00 00 2C" ,
"AA 00 01 01 11 09 08 05 00 00 00 00 00 00 00 29" ,
"AA 00 01 01 11 09 08 05 01 00 00 00 00 00 00 2A" ,
"AA 00 01 01 11 09 08 05 02 00 00 00 00 00 00 2B" ,
"AA 00 01 01 11 09 08 05 03 00 00 00 00 00 00 2C" ,
"AA 00 01 01 11 09 08 05 04 00 00 00 00 00 00 2D" ,
"AA 00 01 01 11 09 08 06 00 00 00 00 00 00 00 2A" ,
"AA 00 01 01 11 09 08 06 01 00 00 00 00 00 00 2B" ,
"AA 00 01 01 11 09 08 06 02 00 00 00 00 00 00 2C" ,
"AA 00 01 01 11 09 08 06 03 00 00 00 00 00 00 2D" ,
"AA 00 01 01 11 09 08 06 04 00 00 00 00 00 00 2E" ,
"AA 00 01 01 11 09 08 07 00 00 00 00 00 00 00 2B" ,
"AA 00 01 01 11 09 08 07 01 00 00 00 00 00 00 2C" ,
"AA 00 01 01 11 09 08 07 02 00 00 00 00 00 00 2D" ,
"AA 00 01 01 11 09 08 07 03 00 00 00 00 00 00 2E" ,
"AA 00 01 01 11 09 08 07 04 00 00 00 00 00 00 2F" ,
]
res=[]
for co in com:
    cm=bytes.fromhex(co)
    ser.write(cm)
    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < TIMEOUT:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        # time.sleep(0.2)

    response_chunks = chunk_bytearray(response)
    res.extend(response_chunks)

for r in res:
    parse(r)


# # checksum=generate_checksum("AA 00 01 02 00 00 08 00 00 00 00 00 00 00 00")
# checksum=generate_checksum(data["CHECKING ONLINE UNIT"])

# print(checksum)
# # command_hex="AA 00 01 02 00 00 08 00 00 00 00 00 00 00 00"+" "+checksum
# command_hex = data["CHECKING ONLINE UNIT"]+" "+checksum
# print("command", command_hex)
# command_bytes=bytes.fromhex(command_hex)
# ser.write(command_bytes)

# start_time = time.time()
# response = bytearray()

# while time.time() - start_time < TIMEOUT:
#     if ser.in_waiting > 0:
#         response.extend(ser.read(ser.in_waiting))
#     # time.sleep(0.2)

# response_chunks = chunk_bytearray(response)
# print("Received", response_chunks)
# print(response_chunks[0][4:6])



ser.close()




