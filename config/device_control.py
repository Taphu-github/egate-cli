from config_util import convert_deci_to_hex, generate_checksum, to_int, hex_to_deci, OPTIONS_MAPPING

def set_device_and_pass_through_parameters(device_parameters, pass_through_parameters, addr_to):
    addr_src="02"
    cid1cid2="11 11"
    # "00 "+addr_src+" "+cid1cid2+" "+addr_to+
    #00 00
    entry_open_door_motor_speed_motor1=device_parameters.get("entry_open_door_motor_speed", {}).get("motor_1", "100")
    entry_open_door_motor_speed_motor2=device_parameters.get("entry_open_door_motor_speed", {}).get("motor_2", "100")
    entry_close_door_motor_speed_motor1=device_parameters.get("entry_close_door_motor_speed", {}).get("motor_1", "100")
    entry_close_door_motor_speed_motor2=device_parameters.get("entry_close_door_motor_speed", {}).get("motor_2", "100")
    exit_open_door_motor_speed_motor1=device_parameters.get("exit_open_door_motor_speed", {}).get("motor_1", "100")
    exit_open_door_motor_speed_motor2=device_parameters.get("exit_open_door_motor_speed", {}).get("motor_2", "100")

    d0000_2=convert_deci_to_hex(to_int(entry_open_door_motor_speed_motor1),1)
    d0000_3=convert_deci_to_hex(to_int(entry_open_door_motor_speed_motor2),1)
    d0000_4=convert_deci_to_hex(to_int(entry_close_door_motor_speed_motor1),1)
    d0000_5=convert_deci_to_hex(to_int(entry_close_door_motor_speed_motor2),1)
    d0000_6=convert_deci_to_hex(to_int(exit_open_door_motor_speed_motor1),1)
    d0000_7=convert_deci_to_hex(to_int(exit_open_door_motor_speed_motor2),1)
    d0000="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 00 "+d0000_2+" "+d0000_3+" "+d0000_4+" "+d0000_5+" "+d0000_6+" "+d0000_7
    d0000_checksum=generate_checksum(d0000)
    d0000="AA "+d0000+" "+d0000_checksum

    #00 01
    exit_close_door_motor_speed_motor1=device_parameters.get("exit_close_door_motor_speed", {}).get("motor_1", "100") or 100
    exit_close_door_motor_speed_motor2=device_parameters.get("exit_close_door_motor_speed", {}).get("motor_2", "100") or 100
    motor_over_current_protection=device_parameters.get("motor_overcurrent_protection", {}).get("value", "20") or 25
    ir_sensor_type=device_parameters.get("ir_sensor_type", {}).get("value","PNP (Hi Trig)") or 'PNP (Hi Trig)'
    ir_logic=device_parameters.get("ir_logic", {}).get("value","External For Entry") or "External For Entry"
    relay_for_passed_counter=device_parameters.get("relay_for_passed_counter", {}).get("value","Disabled") or "Disabled"

    d0001_2=convert_deci_to_hex(to_int(exit_close_door_motor_speed_motor1),1)
    d0001_3=convert_deci_to_hex(to_int(exit_close_door_motor_speed_motor2),1)
    d0001_4=convert_deci_to_hex(to_int(motor_over_current_protection),1)
    d0001_5= OPTIONS_MAPPING.get("ir_sensor_type",{}).get(ir_sensor_type.lower(), "00")
    d0001_6= OPTIONS_MAPPING.get("ir_logic",{}).get(ir_logic.lower(), "40")
    d0001_7=OPTIONS_MAPPING.get("relay_for_passed_counter",{}).get(relay_for_passed_counter.lower(), "00")
    d0001="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 01 "+d0001_2+" "+d0001_3+" "+d0001_4+" "+d0001_5+" "+d0001_6+" "+d0001_7
    d0001_checksum=generate_checksum(d0001)
    d0001="AA "+d0001+" "+d0001_checksum


    #00 02
    barriers_count=device_parameters.get("barriers_count", {}).get("value","Double" ) or "Double"
    ir_sensitivity=device_parameters.get("ir_sensitivity", {}).get("value", "100") or 100
    normally_open_direction=device_parameters.get("normally_open_direction", {}).get("value","Entry") or "Entry"
    action_on_power_lost=device_parameters.get("action_on_power_lost", {}).get("value", "Always Open For Entry") or "Always Open For Entry"
    base_speed_level_motor1=device_parameters.get("base_speed_level",{}).get("motor_1","100") or 100
    base_speed_level_motor2=device_parameters.get("base_speed_level",{}).get("motor_2","100") or 100
    gate_mode=pass_through_parameters.get("gate_mode",{}).get("value","Normally Closed, Entry Card & Exit Reject") or "Normally Closed, Entry Card & Exit Reject"

    d0002_2=OPTIONS_MAPPING.get("barriers_count",{}).get(barriers_count.lower(), "00")
    d0002_3=convert_deci_to_hex(to_int(ir_sensitivity),1)
    normally_open_direction_val=OPTIONS_MAPPING.get("normally_open_direction",{}).get(normally_open_direction.lower(), "00")
    action_on_power_lost_val=OPTIONS_MAPPING.get("action_on_power_lost",{}).get(action_on_power_lost.lower(), "02")
    d0002_4_val=int(normally_open_direction_val, 16)+int(action_on_power_lost_val, 16)
    d0002_4=convert_deci_to_hex(d0002_4_val, 1)
    d0002_5=convert_deci_to_hex(int(base_speed_level_motor1),1)
    d0002_6=convert_deci_to_hex(int(base_speed_level_motor2),1)
    d0002_7=OPTIONS_MAPPING.get("gate_mode",{}).get(gate_mode.lower(), "05")
    d0002="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 02 "+d0002_2+" "+d0002_3+" "+d0002_4+" "+d0002_5+" "+d0002_6+" "+d0002_7
    d0002_checksum=generate_checksum(d0002)
    d0002="AA "+d0002+" "+d0002_checksum

    #00 03
    authorized_with_memory=pass_through_parameters.get("authorized_with_memory",{}).get("value","Entry Allowed") or "Entry Allowed"
    maximum_passage_time=pass_through_parameters.get("maximum_passage_time",{}).get("value","50") or 50
    authorized_open_door_delay=pass_through_parameters.get("authorized_open_door_delay",{}).get("value","00") or 0
    close_door_delay=pass_through_parameters.get("close_door_delay",{}).get("value","00") or 0
    authorized_in_lane=pass_through_parameters.get("authorized_in_lane",{}).get("value","Off") or "Off"
    passage_end_ir_check_at=pass_through_parameters.get("passage_end_ir_check_at",{}).get("value","Exit") or "Exit"

    d0003_2=OPTIONS_MAPPING.get("authorized_with_memory", {}).get(authorized_with_memory.lower(), "00")
    d0003_3=convert_deci_to_hex(int(maximum_passage_time), 1)
    d0003_4=convert_deci_to_hex(int(authorized_open_door_delay), 1)
    d0003_5=convert_deci_to_hex(int(close_door_delay), 1)
    d0003_6=OPTIONS_MAPPING.get("authorized_in_lane", {}).get(authorized_in_lane.lower(), "00")
    d0003_7=OPTIONS_MAPPING.get("passage_end_ir_check_at", {}).get(passage_end_ir_check_at.lower(), "00")
    d0003="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 03 "+d0003_2+" "+d0003_3+" "+d0003_4+" "+d0003_5+" "+d0003_6+" "+d0003_7
    d0003_checksum=generate_checksum(d0003)
    d0003="AA "+d0003+" "+d0003_checksum

    #00 04
    automatic_report_state=pass_through_parameters.get("automatic_report_state",{}).get("value","On") or "On"
    intrusion_alarm=pass_through_parameters.get("intrusion_alarm",{}).get("value","Alarm") or "Alarm"
    reverse_alarm=pass_through_parameters.get("reverse_alarm",{}).get("value","Alarm") or "Alarm"
    tailing_alarm=pass_through_parameters.get("tailing_alarm",{}).get("value","Alarm") or "Alarm"
    power_on_self_check=device_parameters.get("power_on_self_check",{}).get("value","Off") or "Off"

    d0004_2=OPTIONS_MAPPING.get("automatic_report_state", {}).get(automatic_report_state.lower(), "01")
    d0004_3=OPTIONS_MAPPING.get("intrusion_alarm",{}).get(intrusion_alarm.lower(), "01")
    d0004_4=OPTIONS_MAPPING.get("reverse_alarm",{}).get(reverse_alarm.lower(), "01")
    d0004_5=OPTIONS_MAPPING.get("tailing_alarm",{}).get(tailing_alarm.lower(), "01")
    d0004_6=OPTIONS_MAPPING.get("power_on_self_check",{}).get(power_on_self_check.lower(),"00" )
    d0004_7="00"

    d0004="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 00 04 "+d0004_2+" "+d0004_3+" "+d0004_4+" "+d0004_5+" "+d0004_6+" "+d0004_7
    d0004_checksum=generate_checksum(d0004)
    d0004="AA "+d0004+" "+d0004_checksum


    # print([d0000, d0001, d0002, d0003, d0004])
    print(d0000)
    print(d0001)
    print(d0002)
    print(d0003)
    print(d0004)

