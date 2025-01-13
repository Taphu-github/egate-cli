import json
from device_information_config import set_device_address, set_device_information_config
from device_control import set_device_and_pass_through_parameters, set_default_state_for_gate_mode_and_switch_event, set_event_list_for_open_for_entry_and_close_for_entry, set_event_list_for_open_for_exit_and_close_for_exit, set_event_list_for_fire_alarm_and_intrusion_alarm, set_event_list_for_device_lost_power_and_external_alarm, set_event_list_for_reverse_alarm_and_tailing_alarm, set_event_list_for_stayed_alarm_and_reserve


with open("device_information.json", "r") as file:
    device_information = json.load(file)
with open("device_parameters.json", "r") as file:
    device_parameters = json.load(file)
with open("pass_through_parameters.json", "r") as file:
    pass_through_parameters = json.load(file)
with open("event_list.json", "r") as file:
    event_list = json.load(file)
with open("switch_event.json", "r") as file:
    switch_event = json.load(file)

if not device_information:
    print("Device Information 'device_information.json' is missing")
    exit()
if not device_parameters:
    print("Device Parameters 'device_parameters.json' is missing")
    exit()
if not pass_through_parameters:
    print("Pass Through Parameters 'pass_through_parameters.json' is missin")
    exit()
if not event_list:
    print("Event 'event_list.json' is missing")
    exit()
if not switch_event:
    print("Switch 'switch_event.json' is missing")
    exit()

main_json={
    "device_information": device_information,
    "device_parameters":device_parameters,
    "pass_through_parameters":pass_through_parameters,
    "event_list":event_list,
    "switch_event":switch_event
}

# print(pass_through_parameters)
# set_device_information_config(device_information)

set_device_and_pass_through_parameters(device_parameters=device_parameters, pass_through_parameters=pass_through_parameters, addr_to="02")
set_default_state_for_gate_mode_and_switch_event(pass_through_parameters=pass_through_parameters,switch_event=switch_event, addr_to="02")
set_event_list_for_open_for_entry_and_close_for_entry(event_list=event_list, addr_to="02")
set_event_list_for_open_for_exit_and_close_for_exit(event_list=event_list, addr_to="02")
set_event_list_for_device_lost_power_and_external_alarm(event_list=event_list, addr_to="02")
set_event_list_for_fire_alarm_and_intrusion_alarm(event_list=event_list, addr_to="02")
set_event_list_for_reverse_alarm_and_tailing_alarm(event_list=event_list, addr_to="02")
set_event_list_for_stayed_alarm_and_reserve(event_list=event_list, addr_to="02")
