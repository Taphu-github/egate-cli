import serial
import time


SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
TIMEOUT = 6

# SERIAL_PORT = '/dev/cu.usbserial-BG004IEK'
# BAUD_RATE = 9600
# TIMEOUT = 6

# //EXTERNAL ALARM
# AA 00 01 02 00 02 08 02 01 00 00 00 00 00 00 10

# //CANCEL EXTERNAL ALARM
# AA 00 01 02 00 02 08 02 00 00 00 00 00 00 00 0F

# COMMANDS = {
#     'OPEN FOR ENTRY': 'AA00010200020800000000000000000D',
#     'OPEN FOR EXIT': 'AA000102000208000300000000000010',
#     'CLOSE FOR ENTRY': 'AA00010200020800020000000000000F',
#     'CLOSE FOR EXIT': 'AA000102000208000500000000000012',
#     'OPEN ALWAYS FOR ENTRY': 'AA00010200020800010000000000000E',
#     'OPEN ALWAYS FOR EXIT': 'AA000102000208000400000000000011',
#     'SEND ALARM': 'AA000102000208020100000000000010',
#     'STOP ALARM': 'AA00010200020802000000000000000F'
# }
COMMANDS = {
            'OPEN FOR ENTRY': 'AA00010200020800000000000000000D',
            'OPEN FOR EXIT': 'AA000102000208000300000000000010',
            'CLOSE FOR ENTRY': 'AA00010200020800020000000000000F',
            'CLOSE FOR EXIT': 'AA000102000208000500000000000012',
            'OPEN ALWAYS FOR ENTRY': 'AA00010200020800010000000000000E',
            'OPEN ALWAYS FOR EXIT': 'AA000102000208000400000000000011',
            'SEND ALARM': 'AA000102000208020100000000000010',
            'STOP ALARM': 'AA00010200020802000000000000000F'
        }



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

def determine_message_type(parsed_data, controller_address_range=(0x00, 0x0F)):
    """
    Determines whether the message is sent from the PC or is a response from the servo controller.

    :param parsed_data: Dictionary containing parsed message data.
    :param controller_address_range: Tuple indicating the range of addresses for the controller.
    :return: String describing the message type.
    """
    ADR_S = parsed_data['ADR_S']
    ADR_T = parsed_data['ADR_T']

    # Check if the source address is within the controller address range
    if ADR_S in range(controller_address_range[0], controller_address_range[1] + 1):
        return "Message from Controller"

    # Check if the destination address is within the controller address range
    elif ADR_T in range(controller_address_range[0], controller_address_range[1] + 1):
        return "Message to Controller"

    # If neither address is within the controller range, consider it as from/to PC
    else:
        return "Message from/to PC"


def find_response_for_sent_command(hex_command, response_chunks, cid1_match='12'):
    """
    Finds a response chunk that matches the criteria based on the hex command.

    :param hex_command: Hexadecimal string of the command.
    :param response_chunks: List of hexadecimal string chunks of the response.
    :param cid1_match: The CID1 value to match.
    :return: The matching response chunk if found, otherwise None.
    """
    ADR_T = hex_command[10:12]

    for hex_chunk in response_chunks:
        try:
            egate_response_cid1 = hex_chunk[6:8]
            if egate_response_cid1 == cid1_match:
                print("egate_code", hex_chunk)
                return hex_chunk

        except ValueError as e:
            print(f"Error parsing chunk: {e}")

    return None

# this is to handle the processing of response from egate
def handle_response_chunks(command_label, hex_command, response_chunks):


    egate_response = find_response_for_sent_command(hex_command, response_chunks)

    print("egate response", egate_response)

    if(command_label == "OPEN FOR ENTRY"):
        print("open command")


    return "hello"



# # Example usage
# byte_array = bytearray(b'\xaa\x00\x02\x12\x00\x00\x08c\x06\x00\x00\x1b\x00\x002\xd2')
# parsed_data = parse_response(byte_array)
# print(parsed_data)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# def send_command(hex_command):
#     try:
#         command_bytes = bytes.fromhex(hex_command)
#         ser.write(command_bytes)
#         time.sleep(1)
#         response = ser.read(ser.in_waiting)
#         return response.decode()
#     except serial.SerialException as e:
#         print(f"Error during communication: {e}")
#         return None

def send_command_and_listen(command_text):
    if command_text == 'SEND ALARM':
        # Send start alarm command
        start_alarm_command = COMMANDS.get('SEND ALARM')
        if start_alarm_command:
            command_bytes = bytes.fromhex(start_alarm_command)
            ser.write(command_bytes)
            print(f"Sending start alarm command: {start_alarm_command}")

        # Wait for a few seconds
        time.sleep(5)  # Adjust the sleep duration as needed

        # Send stop alarm command
        stop_alarm_command = COMMANDS.get('STOP ALARM')
        if stop_alarm_command:
            command_bytes = bytes.fromhex(stop_alarm_command)
            ser.write(command_bytes)
            print(f"Sending stop alarm command: {stop_alarm_command}")

        # No need to read response for this case
        return None

    else:
        hex_command = COMMANDS.get(command_text)
        if hex_command is None:
            print(f"Invalid command: {command_text}")
            return None

        try:
            command_bytes = bytes.fromhex(hex_command)
            ser.write(command_bytes)

            start_time = time.time()
            response = bytearray()

            while time.time() - start_time < TIMEOUT:
                if ser.in_waiting > 0:
                    response.extend(ser.read(ser.in_waiting))

                time.sleep(0.1)


            response_chunks = chunk_bytearray(response)
            handle_response_chunks(command_text, hex_command, response_chunks)

            print("chunks", response_chunks)
            return response_chunks
            # return response
        except serial.SerialException as e:
            print(f"Error during communication: {e}")
            return None


    # hex_command = COMMANDS.get(command_text)
    # if hex_command is None:
    #     print(f"Invalid command: {command_text}")
    #     return None

    # try:
    #     command_bytes = bytes.fromhex(hex_command)
    #     ser.write(command_bytes)

    #     start_time = time.time()
    #     response = bytearray()

    #     while time.time() - start_time < TIMEOUT:
    #         if ser.in_waiting > 0:
    #             response.extend(ser.read(ser.in_waiting))
    #         time.sleep(0.1)

    #     return response
    # except serial.SerialException as e:
    #     print(f"Error during communication: {e}")
    #     return None

