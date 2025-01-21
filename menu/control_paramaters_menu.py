from commands_and_variables import get_and_create_command, convert_deci_to_hex, generate_checksum

def control_parameters_menu_straight_command(command_name, addr_to):
    if not command_name:
        print("Command not found")
    else:
        generated_commands=get_and_create_command(command_name=command_name, addr_to=addr_to)
    return generated_commands

def control_parameters_menu_set_commands(command_name, addr_to):
    # command_names={15:"Set Counter"#data[2-4]:entry count, data[5-7]:exit count
    # }
    if command_name=="Set Device and Pass Through Parameters":
        print(set_device_and_pass_through_parameters(addr_to=addr_to))
    elif command_name=="Set Event List for Open For Entry and Close For Entry":
        pass
    elif command_name=="Set Event List for Open For Exit and Close For Exit":
        pass
    elif command_name=="Set Event List for Device Lost Power and External Alarm":
        pass
    elif command_name=="Set Event List for Fire Alarm and Intrusion Alarm":
        pass
    elif command_name=="Set Event List for Reverse Alarm and Tailing Alarm":
        pass
    elif command_name=="Set Event List for Stayed Alarm and Reserve":
        pass
    elif command_name=="Set Default State For Gate Mode and Switch Event":
        pass
    else:
        pass

