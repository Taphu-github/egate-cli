import serial
import time

class SerialCommunication:


    def __init__(self, port=None, baudrate=9600, timeout=6):
        """
        Initialize the serial communication object.
        :param port: Serial port (e.g., "COM3" or "/dev/ttyUSB0")
        :param baudrate: Communication speed (default: 9600)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def open(self):
        """
        Open the serial connection.
        """
        if self.serial_connection is None:
            try:
                self.serial_connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                print(f"Opened serial port {self.port} at {self.baudrate} baud.")
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.serial_connection = None

    def close(self):
        """
        Close the serial connection.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed.")
            self.serial_connection = None

    def write(self, data):
        """
        Write data to the serial port.
        :param data: Data to send (as a string or bytes)
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = bytes.fromhex(data) # Convert string to bytes
                self.serial_connection.write(data)
                print(f"Sent: {data}")
            except Exception as e:
                print(f"Error writing to serial port: {e}")
        else:
            print("Serial connection is not open.")

    def read(self, size=1024):
        """
        Read data from the serial port.
        :param size: Number of bytes to read (default: 1024)
        :return: The received data as a string
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.read(size)
                return data.decode()  # Convert bytes to string
            except Exception as e:
                print(f"Error reading from serial port: {e}")
                return None
        else:
            print("Serial connection is not open.")
            return None

    def read_line(self):
        """
        Read a line of data from the serial port.
        :return: The received line as a string
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline()
                return data.decode()  # Convert bytes to string
            except Exception as e:
                print(f"Error reading line from serial port: {e}")
                return None
        else:
            print("Serial connection is not open.")
            return None