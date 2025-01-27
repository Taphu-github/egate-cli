import json
# from device_information_menu import
import asyncio
import serial
from aioserial import AioSerial
from commands_and_variables import COMMANDS, run_command, get_device_id, chunk_bytearray
from input_ouput_menu import input_output_menu_straight_command, input_output_menu_set_commands
from status_control_menu import status_control_menu_straight_command, status_control_menu_set_commands
import threading
from parse_response import parse
import queue
import time

async def menu(ser, addr_to):
    # addr_to="02"
    status_and_control_commands=[]
    input_and_output_commands=[]
    control_parameters_commands=[]
    device_information_commands=[]



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
            await run_command(ser=ser, command_arr=command)

        elif option_var== '2':
            command, command_name=status_and_control_menu(status_and_control_commands, addr_to)
            await run_command(ser=ser, command_arr=command)
        elif option_var== '0':
            # exit_condition=False
            exit(0)
        else :
            pass






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

    opt=input("")
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



def main_thread(ser, addr_to):
    asyncio.run(menu(ser, addr_to))


def read_continuous(ser, addr_to):
    temp_buffer=bytearray()
    response_arr=[]
    while True:
        response = bytearray()
        start_time = time.perf_counter()
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))

        if response:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.6f} seconds")

            if len(response)==16:
                response_chunks = chunk_bytearray(response)
                print(response_chunks)
                for res in response_chunks: parse(res)
                # parse(response_chunks[0])
            else:
                temp_buffer.extend(response)

            if len(temp_buffer)==16:
                response_chunks = chunk_bytearray(temp_buffer)
                print(response_chunks)
                for res in response_chunks: parse(res)
                temp_buffer.clear()
            # response_chunks = chunk_bytearray(response)


            # temp_response_chunks=response_chunks
            # for i in range(len(response_chunks)):
            #     if len(response_chunks[i])==32:
            #         response_arr.append(response_chunks[i])
            #         temp_response_chunks.pop(i)
            # temp=""
            # for i in range(len(temp_response_chunks)):
            #     if len(temp_response_chunks[i])+len(temp_response_chunks[i+1])==16:
            #         temp=temp_response_chunks[i]+temp_response_chunks[i+1]
            # response_arr.append(temp)

            # print(response_arr)



# Create two threads
try:
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 38400
    TIMEOUT = 6

    ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    shared_message=queue.Queue()


    addr_to=get_device_id(ser=ser)
    thread1 = threading.Thread(target=main_thread, args=(ser,addr_to,), daemon=True)
    thread2 = threading.Thread(target=read_continuous, args=(ser, addr_to,), daemon=True)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
except Exception as e:
    pass




# if ser.in_waiting > 0:
        #     data = ser.readline().decode('utf-8').strip()
        #     print(f"Received: {data}")


        # if command_name=="Get Voltage" and res:
        #     formatted_response=[res[0][i:i+2] for i in range(0,32,2)]
        #     psv=int("".join(formatted_response[11:13]), 16)
        #     bv=int("".join(formatted_response[13:15]), 16)
        #     print(f"Power Supply Voltage: {psv}")
        #     print(f"Battery Voltage: {bv}")
        # elif command_name=="Refresh Get Passed Counter" and res:
        #     formatted_response=[res[0][i:i+2] for i in range(0,32,2)]
        #     entry_counter=int("".join(formatted_response[9:12]), 16)
        #     exit_counter=int("".join(formatted_response[12:15]), 16)
        #     print(f"Entry Counter: {entry_counter}")
        #     print(f"Exit Countyer: {exit_counter}")
        # elif command_name=="Open For Entry" and res:
        #     counter=set()
        #     for r in res:
        #         if r[6:10]=="1200":
        #             if r[14:16]=="60":
        #                 print("INTRUSION")
        #             if r[14:16]=="62":
        #                 print("TAILING")
        #             if r[18:24] not in counter:
        #                 counter.add(r[18:24])

        #     if len(counter)==2:
        #         counter_list=list(counter)
        #         start=int(counter_list[0], 16)
        #         end=int(counter_list[1], 16)
        #         print(f"COUNTER INCREASED BY ONE FROM {start} to {end}")
        #         print(counter)

            # print("OFE",res)