def set_default_state_for_gate_mode_and_switch_event(pass_through_parameters, switch_event, addr_to):
    # print(switch_event)
    addr_src="02"
    cid1cid2="11 11"


    #0100
    normally_closed_both_card=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_both_card",{})
    normally_closed_both_free=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_both_free",{})
    normally_closed_both_reject=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_both_reject",{})
    normally_closed_entry_card_exit_free=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_card_exit_free",{})
    normally_closed_entry_card_exit_reject=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_card_exit_reject",{})
    normally_closed_entry_free_exit_card=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_free_exit_card",{})

    d0100_2=calculate_ir_and_color(normally_closed_both_card)
    d0100_3=calculate_ir_and_color(normally_closed_both_free)
    d0100_4=calculate_ir_and_color(normally_closed_both_reject)
    d0100_5=calculate_ir_and_color(normally_closed_entry_card_exit_free)
    d0100_6=calculate_ir_and_color(normally_closed_entry_card_exit_reject)
    d0100_7=calculate_ir_and_color(normally_closed_entry_free_exit_card)

    d0100="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 01 00 "+d0100_2+" "+d0100_3+" "+d0100_4+" "+d0100_5+" "+d0100_6+" "+d0100_7
    d0100_check_sum=generate_checksum(d0100)
    d0100="AA "+d0100+" "+d0100_check_sum


    #0101
    normally_closed_entry_free_exit_reject=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_free_exit_reject",{})
    normally_closed_entry_reject_exit_free=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_reject_exit_free",{})
    normally_closed_entry_reject_exit_card=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_closed_entry_reject_exit_card",{})
    normally_open_both_free=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_open_both_free",{})
    normally_open_both_card=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_open_both_card",{})
    normally_open_entry_free_exit_card=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_open_entry_free_exit_card",{})

    d0101_2=calculate_ir_and_color(normally_closed_entry_free_exit_reject)
    d0101_3=calculate_ir_and_color(normally_closed_entry_reject_exit_free)
    d0101_4=calculate_ir_and_color(normally_closed_entry_reject_exit_card)
    d0101_5=calculate_ir_and_color(normally_open_both_free)
    d0101_6=calculate_ir_and_color(normally_open_both_card)
    d0101_7=calculate_ir_and_color(normally_open_entry_free_exit_card)

    d0101="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 01 01 "+d0101_2+" "+d0101_3+" "+d0101_4+" "+d0101_5+" "+d0101_6+" "+d0101_7
    d0101_check_sum=generate_checksum(d0101)
    d0101="AA "+d0101+" "+d0101_check_sum

    #0102
    normally_open_entry_card_exit_free=pass_through_parameters.get("gate_mode_default_state",{}).get("normally_open_entry_card_exit_free",{})
    automatic_switch1_trigger=switch_event.get("automatic_switch_1",{}).get("on_trigger", "Open For Entry")
    automatic_switch1_release=switch_event.get("automatic_switch_1",{}).get("on_release", "None")
    automatic_switch2_trigger=switch_event.get("automatic_switch_2",{}).get("on_trigger","Open For Exit" )
    automatic_switch2_release=switch_event.get("automatic_switch_2",{}).get("on_release", "None")
    fire_alarm_trigger=switch_event.get("fire_alarm",{}).get("on_trigger", "Always Open For Exit")
    fire_alarm_release=switch_event.get("fire_alarm",{}).get("on_release", "Idle (Default State)")
    manual_switch_trigger=switch_event.get("manual_switch",{}).get("on_trigger","Always Open For Entry" )
    manual_switch_release=switch_event.get("manual_switch",{}).get("on_release","Idle (Default State)" )

    d0102_2=calculate_ir_and_color(normally_open_entry_card_exit_free)

    automatic_switch1_trig=OPTIONS_MAPPING.get("switch_options", {}).get("on_trigger", {}).get(automatic_switch1_trigger.lower(), "02")
    automatic_switch1_rel=OPTIONS_MAPPING.get("switch_options", {}).get("on_release", {}).get(automatic_switch1_release.lower(), "00")
    automatic_switch1_int=int(automatic_switch1_trig, 16)+int(automatic_switch1_rel, 16)
    d0102_3=convert_deci_to_hex(automatic_switch1_int, 1)

    automatic_switch2_trig=OPTIONS_MAPPING.get("switch_options", {}).get("on_trigger", {}).get(automatic_switch2_trigger.lower(), "02")
    automatic_switch2_rel=OPTIONS_MAPPING.get("switch_options", {}).get("on_release", {}).get(automatic_switch2_release.lower(), "00")
    automatic_switch2_int=int(automatic_switch2_trig, 16)+int(automatic_switch2_rel, 16)
    d0102_4=convert_deci_to_hex(automatic_switch2_int, 1)

    fire_alarm_trig=OPTIONS_MAPPING.get("switch_options", {}).get("on_trigger", {}).get(fire_alarm_trigger.lower(), "03")
    fire_alarm_rel=OPTIONS_MAPPING.get("switch_options", {}).get("on_release", {}).get(fire_alarm_release.lower(), "10")
    fire_alarm_int=int(fire_alarm_trig, 16)+int(fire_alarm_rel, 16)
    d0102_5=convert_deci_to_hex(fire_alarm_int, 1)

    manual_switch_trig=OPTIONS_MAPPING.get("switch_options", {}).get("on_trigger", {}).get(manual_switch_trigger.lower(), "03")
    manual_switch_rel=OPTIONS_MAPPING.get("switch_options", {}).get("on_release", {}).get(manual_switch_release.lower(), "10")
    manual_switch_int=int(manual_switch_trig, 16)+int(manual_switch_rel, 16)
    d0102_6=convert_deci_to_hex(manual_switch_int, 1)

    d0102_7="00"

    d0102="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 01 02 "+d0102_2+" "+d0102_3+" "+d0102_4+" "+d0102_5+" "+d0102_6+" "+d0102_7
    d0102_check_sum=generate_checksum(d0102)
    d0102="AA "+d0102+" "+d0102_check_sum

    d0103="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 01 03 00 00 00 00 00 00"
    d0103_check_sum=generate_checksum(d0103)
    d0103="AA "+d0103+" "+ d0103_check_sum

    d0104="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 01 04 00 00 00 00 00 00"
    d0104_check_sum=generate_checksum(d0104)
    d0104="AA "+d0104+" "+ d0104_check_sum

    # print([d0100, d0101, d0102, d0103, d0104])
    print(d0100)
    print(d0101)
    print(d0102)
    print(d0103)
    print(d0104)


