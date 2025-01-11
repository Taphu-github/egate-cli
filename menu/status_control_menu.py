from commands_and_variables import get_and_create_command, get_command, convert_deci_to_hex, get_semi_complete_command, generate_checksum

def status_control_menu_straight_command(command_name, addr_to):
    if not command_name:
        print("Command not found")
    else:
        generated_commands=get_and_create_command(command_name=command_name, addr_to=addr_to)
    return generated_commands

def status_control_menu_set_commands(command_name, addr_to):

    if command_name=="Set Counter":
        set_counter_command_structure=get_command(command_name)

        entry_count=int(input("Enter the Entry Count: "))
        exit_count=int(input("Enter the Exit Count: "))

        entry_count_in_hex_arr=convert_deci_to_hex(entry_count,3).split(" ")
        exit_count_in_hex_arr=convert_deci_to_hex(exit_count,3).split(" ")

        command_str,datas=get_semi_complete_command(command_structure=set_counter_command_structure, addr_to=addr_to)
        datas[2]=entry_count_in_hex_arr[0]
        datas[3]=entry_count_in_hex_arr[1]
        datas[4]=entry_count_in_hex_arr[2]
        datas[5]=exit_count_in_hex_arr[0]
        datas[6]=exit_count_in_hex_arr[1]
        datas[7]=exit_count_in_hex_arr[2]


        without_checksum_command=command_str+" "+" ".join(datas).upper()
        checksum=generate_checksum(without_checksum_command)
        print(without_checksum_command+" "+checksum)






        # print("command name",command_name)
        # print(get_command(command_name=command_name))



