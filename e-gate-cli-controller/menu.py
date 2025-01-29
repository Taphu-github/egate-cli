import asyncio
import threading
import time
from aioserial import AioSerial
from commands_and_variables import (
    COMMANDS, run_command, get_device_id, chunk_bytearray, shared_message
)
from input_ouput_menu import input_output_menu_straight_command, input_output_menu_set_commands
from status_control_menu import status_control_menu_straight_command, status_control_menu_set_commands
from parse_response import parse
from tcp_server import start_tcp_server


async def menu(ser, addr_to):
    """Menu for device configuration."""
    command_categories = {
        "control parameters": [],
        "device information": [],
        "status and control": [],
        "input and output": [],
    }

    for command in COMMANDS:
        family = command.get("family")
        if not family:
            print(f"Warning: Missing 'family' key in command: {command.get('id')}")
            continue

        if family in command_categories:
            command_categories[family].append(command)
        else:
            print(f"Warning: Unexpected 'family' value '{family}' in command JSON.")

    while True:
        print("\n---------------------- E-GATE DEVICE CONFIGURATION ---------------------")
        print("1: Input and Output\n2: Status and Control\n0: Quit")
        option_var = input("Enter your choice: ").strip()

        if option_var == '1':
            command, command_name = input_and_output_menu(command_categories["input and output"], addr_to)
            run_command(ser=ser, command_arr=command)

        elif option_var == '2':
            command, command_name = status_and_control_menu(command_categories["status and control"], addr_to)
            run_command(ser=ser, command_arr=command)

        elif option_var == '0':
            print("Exiting configuration menu...")
            exit(0)
        else:
            print("Invalid option. Try again.")


def input_and_output_menu(commands, addr_to):
    """Handles Input and Output Menu selection."""
    return handle_menu_selection(commands, addr_to, "Input and Output", input_output_menu_straight_command, input_output_menu_set_commands)


def status_and_control_menu(commands, addr_to):
    """Handles Status and Control Menu selection."""
    return handle_menu_selection(commands, addr_to, "Status and Control", status_control_menu_straight_command, status_control_menu_set_commands)


def handle_menu_selection(commands, addr_to, mode_name, straight_func, set_func):
    """Generalized function to handle menu selections."""
    print(f"\nYou are in the {mode_name.upper()} Mode")
    command_name, command_type = print_options(commands)

    if not command_name or not command_type:
        return None, None

    if command_type == "straight":
        generated_commands = straight_func(command_name=command_name, addr_to=addr_to)
    elif command_type == "set":
        generated_commands = set_func(command_name=command_name, addr_to=addr_to)
    else:
        print(f"Error: Unknown command type '{command_type}'")
        return None, None

    return ["".join(generated_commands[0].split(" "))], command_name


def print_options(commands):
    """Displays command options and returns selected command details."""
    for command in commands:
        id_ = command.get("id")
        com = command.get("command")

        if id_ is None or com is None:
            print(f"Warning: Missing 'id' or 'command' in: {command}")
            continue

        print(f"Enter '{id_}' for '{com}'")

    opt = input("Select an option: ").strip()

    for command in commands:
        if str(command.get("id")) == opt:
            return command.get("command"), command.get("type")

    print("Invalid selection. Please try again.")
    return None, None


def main_thread(ser, addr_to):
    """Runs the main menu asynchronously."""
    asyncio.run(menu(ser, addr_to))


def read_continuous(ser):
    """Continuously reads responses from the serial connection."""
    temp_buffer = bytearray()

    while True:
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting)
            process_response(response, temp_buffer)


def process_response(response, temp_buffer):
    """Processes serial responses and handles buffering."""
    start_time = time.perf_counter()

    if response:
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.6f} seconds")

        while not shared_message.empty():
            shared_message.get()
        shared_message.put(response)

        if len(response) == 16:
            response_chunks = chunk_bytearray(response)
            for res in response_chunks:
                parse(res)
        else:
            temp_buffer.extend(response)

        if len(temp_buffer) == 16:
            response_chunks = chunk_bytearray(temp_buffer)
            for res in response_chunks:
                parse(res)
            temp_buffer.clear()


def start_threads():
    """Initializes and starts all necessary threads."""
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 38400
    TIMEOUT = 6
    shutdown_event = asyncio.Event()

    try:
        ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        addr_to = get_device_id(ser=ser)

        # Thread Definitions
        thread1 = threading.Thread(target=main_thread, args=(ser, addr_to,), daemon=True)
        thread2 = threading.Thread(target=read_continuous, args=(ser,), daemon=True)
        tcp_thread = threading.Thread(target=start_tcp_server, args=(shutdown_event,), daemon=True)

        # Start Threads
        thread1.start()
        thread2.start()
        tcp_thread.start()

        # Keep Main Thread Alive
        thread1.join()
        thread2.join()
        tcp_thread.join()

    except Exception as e:
        print(f"Error occurred: {e}")
        shutdown_event.set()


# Start the program
if __name__ == "__main__":
    start_threads()
