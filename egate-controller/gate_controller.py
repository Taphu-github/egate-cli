import serial
import time
from parse_response import get_parsed_response, parse
import queue

# SERIAL_PORT = '/dev/ttyUSB0'
# BAUD_RATE = 38400
# TIMEOUT = 6

SERIAL_PORT = '/dev/cu.usbserial-BG004IEK'
BAUD_RATE = 38400
TIMEOUT = 4

SOA = b'\xaa'

# Global variables
awaiting_response = None  # Stores the expected response type
response_queue = queue.Queue()  # Thread-safe queue for passing responses

COMMANDS = {
            'GATE_STATUS': 'AA000102000208FF000000000000000C',
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
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=None)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# def send_command_and_listen(command_text):
#     global awaiting_response
#     if command_text == 'SEND ALARM':
#         # Send start alarm command
#         start_alarm_command = COMMANDS.get('SEND ALARM')
#         if start_alarm_command:
#             command_bytes = bytes.fromhex(start_alarm_command)
#             ser.write(command_bytes)
#             print(f"Sending start alarm command: {start_alarm_command}")

#         # Wait for a few seconds
#         time.sleep(5)  # Adjust the sleep duration as needed

#         # Send stop alarm command
#         stop_alarm_command = COMMANDS.get('STOP ALARM')
#         if stop_alarm_command:
#             command_bytes = bytes.fromhex(stop_alarm_command)
#             ser.write(command_bytes)
#             print(f"Sending stop alarm command: {stop_alarm_command}")

#         # No need to read response for this case
#         return None

#     else:
#         hex_command = COMMANDS.get(command_text)
#         if hex_command is None:
#             print(f"Invalid command: {command_text}")
#             return None

#         try:
#             command_bytes = bytes.fromhex(hex_command)
#             ser.write(command_bytes)

#             awaiting_response = command_text  # Set flag to track response

#             start_time = time.time()
#             responses = []

#             while time.time() - start_time < TIMEOUT:
#                 try:
#                     # Wait for a response with timeout
#                     response = response_queue.get(timeout=0.5)

#                     if isinstance(response, dict):  # Ensure response is a dictionary
#                         responses.append(response)
#                     else:
#                         print("Warning: Received non-dictionary response, ignoring.")

#                     # print(f"Received Parsed Response: {response}")
#                     # Exit loop when "gate closing" message is received

#                 except queue.Empty:
#                     continue  # Keep waiting if queue is empty

#             awaiting_response = None  # Reset flag

#             return responses  # Return last received response
        
#         except serial.SerialException as e:
#             print(f"Error during communication: {e}")
#             return None

def send_command_and_listen(command_text):
    global awaiting_response
    
    # Handle alarm-related commands
    if command_text == 'SEND ALARM':
        start_alarm_command = COMMANDS.get('SEND ALARM')
        if start_alarm_command:
            command_bytes = bytes.fromhex(start_alarm_command)
            ser.write(command_bytes)
            print(f"Sending start alarm command: {start_alarm_command}")
        else:
            print("Error: 'SEND ALARM' command not found in COMMANDS")
            return {"status": "error", "message": "'SEND ALARM' command not found"}

        time.sleep(5)  # Adjust the sleep duration as needed

        stop_alarm_command = COMMANDS.get('STOP ALARM')
        if stop_alarm_command:
            command_bytes = bytes.fromhex(stop_alarm_command)
            ser.write(command_bytes)
            print(f"Sending stop alarm command: {stop_alarm_command}")
        else:
            print("Error: 'STOP ALARM' command not found in COMMANDS")
            return {"status": "error", "message": "'STOP ALARM' command not found"}

        return {"status": "success", "message": "Alarm started and stopped successfully"}

    else:
        # Handle other commands
        hex_command = COMMANDS.get(command_text)
        if hex_command is None:
            print(f"Invalid command: '{command_text}' not found in COMMANDS")
            return {"status": "error", "message": f"Invalid command: '{command_text}'"}

        try:
            # Send the command
            command_bytes = bytes.fromhex(hex_command)
            ser.write(command_bytes)

            awaiting_response = command_text  # Set flag to track response

            start_time = time.time()
            responses = []
            response_time_out = TIMEOUT
            if(command_text == "GATE_STATUS"):
                response_time_out = 0.2

            # Wait for response or timeout
            while time.time() - start_time < response_time_out:
                try:
                    response = response_queue.get(timeout=0.5)

                    if isinstance(response, dict):  # Ensure response is a dictionary
                        responses.append(response)
                    else:
                        print("Warning: Received non-dictionary response, ignoring.")

                except queue.Empty:
                    continue  # Keep waiting if queue is empty

            awaiting_response = None  # Reset flag

            # Check if responses were collected
            if responses:
                return {"status": "success", "responses": responses}
            else:
                print("Error: No valid responses received")
                return {"status": "error", "message": "No valid responses received"}

        except serial.SerialException as e:
            print(f"Error during serial communication: {e}")
            return {"status": "error", "message": f"Error during serial communication: {e}"}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"status": "error", "message": f"Unexpected error: {e}"}

def read_continuous():
    """Continuously reads responses from the serial connection."""
    temp_buffer = bytearray()

    while True:
        response = ser.read(16)  # Wait for exactly 16 bytes
        print("Received RESPONSE: ", response)
        if len(response) == 16:
            process_response(response, temp_buffer)
        else:
            print("Incomplete packet received, possible timeout.")
        
        # if ser.in_waiting > 0:
        #     response = ser.read(ser.in_waiting)
        #     # print(f"Received RESPONSE: {response}")
        #     process_response(response, temp_buffer)

def process_response(response, temp_buffer):
    """Processes serial responses and handles buffering."""
    global awaiting_response

    start_time = time.perf_counter()

    # if response:
    #     temp_buffer.extend(response)

    #     while SOA in temp_buffer:  # Process messages with SOA (0xAA)
    #         index = temp_buffer.index(SOA)
    #         if len(temp_buffer) - index >= 16:
    #             message_chunk = temp_buffer[index:index + 16]
    #             del temp_buffer[:index + 16]  # Remove processed data

    #             parsed_message = parse(message_chunk)  # Parse the message
    #             print(f"Parsed Message: {parsed_message}")

    #             if awaiting_response:  # Only send if a command is waiting for response
    #                 response_queue.put(parsed_message)  # Send to main thread


    if response:
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        # print(f"Execution time: {execution_time:.6f} seconds")

        # while not shared_message.empty():
        #     shared_message.get()
        # shared_message.put(response)

        if len(response) == 16:
            response_chunks = chunk_bytearray(response)
            for res in response_chunks:
                # get_parsed_response(res)
                print(f"UNPARSED", res)
                response_from_gate = get_parsed_response(res)
                print(f"RESPONSE PARSED", response_from_gate)
                if awaiting_response:
                    response_queue.put(response_from_gate)
        else:
            temp_buffer.extend(response)

        if len(temp_buffer) == 16:
            response_chunks = chunk_bytearray(temp_buffer)
            for res in response_chunks:
                response_from_gate = get_parsed_response(res)
                if awaiting_response:
                    response_queue.put(response_from_gate)
            temp_buffer.clear()

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
