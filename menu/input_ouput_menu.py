from commands_and_variables import get_and_create_command

def input_output_menu_straight_command(command_name, addr_to):
    if not command_name:
        print("Command not found")
    else:
        generated_commands=get_and_create_command(command_name=command_name, addr_to=addr_to)
    return generated_commands

def input_output_menu_set_commands():
    command_names={15:"Set Counter"#data[2-4]:entry count, data[5-7]:exit count
    }