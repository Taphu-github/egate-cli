from queue import Queue
import threading
import serial

write_queue = Queue()
response_queue = Queue()
command_response_map = {}  # Maps command IDs to responses
lock = threading.Lock()

def serial_writer(ser):
    command_id = 0
    while True:
        command = write_queue.get()
        if command == "STOP":
            break
        # Add unique ID to the command
        command_id += 1
        command_with_id = f"{command}|ID:{command_id}"
        command_response_map[command_id] = None  # Initialize the map entry
        ser.write(command_with_id.encode())
        print(f"Sent: {command_with_id}")

def serial_reader(ser):
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            # Extract ID from response (assuming response includes ID)
            if "|ID:" in data:
                response, command_id = data.split("|ID:")
                command_id = int(command_id)
                with lock:
                    command_response_map[command_id] = response
                response_queue.put((command_id, response))
                print(f"Received response for Command ID {command_id}: {response}")

def main():
    # SERIAL_PORT = '/dev/ttyUSB0'
    # BAUD_RATE = 9600
    # ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser="TEST"

    writer_thread = threading.Thread(target=serial_writer, args=(ser,))
    reader_thread = threading.Thread(target=serial_reader, args=(ser,))

    writer_thread.start()
    reader_thread.start()

    # Example: Send commands
    write_queue.put("COMMAND_1")
    write_queue.put("COMMAND_2")

    # Retrieve specific responses
    while not response_queue.empty():
        cmd_id, response = response_queue.get()
        print(f"Processed response for Command ID {cmd_id}: {response}")

    write_queue.put("STOP")
    writer_thread.join()
    reader_thread.join()
    ser.close()
    print("Serial connection closed.")

main()