def set_event_list_for_open_for_entry_and_close_for_entry(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("open_for_entry"), event_2=event_list.get("close_for_entry"), addr_to=addr_to, d00="02")

def set_event_list_for_open_for_exit_and_close_for_exit(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("open_for_exit"), event_2=event_list.get("close_for_exit"), addr_to=addr_to, d00="03")

def set_event_list_for_device_lost_power_and_external_alarm(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("device_lost_power"), event_2=event_list.get("external_alarm"), addr_to=addr_to, d00="04")

def set_event_list_for_fire_alarm_and_intrusion_alarm(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("fire_alarm"), event_2=event_list.get("intrusion_alarm"), addr_to=addr_to, d00="05")

def set_event_list_for_reverse_alarm_and_tailing_alarm(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("reverse_alarm"), event_2=event_list.get("tailing_alarm"), addr_to=addr_to, d00="06")

def set_event_list_for_stayed_alarm_and_reserve(event_list, addr_to):
    generate_two_events_config(event_1=event_list.get("stayed_alarm"), event_2=event_list.get("reverse"), addr_to=addr_to, d00="07")

def calculate_ir_and_color(ir_and_color_json):
    d1_val=ir_and_color_json.get("d1", "Off")
    d1_hex="01" if d1_val.lower()=="on" else "00"
    d1=int(d1_hex, 16)

    d2_val=ir_and_color_json.get("d2", "Off")
    d2_hex="02" if d2_val.lower()=="on" else "00"
    d2=int(d2_hex, 16)

    d3_val=ir_and_color_json.get("d3","Off")
    d3_hex="04" if d3_val.lower()=="on" else "00"
    d3=int(d3_hex, 16)

    d4_val=ir_and_color_json.get("d4","Off")
    d4_hex="08" if d4_val.lower()=="on" else "00"
    d4=int(d4_hex, 16)

    r_val=ir_and_color_json.get("r","Off")
    r_hex="10" if r_val.lower()=="on" else "00"
    r=int(r_hex, 16)

    g_val=ir_and_color_json.get("g","Off")
    g_hex="20" if g_val.lower()=="on" else "00"
    g=int(g_hex, 16)

    b_val=ir_and_color_json.get("b","Off")
    b_hex="40" if b_val.lower()=="on" else "00"
    b=int(b_hex, 16)

    # print(f'd1: {d1} d2: {d2}, d3: {d3}, d4: {d4}, r: {r}, g: {g}, b: {b}')

    total=d1+d2+d3+d4+r+g+b

    return convert_deci_to_hex(total, 1)

