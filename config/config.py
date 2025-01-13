import json
from device_information_config import set_device_address, set_device_information_config

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

print(pass_through_parameters)
# set_device_information_config(device_information)