import json
# from device_information_menu import
import asyncio
import serial
from aioserial import AioSerial
from commands_and_variables import COMMANDS, run_command, get_device_id
from input_ouput_menu import input_output_menu_straight_command, input_output_menu_set_commands
from status_control_menu import status_control_menu_straight_command, status_control_menu_set_commands


async def menu(ser):
    # addr_to="02"
    status_and_control_commands=[]
    input_and_output_commands=[]
    control_parameters_commands=[]
    device_information_commands=[]

    addr_to=get_device_id(ser=ser)

    for command in COMMANDS:
        if not command.get("family"):
            id=command.get("id")
            print("There is family key missing in '{id}'")
        if command.get("family")=="control parameters":
            control_parameters_commands.append(command)
        elif command.get("family")=="device information":
            device_information_commands.append(command)
        elif command.get("family")=="status and control":
            status_and_control_commands.append(command)
        elif command.get("family")=="input and output":
            input_and_output_commands.append(command)
        else:
            print("key exits but there is a command json with different value for family key")
    exit_condition=True

    while exit_condition:
        print("----------------------E GATE DEVICE CONFIGURATION---------------------")
        print("**********************************************************************")
        print("Enter to select an option:\n'1' for Input and Output\n'2' for Status and Control\n'0' to Quit\n")
        option_var=str(input("Value: "))
        if option_var== '1':
            command, command_name=input_and_output_menu(input_and_output_commands, addr_to)
            res=await run_command(ser=ser, command_arr=command)

        elif option_var== '2':
            command, command_name=status_and_control_menu(status_and_control_commands, addr_to)
            res=await run_command(ser=ser, command_arr=command)
        elif option_var== '0':
            exit_condition=False
            exit(0)
        else :
            pass

        if command_name=="Get Voltage" and res:
            formatted_response=[res[0][i:i+2] for i in range(0,32,2)]
            psv=int("".join(formatted_response[11:13]), 16)
            bv=int("".join(formatted_response[13:15]), 16)
            print(f"Power Supply Voltage: {psv}")
            print(f"Battery Voltage: {bv}")
        elif command_name=="Refresh Get Passed Counter" and res:
            formatted_response=[res[0][i:i+2] for i in range(0,32,2)]
            entry_counter=int("".join(formatted_response[9:12]), 16)
            exit_counter=int("".join(formatted_response[12:15]), 16)
            print(f"Entry Counter: {entry_counter}")
            print(f"Exit Countyer: {exit_counter}")
        elif command_name=="Open For Entry" and res:
            counter=set()
            for r in res:
                if r[6:10]=="1200":
                    if r[14:16]=="60":
                        print("INTRUSION")
                    if r[14:16]=="62":
                        print("TAILING")
                    if r[18:24] not in counter:
                        counter.add(r[18:24])

            if len(counter)==2: print("COUNTER INCREASED BY ONE")

            # print("OFE",res)





def input_and_output_menu(commands, addr_to):
    print("You are in the Input and Output Mode".upper())
    command_name, command_type=print_options(commands=commands)
    if not command_name and not command_type:
        return
    if command_type=="straight":
        generated_commands=input_output_menu_straight_command(command_name=command_name, addr_to=addr_to)
    elif command_type=="set":
        generated_commands=input_output_menu_set_commands(command_name=command_name, addr_to=addr_to)
    else:
        print("command_type is wrong, '{}'".format(command_type))
    print(generated_commands)
    gen=generated_commands[0].split(" ")
    return ["".join(gen)], command_name

def status_and_control_menu(commands, addr_to):
    print("You are in the Status and Control Mode".upper())
    command_name, command_type=print_options(commands=commands)
    if not command_name and not command_type:
        return
    if command_type=="straight":
        generated_commands=status_control_menu_straight_command(command_name=command_name, addr_to=addr_to)
    elif command_type=="set":
        generated_commands=status_control_menu_set_commands(command_name=command_name, addr_to=addr_to)
    else:
        print("command_type is wrong, '{}'".format(command_type))
    gen=generated_commands[0].split(" ")
    return ["".join(gen)], command_name


def print_options(commands):
    mode_exit_condition=False
    for command in commands:
        id=command.get("id")
        if not id:
            print("This dic does'nt have id")
            print(command)
            continue
        com=command.get("command")
        if not com:
            print("This dic does'nt have command")
            print(command)
            continue
        print(f"Enter '{id}' for '{com}'")

    opt=input("Enter: ")
    command_name=""
    command_type=""
    for command in commands:
        identity=command.get("id")
        if identity == int(opt):
            command_name=command.get("command")
            command_type=command.get("type")

    if not command_name and not command_type:
        print("you have selected wrong id")
        return "",""

    return command_name, command_type



try:
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 38400
    TIMEOUT = 6
    ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    asyncio.run(menu(ser))
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()