def generate_two_events_config(event_1, event_2, addr_to, d00):
    addr_src="02"
    cid1cid2="11 11"
     #0
    entrance_indicator=event_1.get("entrance_indicator",{}).get("choice","D1") or "D1"
    # print(f"Label Entrance Indicator (D3): '{entrance_indicator}'")
    entrance_indicator_blink_on=event_1.get("entrance_indicator",{}).get("blink_on_delay","0") or 0
    entrance_indicator_blink_off=event_1.get("entrance_indicator",{}).get("blink_off_delay","0") or 0
    entrance_indicator_repetitions=event_1.get("entrance_indicator",{}).get("repetitions","0") or 0
    rgb_led=event_1.get("rgb_led",{}).get("choice","Black(All Off)") or "Black(All Off)"

    d0_2="00"
    d0_3=OPTIONS_MAPPING.get("entrance_indicator",{}).get(entrance_indicator.lower(), "01") or "01"
    # print("Entrance Indicator Json: ", OPTIONS_MAPPING.get("entrance_indicator"))
    # print(f"Value Entrance Indicator (D3): '{d0_3}'")
    d0_4=convert_deci_to_hex(entrance_indicator_blink_on, 1)
    d0_5=convert_deci_to_hex(entrance_indicator_blink_off, 1)
    d0_6=convert_deci_to_hex(entrance_indicator_repetitions, 1)
    d0_7=OPTIONS_MAPPING.get("rgb_led",{}).get(rgb_led.lower(),"00" ) or "00"
    d0="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 "+d00+" 00 "+d0_2+" "+d0_3+" "+d0_4+" "+d0_5+" "+d0_6+" "+d0_7
    d0_check_sum=generate_checksum(d0)
    d0="AA "+d0+" "+d0_check_sum


    #1
    rgb_led_blink_on=event_1.get("rgb_led",{}).get("blink_on_delay","0") or "0"
    rgb_led_blink_off=event_1.get("rgb_led",{}).get("blink_off_delay","0") or "0"
    rgb_led_repetitions=event_1.get("rgb_led",{}).get("repetitions","0") or "0"
    relay=event_1.get("relay",{}).get("choice","None") or "None"
    relay_blink_on=event_1.get("relay",{}).get("blink_on_delay","0") or "0"
    relay_blink_off=event_1.get("relay",{}).get("blink_off_delay","0") or "0"

    d1_2=convert_deci_to_hex(rgb_led_blink_on,1)
    d1_3=convert_deci_to_hex(rgb_led_blink_off,1)
    d1_4=convert_deci_to_hex(rgb_led_repetitions, 1)
    d1_5=OPTIONS_MAPPING.get("relay",{}).get(relay.lower(), "F0")
    d1_6=convert_deci_to_hex(relay_blink_on,1)
    d1_7=convert_deci_to_hex(relay_blink_off, 1)
    d1="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 "+d00+" 01 "+d1_2+" "+d1_3+" "+d1_4+" "+d1_5+" "+d1_6+" "+d1_7
    d1_check_sum=generate_checksum(d1)
    d1="AA "+d1+" "+d1_check_sum


    #2
    relay_repetitions=event_1.get("relay",{}).get("repetitions","0") or "0"
    voice_module=event_1.get("voice_module",{}).get("choice","None") or "N9200"
    voice_module_play_sound=event_1.get("voice_module",{}).get("play_sound","1") or "1"
    entrance_indicator1=event_2.get("entrance_indicator",{}).get("choice","D1") or "D1"
    entrance_indicator_blink_on1=event_2.get("entrance_indicator",{}).get("blink_on_delay","0") or 0

    d2_2=convert_deci_to_hex(relay_repetitions,1)
    d2_3=OPTIONS_MAPPING.get("voice_module",{}).get(voice_module.lower(), "F0") or "F0"
    d2_4=convert_deci_to_hex(voice_module_play_sound,1)
    d2_5="00"
    d2_6=OPTIONS_MAPPING.get("entrance_indicator",{}).get(entrance_indicator1.lower(), "F0") or "F0"
    d2_7=convert_deci_to_hex(entrance_indicator_blink_on1,1)
    d2="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 "+d00+" 02 "+d2_2+" "+d2_3+" "+d2_4+" "+d2_5+" "+d2_6+" "+d2_7
    d2_check_sum=generate_checksum(d2)
    d2="AA "+d2+" "+d2_check_sum

    #3
    entrance_indicator_blink_off1=event_2.get("entrance_indicator",{}).get("blink_off_delay","0") or 0
    entrance_indicator_repetitions1=event_2.get("entrance_indicator",{}).get("repetitions","0") or 0
    rgb_led1=event_2.get("rgb_led",{}).get("choice","Black(All Off)") or "Black(All Off)"
    rgb_led_blink_on1=event_2.get("rgb_led",{}).get("blink_on_delay","0") or "0"
    rgb_led_blink_off1=event_2.get("rgb_led",{}).get("blink_off_delay","0") or "0"
    rgb_led_repetitions1=event_2.get("rgb_led",{}).get("repetitions","0") or "0"

    d3_2=convert_deci_to_hex(entrance_indicator_blink_off1,1)
    d3_3=convert_deci_to_hex(entrance_indicator_repetitions1,1)
    d3_4=OPTIONS_MAPPING.get("rgb_led",{}).get(rgb_led1.lower(), "F0") or "F0"
    d3_5=convert_deci_to_hex(rgb_led_blink_on1,1)
    d3_6=convert_deci_to_hex(rgb_led_blink_off1,1)
    d3_7=convert_deci_to_hex(rgb_led_repetitions1,1)

    d3="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 "+d00+" 03 "+d3_2+" "+d3_3+" "+d3_4+" "+d3_5+" "+d3_6+" "+d3_7
    d3_check_sum=generate_checksum(d3)
    d3="AA "+d3+" "+d3_check_sum

    #4
    relay1=event_2.get("relay",{}).get("choice","None") or "None"
    relay_blink_on1=event_2.get("relay",{}).get("blink_on_delay","0") or "0"
    relay_blink_off1=event_2.get("relay",{}).get("blink_off_delay","0") or "0"
    relay_repetitions1=event_2.get("relay",{}).get("repetitions","0") or "0"
    voice_module1=event_2.get("voice_module",{}).get("choice","None") or "N9200"
    voice_module_play_sound1=event_2.get("voice_module",{}).get("play_sound","1") or "1"

    d4_2=OPTIONS_MAPPING.get("relay",{}).get(relay1, "F0") or "F0"
    d4_3=convert_deci_to_hex(relay_blink_on1, 1)
    d4_4=convert_deci_to_hex(relay_blink_off1, 1)
    d4_5=convert_deci_to_hex(relay_repetitions1, 1)
    d4_6=OPTIONS_MAPPING.get("voice_module",{}).get(voice_module1, "F0") or "F0"
    d4_7=convert_deci_to_hex(voice_module_play_sound1, 1)

    d4="00 "+addr_src+" "+cid1cid2+" "+addr_to+" 08 "+d00+" 04 "+d4_2+" "+d4_3+" "+d4_4+" "+d4_5+" "+d4_6+" "+d4_7
    d4_check_sum=generate_checksum(d4)
    d4="AA "+d4+" "+d4_check_sum

    print(d0)
    print(d1)
    print(d2)
    print(d3)
    print(d4)