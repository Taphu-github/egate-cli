import json
import serial
import asyncio
from parse_response import parse

SERIAL_PORT = "COM3"
BAUD_RATE = 38400
TIMEOUT = 0.5

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

main_json = {
    "device_information": device_information,
    "device_parameters": device_parameters,
    "pass_through_parameters": pass_through_parameters,
    "event_list": event_list,
    "switch_event": switch_event,
}

# # print(pass_through_parameters)
# # set_device_information_config(device_information)


async def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        exit()

    from device_information_config import set_device_address, set_device_information_config
    from config_util import get_mac_address, get_device_id, run_command
    from device_control import (
        set_device_and_pass_through_parameters,
        set_default_state_for_gate_mode_and_switch_event,
        set_event_list_for_open_for_entry_and_close_for_entry,
        set_event_list_for_open_for_exit_and_close_for_exit,
        set_event_list_for_fire_alarm_and_intrusion_alarm,
        set_event_list_for_device_lost_power_and_external_alarm,
        set_event_list_for_reverse_alarm_and_tailing_alarm,
        set_event_list_for_stayed_alarm_and_reserve,
    )

    addr_to = get_device_id(ser=ser)
    mac_address = get_mac_address(ser=ser)
    # addr_to="02"
    # mac_address="F0 F0 F0 F0 F0 F0"

    command_arr = []
    command_arr.extend(
        set_device_information_config(
            json_list=device_information, addr_to=addr_to, mac_address=mac_address
        )
    )
    command_arr.extend(
        set_device_and_pass_through_parameters(
            device_parameters=device_parameters,
            pass_through_parameters=pass_through_parameters,
            addr_to=addr_to,
        )
    )
    command_arr.extend(
        set_default_state_for_gate_mode_and_switch_event(
            pass_through_parameters=pass_through_parameters,
            switch_event=switch_event,
            addr_to=addr_to,
        )
    )
    command_arr.extend(
        set_event_list_for_open_for_entry_and_close_for_entry(
            event_list=event_list, addr_to=addr_to
        )
    )
    command_arr.extend(
        set_event_list_for_open_for_exit_and_close_for_exit(
            event_list=event_list, addr_to=addr_to
        )
    )
    command_arr.extend(
        set_event_list_for_device_lost_power_and_external_alarm(
            event_list=event_list, addr_to=addr_to
        )
    )
    command_arr.extend(
        set_event_list_for_fire_alarm_and_intrusion_alarm(
            event_list=event_list, addr_to=addr_to
        )
    )
    command_arr.extend(
        set_event_list_for_reverse_alarm_and_tailing_alarm(
            event_list=event_list, addr_to=addr_to
        )
    )
    command_arr.extend(
        set_event_list_for_stayed_alarm_and_reserve(event_list=event_list, addr_to=addr_to)
    )

    # print(mac_address)


    all_response=await run_command(ser=ser, command_arr=command_arr)
    # print(all_response)

    ser.close()



    # print(all_response)
    for response in all_response:
        # print(response)
        # arranged_response = [
        #     response[i : i + 2]
        #     for i in range(0, (len(response)), 2)
        # ]
        # print(arranged_response)
        # parse(response)
        try:
            parse(response)
        except Exception:
            print("error at: ",response)
        #     print("Error: ", Exception)


asyncio.run(main())