def set_device_and_pass_through_parameters(addr_to):
    addr_src="02"
    cid1cid2="01 12"

    #00 00
    entry_open_door_motor_speed_motor1=int(input("motor 1 speed for ENTRY OPEN DOOR(0-100): "))
    entry_open_door_motor_speed_motor2=int(input("motor 2 speed for ENTRY OPEN DOOR(0-100): "))
    entry_close_door_motor_speed_motor1=int(input("motor 1 speed for ENTRY CLOSE DOOR(0-100): "))
    entry_close_door_motor_speed_motor2=int(input("motor 2 speed for ENTRY CLOSE DOOR(0-100): "))
    exit_open_door_motor_speed_motor1=int(input("motor 1 speed for EXIT OPEN DOOR(0-100): "))
    exit_open_door_motor_speed_motor2=int(input("motor 1 speed for EXIT OPEN DOOR(0-100): "))

    d0000_2=convert_deci_to_hex(int(entry_open_door_motor_speed_motor1),1)
    d0000_3=convert_deci_to_hex(int(entry_open_door_motor_speed_motor2),1)
    d0000_4=convert_deci_to_hex(int(entry_close_door_motor_speed_motor1),1)
    d0000_5=convert_deci_to_hex(int(entry_close_door_motor_speed_motor2),1)
    d0000_6=convert_deci_to_hex(int(exit_open_door_motor_speed_motor1),1)
    d0000_7=convert_deci_to_hex(int(exit_open_door_motor_speed_motor2),1)
    d0000="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 00 "+d0000_2+" "+d0000_3+" "+d0000_4+" "+d0000_5+" "+d0000_6+" "+d0000_7
    d0000_checksum=generate_checksum(d0000)
    d0000="AA "+d0000+" "+d0000_checksum

    #00 01
    exit_close_door_motor_speed_motor1=int(input("Motor 1 speed for EXIT CLOSE DOOR(0-100): "))
    exit_close_door_motor_speed_motor2=int(input("Motor 1 speed for EXIT CLOSE DOOR(0-100): "))
    motor_over_current_protection=input("Motor over current protection(20->2.0V): \n")
    ir_sensor_type=input("Select IR sensor type:\n1 for 'PNP (Hi Trig) (Default)'\n2 for 'PNP (Low Trig)'\n")
    ir_logic=input("Select IR Logic:\n1 for Disabled\n2 for Local Interface\n3 for External For Entry (Default)\n4 for External For Exit\n5 for External For Both\n")
    relay_for_passed_counter=input("Select Relay for passed counter: \n1 for entry\n2 for disabled\n3 for exit\n4 for both (default)\n")

    d0001_2=convert_deci_to_hex(int(exit_close_door_motor_speed_motor1),1)
    d0001_3=convert_deci_to_hex(int(exit_close_door_motor_speed_motor2),1)
    d0001_4=convert_deci_to_hex(int(motor_over_current_protection),1)
    d0001_5= "01" if ir_sensor_type==2 else "00"
    d0001_6= "00" if ir_logic==1 else "01" if ir_logic==2 else "80" if ir_logic==4 else "C0" if ir_logic==5 else "40"
    d0001_7= "01" if relay_for_passed_counter==1 else "00" if relay_for_passed_counter==2 else "02" if relay_for_passed_counter==3 else "03"
    d0001="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 01 "+d0001_2+" "+d0001_3+" "+d0001_4+" "+d0001_5+" "+d0001_6+" "+d0001_7
    d0001_checksum=generate_checksum(d0001)
    d0001="AA "+d0001+" "+d0001_checksum


    #00 02
    barriers_count=input("Select Barriers_count:\n1 for single\n2 for double (default)\n")
    ir_sensitivity=int(input("IR sensitivity(0-100): \n"))
    normally_open_direction=input("Select Normally Open Direction:\n1 for entry (default)\n2 for exit\n")
    action_on_power_lost=input("Select Action on power lost: \n1 for none\n2 for closed\n3 for always open for entry (default)\n4 for always open for exit\n")
    base_speed_level_motor1=int(input("Base speed level for motor 1(0-100): "))
    base_speed_level_motor2=int(input("Base speed level for motor 2(0-100): "))
    gate_mode=input("Select Gate Mode: \n1 for normally closed, both card\n2 for normally closed, both free\n3 for normally closed, both reject\n4 for normally closed, entry card and exit free\n5 for normally closed, entry card and exit reject (default)\n6 for normally closed, entry free and exit card\n7 for normally closed, entry free and exit reject\n8 for normally closed, entry reject and exit free\n9 for normally closed, entry reject and exit card\n10 for normally open, both free\n11 for normally open, both card\n12 for normally open, entry free and exit card\n13 for normally open, entry card and exit reject\n")

    d0002_2="01" if barriers_count==1 else "00"
    d0002_3=convert_deci_to_hex(int(ir_sensitivity),1)
    normally_open_direction_val="10" if normally_open_direction==2 else "00"
    action_on_power_lost_val="00" if action_on_power_lost==1 else "01" if action_on_power_lost==2 else "03" if action_on_power_lost==4 else "02"
    d0002_4_val=int(normally_open_direction_val, 16)+int(action_on_power_lost_val, 16)
    d0002_4=convert_deci_to_hex(d0002_4_val, 1)
    d0002_5=convert_deci_to_hex(int(base_speed_level_motor1),1)
    d0002_6=convert_deci_to_hex(int(base_speed_level_motor2),1)
    d0002_7="01" if gate_mode==1 else "02" if gate_mode==2 else "03" if gate_mode==3 else "04" if gate_mode==4 else "06" if gate_mode==6 else "07" if gate_mode==7 else "08" if gate_mode==8 else "09" if gate_mode==9 else "0A" if gate_mode==10 else "0B" if gate_mode==11 else "0C" if gate_mode==12 else "0D" if gate_mode==13 else "05"
    d0002="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 02 "+d0002_2+" "+d0002_3+" "+d0002_4+" "+d0002_5+" "+d0002_6+" "+d0002_7
    d0002_checksum=generate_checksum(d0002)
    d0002="AA "+d0002+" "+d0002_checksum
    #00 03
    authorized_with_memory=input("Select Authorized with memory:\n1 for both disabled (default) \n2 for entry allowed\n3 for exit allowed\n4 for both allowed\n")
    maximum_passage_time=int(input("Maximum Passage Time(50->5.0V): "))
    authorized_open_door_delay=int(input("Authorized Open Door Delay(30-> 3sec): "))
    close_door_delay=int(input("Close Door Delay(30->3sec): "))
    authorized_in_lane=input("Select Authorized in Lane: \n1 for On (default)\n2 for Off\n")
    passage_end_ir_check_at=input("Select Passage End IR Check At: \n1 for exit (default)\n2 for safety\n")

    d0003_2="01" if authorized_with_memory==2 else "02" if authorized_with_memory==3 else "03" if authorized_with_memory==4 else "00"
    d0003_3=convert_deci_to_hex(int(maximum_passage_time), 1)
    d0003_4=convert_deci_to_hex(int(authorized_open_door_delay), 1)
    d0003_5=convert_deci_to_hex(int(close_door_delay), 1)
    d0003_6="00" if authorized_in_lane==2 else "01"
    d0003_7="01" if passage_end_ir_check_at==2 else "00"
    d0003="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 03 "+d0003_2+" "+d0003_3+" "+d0003_4+" "+d0003_5+" "+d0003_6+" "+d0003_7
    d0003_checksum=generate_checksum(d0003)
    d0003="AA "+d0003+" "+d0003_checksum

    #00 04
    automatic_report_state="01"
    intrusion_alarm=input("Select Intrusion Alarm: \n1 for none\n2 for alarm \n 3 for alarm and close door (default)\n")
    reverse_alarm=input("Select Reverse Alarm: \n1 for none\n2 for alarm (default)\n 3 for alarm and close door\n")
    tailing_alarm=input("Select Tailing Alarm: \n1 for none\n2 for alarm\n 3 for alarm and close door (default)\n")
    power_on_self_check=input("Select Power On Self Check: \n1 for On(default)\n2 for Off\n")

    print("Automatic Report State: ON")
    d0004_2=automatic_report_state
    d0004_3="00" if intrusion_alarm==1 else "01" if intrusion_alarm==2 else "02"
    d0004_4="00" if reverse_alarm==1 else "02" if reverse_alarm==3 else "01"
    d0004_5="00" if tailing_alarm==1 else "01" if tailing_alarm==2 else "02"
    d0004_6="00" if power_on_self_check==2 else "01"
    d0004_7="00"

    d0004="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 04 "+d0004_2+" "+d0004_3+" "+d0004_4+" "+d0004_5+" "+d0004_6+" "+d0004_7
    d0004_checksum=generate_checksum(d0004)
    d0004="AA "+d0004+" "+d0004_checksum


    # print([d0000, d0001, d0002, d0003, d0004])
    # print(d0000)
    # print(d0001)
    # print(d0002)
    # print(d0003)
    # print(d0004)
    return [d0000, d0001, d0002, d0003, d0004]