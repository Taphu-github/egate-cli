from commands_and_variables import get_and_create_command, get_command, convert_deci_to_hex, get_semi_complete_command, generate_checksum

def input_output_menu_straight_command(command_name, addr_to):
    if not command_name:
        print("Command not found")
    else:
        generated_commands=get_and_create_command(command_name=command_name, addr_to=addr_to)
    return generated_commands

def input_output_menu_set_commands(command_name, addr_to):
    command_structure=get_command(command_name)
    print_str=""
    if command_name=="Set D1":
        print_str="Enter '1' to turn on D1 and '0' to turn off D1: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set D2":
        print_str="Enter '1' to turn on D2 and '0' to turn off D2: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set D3":
        print_str="Enter '1' to turn on D3 and '0' to turn off D3: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set D4":
        print_str="Enter '1' to turn on D4 and '0' to turn off D4: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set R":
        print_str="Enter '1' to turn on R and '0' to turn off R: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set G":
        print_str="Enter '1' to turn on G and '0' to turn off G: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set B":
        print_str="Enter '1' to turn on B and '0' to turn off B: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set Relay 1":
        print_str="Enter '1' to turn on Relay 1 and '0' to turn off Relay 1: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=2 )
    elif command_name=="Set Battery":
        print_str="Enter '1' to turn on Battery and '0' to turn off Battery: "
        return setting_one_hex(command_structure=command_structure, addr_to=addr_to, print_str=print_str, data_index=1 )
    else:
        print("wrong command name")


def setting_one_hex(command_structure, addr_to, print_str, data_index):
    input_data=""
    exit_status=False
    while not exit_status:
        on_off=int(input(print_str))
        if on_off==1:
            input_data="01"
            exit_status=True
        elif on_off==0:
            input_data="00"
            exit_status=True

    command_str,datas=get_semi_complete_command(command_structure=command_structure, addr_to=addr_to)
    datas[data_index]=input_data

    without_checksum_command=command_str+" "+" ".join(datas).upper()
    checksum=generate_checksum(without_checksum_command)
    # print(without_checksum_command+" "+checksum)
    return without_checksum_command+ " " + checksum
