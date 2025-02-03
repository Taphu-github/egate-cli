import tkinter as tk
from tkinter import scrolledtext
import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust this to your serial port
BAUD_RATE = 9600              # Adjust this to the baud rate required by your eGate controller
TIMEOUT = 6                    # Timeout for read operations (in seconds)

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Function to send a hex command and receive a response
def send_command(hex_command):
    try:
        # Convert hex string to bytes
        command_bytes = bytes.fromhex(hex_command)
        ser.write(command_bytes)  # Send command to the eGate controller
        time.sleep(1)          # Wait for the response
        response = ser.read(ser.in_waiting)  # Read the response
        print("response", response)
        return response.decode()
    except serial.SerialException as e:
        print(f"Error during communication: {e}")
        return None

# Function to send a hex command and listen for a response
def send_command_and_listen(hex_command):
    try:
        # Convert hex string to bytes
        command_bytes = bytes.fromhex(hex_command)
        ser.write(command_bytes)  # Send command to the eGate controller

        # Listen for response or events
        start_time = time.time()
        response = bytearray()
        while time.time() - start_time < TIMEOUT:
            if ser.in_waiting > 0:
                response.extend(ser.read(ser.in_waiting))
            # You can add more sophisticated conditions here to break the loop based on expected responses
            time.sleep(0.1)  # Small delay to avoid busy waiting
        
        # Return raw response
        return response
    except serial.SerialException as e:
        print(f"Error during communication: {e}")
        return None

# Command mapping (hex values for different commands)
COMMANDS = {
    'OPEN FOR ENTRY': 'AA 00 01 02 00 02 08 00 00 00 00 00 00 00 00 0D',   # OPEN FOR ENTRY
    'OPEN FOR EXIT': 'AA 00 01 02 00 02 08 00 03 00 00 00 00 00 00 10',   # OPEN FOR EXIT
    'CLOSE FOR ENTRY': 'AA 00 01 02 00 02 08 00 02 00 00 00 00 00 00 0F',   # CLOSE FOR ENTRY
    'CLOSE FOR EXIT': 'AA 00 01 02 00 02 08 00 05 00 00 00 00 00 00 12',   # CLOSE FOR EXIT
    'OPEN ALWAYS FOR ENTRY': 'AA 00 01 02 00 02 08 00 01 00 00 00 00 00 00 0E',   # OPEN ALWAYS FOR ENTRY
    'OPEN ALWAYS FOR EXIT': 'AA 00 01 02 00 02 08 00 04 00 00 00 00 00 00 11'   # OPEN ALWAYS FOR ENTRY
}


# GUI Application
class GateControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("eGate Controller")
        self.geometry("500x400")

        # Create command selection dropdown
        self.command_var = tk.StringVar(value=list(COMMANDS.keys())[0])
        self.command_menu = tk.OptionMenu(self, self.command_var, *COMMANDS.keys())
        self.command_menu.pack(pady=10)

        # Send button
        self.send_button = tk.Button(self, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=5)

        # Response display area
        self.response_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=60)
        self.response_area.pack(pady=10)

    def send_command(self):
        command = self.command_var.get()
        hex_command = COMMANDS.get(command)
        if hex_command:
            response = send_command_and_listen(hex_command)
            self.response_area.delete(1.0, tk.END)  # Clear previous response
            self.response_area.insert(tk.END, f"Sending command: {command} ({hex_command})\n")
            self.response_area.insert(tk.END, f"Response: {response}\n")

# Main loop
if __name__ == "__main__":
    app = GateControllerApp()
    app.mainloop()

    # Close the serial connection when the application exits
    if ser:
        ser.close()
        print("Serial connection closed.")


