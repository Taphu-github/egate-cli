from gate_controller import send_command_and_listen
import asyncio
import json
import os
import websockets
import datetime
from mrz.checker.td3 import TD3CodeChecker
from websocket_server import broadcast_message


# Configuration for WebSocket
WEBSOCKET_URI = 'ws://127.0.0.1:90/echo'  # Replace with your WebSocket server address
LOG_DIRECTORY = 'logs'
os.makedirs(LOG_DIRECTORY, exist_ok=True)

reply_log_file_path = os.path.join(LOG_DIRECTORY, 'device_status_reply.txt')  # Single file for "Reply" messages
notify_log_file_path = None  # Path for "Notify" messages, created as needed

# allowed_passport = "G102040"
allowed_passport = "S0A00J24"


# Graceful shutdown event
shutdown_event = asyncio.Event()

# This method is responsible for sending JSON data to WebSocket
async def send_json(websocket, json_data):
    try:
        if websocket is not None:
            await websocket.send(json.dumps(json_data))
    except Exception as e:
        print(f"Error sending JSON data: {e}")

# Function to get web constants
async def get_web_constants(websocket):
    request = {
        "Type": "Request",
        "Commands": [
            {"Command": "Get", "Operand": "WebConstant", "Param": "CardRecogSystem"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "Connect"},
            # Add other constants here
        ]
    }
    await send_json(websocket, request)

# Function to get device status periodically
async def get_device_status(websocket):
    while not shutdown_event.is_set():
        request = {
            "Type": "Request",
            "Commands": [
                {"Command": "Get", "Operand": "OnLineStatus"},
                {"Command": "Get", "Operand": "DeviceName"},
                # Add other commands here
            ]
        }
        try:
            if websocket.open:
                await websocket.send(json.dumps(request))
            # else:
                # print("WebSocket connection is not open. Skipping status request.")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed error while sending device status: {e}")
            break
        except Exception as e:
            print(f"Unexpected error while sending device status: {e}")
        await asyncio.sleep(5)  # Send request every 5 seconds



def verifyPassport(json_msg):
    message_type = json_msg.get('Type')
    operand_type = json_msg.get('Operand')

    if operand_type == 'CardContentText':
        param = json_msg.get('Param', {})

        # Extract MRZ fields from the 'Param' dictionary
        mrz1 = param.get('MRZ1', '')
        mrz2 = param.get('MRZ2', '')

        # Combine MRZ1 and MRZ2 if necessary
        mrz_combined = mrz1+'\n'+mrz2

        # Use the mrz package to parse the MRZ data
        try:
           
            
            mrz_td3 = (mrz_combined)

            td3_check = TD3CodeChecker(mrz_td3, check_expiry=True)

            if not td3_check:
                return False

            fields = td3_check.fields()

            if fields and fields.document_number == allowed_passport:
                return True
            else:
                return False

            # return passport_number
        except Exception as e:
            print("Error parsing MRZ data:", e)
            return False

        


# Handle WebSocket messages
async def handle_websocket_message(message):
    global notify_log_file_path
    try:
        json_msg = json.loads(message)
        # print("DOC TYPE", json_msg.get('Type'))

        message_type = json_msg.get('Type')

        if message_type == 'Reply':
            if reply_log_file_path:
                with open(reply_log_file_path, 'w') as log_file:
                    log_file.write(f"{json.dumps(json_msg, indent=4)}\n")
            else:
                print("Reply log file path is not set.")

        elif message_type == 'Notify':
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            notify_log_file_path = os.path.join(LOG_DIRECTORY, f"log_{timestamp}.txt")

            with open(notify_log_file_path, 'w') as log_file:
                log_file.write(f"{json.dumps(json_msg, indent=4)}\n")
            print(f"Created new log file: {notify_log_file_path}")

        if json_msg.get('Type') == 'Notify' and json_msg.get('Command') == 'Save':
            # Extract parameters
            param = json_msg.get('Param', {})
            
            # Print extracted parameters for debugging
            # print(f"Extracted parameters: {param}")

            # Check if the passport information is present
            if 'CARD_MAINID' in param and 'CARD_NAME' in param:
                # For example, you could check specific fields or just proceed based on the presence of data
                print("Passport scan data received.")
                
                # Here, you can define your own condition for when to open the gate

                # For instance, let's say we open the gate for all valid passport scans

                print("Condition met. Opening gate for entry.")

                if verifyPassport(json_msg):

                    # response = send_command_and_listen("OPEN FOR ENTRY")

                    await broadcast_message(
                        event_type="passport_scanned",
                        document_type="passport",
                        status="scanned",
                        details={
                            "name": "John Doe",
                            "nationality": "USA"
                        }
                    )
                    
                    # print(f"Open gate command response: {response}")
                    # await broadcast_message("HELLO FROM SERVER")

                else:
                    response = send_command_and_listen("SEND ALARM")

            else:
                print("Passport scan data received, but necessary fields are missing.")
                await broadcast_message(
                    event_type="invalid_document",
                    document_type="passport",
                    status="invalid",
                    details={
                        "error": "Invalid MRZ format",
                        "nationality": "Unknown"
                    }
                )


        # # Check if the message type is 'Notify' and the command is 'Save'
        # if json_msg.get('Type') == 'Notify' and json_msg.get('Command') == 'Save':
        #     # Extract parameters
        #     param = json_msg.get('Param', {})
            
        #     # Check if the necessary passport scan data is present
        #     if 'CARD_MAINID' in param and 'CARD_NAME' in param:
        #         print("Passport scan data received.")
                
        #         # Example condition to open gate for entry
        #         # You can define your own condition based on the data you receive
        #         if param.get('CARD_TYPE') == 1:
        #             print("Condition met. Opening gate for entry.")
        #             hex_command = COMMANDS['OPEN FOR ENTRY']
        #             response = send_command_and_listen(hex_command)
        #             print(f"Open gate command response: {response}")
                    
        #         else:
        #             print("Passport scan data received, but condition not met.")
        
        

    except json.JSONDecodeError:
        print(f"WebSocket parse error: {message}")

# WebSocket communication handler
async def websocket_handler():
    while not shutdown_event.is_set():
        try:
            async with websockets.connect(WEBSOCKET_URI, max_size=10*1024*1024) as websocket:
                await get_web_constants(websocket)
                asyncio.create_task(get_device_status(websocket))

                while not shutdown_event.is_set():
                    try:
                        message = await websocket.recv()
                        await handle_websocket_message(message)
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed.")
                        break
        except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as e:
            print(f"WebSocket connection closed: {e}")
        except Exception as e:
            print(f"WebSocket error 1: {e}")
        await asyncio.sleep(5)  # Wait before retrying connection
