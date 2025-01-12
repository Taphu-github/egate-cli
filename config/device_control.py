
def set_device_and_pass_through_parameters(json_list):
    #00 00
    entry_open_door_motor_speed_motor1=json_list.get("entry_open_door_motor_speed", {}).get("motor_1", "100")
    entry_open_door_motor_speed_motor2=json_list.get("entry_open_door_motor_speed", {}).get("motor_2", "100")
    entry_close_door_motor_speed_motor1=json_list.get("entry_close_door_motor_speed", {}).get("motor_1", "100")
    entry_close_door_motor_speed_motor2=json_list.get("entry_close_door_motor_speed", {}).get("motor_2", "100")
    exit_open_door_motor_speed_motor1=json_list.get("exit_open_door_motor_speed", {}).get("motor_1", "100")
    exit_open_door_motor_speed_motor2=json_list.get("exit_open_door_motor_speed", {}).get("motor_2", "100")

    #00 01
    exit_close_door_motor_speed_motor1=json_list.get("exit_close_door_motor_speed", {}).get("motor_1", "100")
    exit_close_door_motor_speed_motor2=json_list.get("exit_close_door_motor_speed", {}).get("motor_2", "100")
    motor_over_current_protection=json_list.get("motor_overcurrent_protection", {}).get("value", "20")
    ir_sensor_type=json_list.get("ir_sensor_type, {}").get("value","PNP (Hi Trig)")
    ir_logic=json_list.get("ir_logic", {}).get("value","External For Entry")
    relay_for_passed_counter=json_list.get("relay_for_passed_counter", {}).get("value","Disabled")


    #00 02
    barriers_count=json_list.get("barriers_count", {}).get("value","Double" )
    normally_open_direction=json_list.get("normally_open_direction", {}).get("value","Entry")
    action_on_power_lost=json_list.get("action_on_power_lost", {}).get("value", "Always Open For Entry")
    ir_sensitivity=json_list.get("ir_sensitivity", {}).get("value", "100")
    base_speed_level_motor1=json_list.get("base_speed_level",{}).get("motor_1","100")
    base_speed_level_motor1=json_list.get("base_speed_level",{}).get("motor_2","100")

    #
    print("Setting device and pass-through parameters...")

def set_default_state_for_gate_mode_and_switch_event():
    print("Setting default state for gate mode and switch event...")

def set_event_list_for_open_for_entry_and_close_for_entry():
    print("Setting event list for open for entry and close for entry...")

def set_event_list_for_open_for_exit_and_close_for_exit():
    print("Setting event list for open for exit and close for exit...")

def set_event_list_for_device_lost_power_and_external_alarm():
    print("Setting event list for device lost power and external alarm...")

def set_event_list_for_fire_alarm_and_intrusion_alarm():
    print("Setting event list for fire alarm and intrusion alarm...")

def set_event_list_for_reverse_alarm_and_tailing_alarm():
    print("Setting event list for reverse alarm and tailing alarm...")

def set_event_list_for_stayed_alarm_and_reserve():
    print("Setting event list for stayed alarm and reserve...")

