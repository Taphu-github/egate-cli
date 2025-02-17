import json
# from device_information_menu import
from commands_and_variables import COMMANDS
from input_ouput_menu import input_output_menu_straight_command, input_output_menu_set_commands
from status_control_menu import status_control_menu_straight_command, status_control_menu_set_commands


def menu():
    addr_to="09"
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
            input_and_output_menu(input_and_output_commands, addr_to)
        elif option_var== '2':
            status_and_control_menu(status_and_control_commands, addr_to)
        elif option_var== '0':
            exit_condition=False
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
    print(generated_commands)

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





menu()