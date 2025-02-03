import tkinter as tk
from tkinter import scrolledtext
import serial
import time
import asyncio
import websockets
import threading
import json
import signal
import sys
import os
import datetime

# ======================================PASSPORT READER CODES===============================================#
# Configuration for WebSocket
WEBSOCKET_URI = 'ws://127.0.0.1:90/echo'  # Replace with your WebSocket server address
# Directory to save log files
# Global variables for log files of passport reader
LOG_DIRECTORY = 'logs'
# Ensure the log directory exists
os.makedirs(LOG_DIRECTORY, exist_ok=True)

reply_log_file_path = os.path.join(LOG_DIRECTORY, 'device_status_reply.txt')  # Single file for "Reply" messages
notify_log_file_path = None  # Path for "Notify" messages, created as needed



#this method is responsible to send message to web socket
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
            {"Command": "Get", "Operand": "WebConstant", "Param": "Disconnect"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "Save"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "IDCANCEL"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceStatus"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceName"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceSerialno"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceNotConnected"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DescOfWebsocketError"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DescFailSetRFID"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DescFailSetVIZ"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "PlaceHolderCardTextInfo"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceOffLine"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceReconnected"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DescFailSendWebsocket"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "WebDescDeviceNotFound"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "WebDescRequireRestartSvc"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "WebDescAskForSupport"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "WebDescRequireReconnect"},
            {"Command": "Get", "Operand": "WebConstant", "Param": "DeviceConnected"}
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
                {"Command": "Get", "Operand": "DeviceType"},
                {"Command": "Get", "Operand": "DeviceSerialNo"},
                {"Command": "Get", "Operand": "VersionInfo"}
            ]
        }

        try:
            # Check if the WebSocket is still open before sending
            if websocket.open:
                await websocket.send(json.dumps(request))
            else:
                print("WebSocket connection is not open. Skipping status request.")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed error while sending device status: {e}")
            break  # Exit loop and retry connection in the main handler
        except Exception as e:
            print(f"Unexpected error while sending device status: {e}")
        
        await asyncio.sleep(5)  # Send request every 5 seconds

# Graceful shutdown event
shutdown_event = asyncio.Event()

# WebSocket communication
async def websocket_handler():
    while not shutdown_event.is_set():
        try:
            #max_size=10*1024*1024
            async with websockets.connect(WEBSOCKET_URI, max_size=10*1024*1024) as websocket:

                await get_web_constants(websocket)

                 # Set up periodic device status requests
                asyncio.create_task(get_device_status(websocket))

                while not shutdown_event.is_set():
                    try:
                        # Wait indefinitely for a message
                        message = await websocket.recv()
                        handle_websocket_message(message)
                        
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed.")
                        break


        except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as e:
            print(f"WebSocket connection closed: {e}")
        except Exception as e:
            print(f"WebSocket error: {e}")

        await asyncio.sleep(1)  # Wait before retrying connection

# # WebSocket communication
# async def websocket_handler():
#     while not shutdown_event.is_set():
#         try:
#             #max_size=10*1024*1024
#             async with websockets.connect(WEBSOCKET_URI, max_size=10*1024*1024) as websocket:

#                 await get_web_constants(websocket)




def handle_websocket_message(message):
    global notify_log_file_path

    try:
        json_msg = json.loads(message)
        print("DOC TYPE", json_msg.get('Type'))

        # Determine the type of the message
        message_type = json_msg.get('Type')
        
        # save log files
        if message_type == 'Reply':
            # Write to the reply log file
            if reply_log_file_path:
                with open(reply_log_file_path, 'w') as log_file:
                    log_file.write(f"{json.dumps(json_msg, indent=4)}\n")
            else:
                print("Reply log file path is not set.")
                
        elif message_type == 'Notify':
            # Generate timestamp for the filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            notify_log_file_path = os.path.join(LOG_DIRECTORY, f"log_{timestamp}.txt")

            # Save the message to a new file
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
                hex_command = COMMANDS['OPEN FOR ENTRY']
                response = send_command_and_listen(hex_command)
                print(f"Open gate command response: {response}")

            else:
                print("Passport scan data received, but necessary fields are missing.")
                
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


# =================== EGATE CONTROLLER CODES ====================================#
# Configuration for Serial
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
TIMEOUT = 6




# Command mapping (hex values for different commands)
COMMANDS = {
    'OPEN FOR ENTRY': 'AA 00 01 02 00 02 08 00 00 00 00 00 00 00 00 0D',
    'OPEN FOR EXIT': 'AA 00 01 02 00 02 08 00 03 00 00 00 00 00 00 10',
    'CLOSE FOR ENTRY': 'AA 00 01 02 00 02 08 00 02 00 00 00 00 00 00 0F',
    'CLOSE FOR EXIT': 'AA 00 01 02 00 02 08 00 05 00 00 00 00 00 00 12',
    'OPEN ALWAYS FOR ENTRY': 'AA 00 01 02 00 02 08 00 01 00 00 00 00 00 00 0E',
    'OPEN ALWAYS FOR EXIT': 'AA 00 01 02 00 02 08 00 04 00 00 00 00 00 00 11'
}


# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Function to send a hex command and receive a response over serial
def send_command(hex_command):
    try:
        command_bytes = bytes.fromhex(hex_command)
        ser.write(command_bytes)
        time.sleep(1)
        response = ser.read(ser.in_waiting)
        print("response", response)
        return response.decode()
    except serial.SerialException as e:
        print(f"Error during communication: {e}")
        return None

# Function to send a hex command and listen for a response
def send_command_and_listen(hex_command):
    try:
        command_bytes = bytes.fromhex(hex_command)
        ser.write(command_bytes)

        start_time = time.time()
        response = bytearray()
        while time.time() - start_time < TIMEOUT:
            if ser.in_waiting > 0:
                response.extend(ser.read(ser.in_waiting))
            time.sleep(0.1)
        
        return response
    except serial.SerialException as e:
        print(f"Error during communication: {e}")
        return None


# GUI Application
class GateControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("eGate Controller")
        self.geometry("600x400")

        # Create command selection dropdown
        self.command_var = tk.StringVar(value=list(COMMANDS.keys())[0])
        self.command_menu = tk.OptionMenu(self, self.command_var, *COMMANDS.keys())
        self.command_menu.pack(pady=10)

        # Send button
        self.send_button = tk.Button(self, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=5)

        # Response display area
        self.response_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=70)
        self.response_area.pack(pady=10)

    def send_command(self):
        command = self.command_var.get()
        hex_command = COMMANDS.get(command)
        if hex_command:
            response = send_command_and_listen(hex_command)
            self.response_area.delete(1.0, tk.END)
            self.response_area.insert(tk.END, f"Sending command: {command} ({hex_command})\n")
            self.response_area.insert(tk.END, f"Response: {response}\n")




# Run WebSocket handler in a separate thread
def start_websocket_loop():
    asyncio.run(websocket_handler())

# Function to handle clean shutdown
def signal_handler(sig, frame):
    print('Shutting down...')
    shutdown_event.set()  # Signal the WebSocket handler to stop
    app.quit()  # Close the GUI application
    
    
# Main loop
if __name__ == "__main__":
    app = GateControllerApp()
    
    # Register the signal handler for termination signals
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signal
    
    # Start WebSocket handling in a separate thread
    websocket_thread = threading.Thread(target=start_websocket_loop, daemon=True)
    websocket_thread.start()

    app.mainloop()

    # Close the serial connection when the application exits
    if ser:
        ser.close()
        print("Serial connection closed.")

