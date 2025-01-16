def validate_command(command, command_name):
    commad_arr=command.split(" ")
    if len(commad_arr)!=16:
        print(f"the {command_name} command is incomplete")

    for com in commad_arr:
        try:
            int(com, 16)
        except Exception as e:
            print(f"the {command_name} has consists of non-hexadecimal value ")

validate_command(command="AA 00 02 11 11 01 08 04 02 00 F0 01 00 00 00 24", command_name="my_command")