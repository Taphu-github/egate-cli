import json
import asyncio
from aioserial import AioSerial
from parse_response import parse
import os

from device_information_config import set_device_information_config, set_device_address
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

SERIAL_PORT = '/dev/ttyUSB0'
#"COM3"
BAUD_RATE = 38400
TIMEOUT = 0.5
base_dir=os.getcwd()

def load_json(file_path):
    try:
        full_file_path = os.path.join(base_dir, "config_jsons", file_path)
        with open(full_file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        exit()

async def main():
    try:
        device_information = load_json("device_information.json")
        device_parameters = load_json("device_parameters.json")
        pass_through_parameters = load_json("pass_through_parameters.json")
        event_list = load_json("event_list.json")
        switch_event = load_json("switch_event.json")


        ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")


        cur_addr = get_device_id(ser=ser)
        mac_address = get_mac_address(ser=ser)

        print("Device Address: ", cur_addr)
        print("Mac Address: ", mac_address)


        new_device_addr=device_information.get("device_address") or "02"


        set_dev_add=[set_device_address(new_device_addr=new_device_addr, addr_to=cur_addr, mac_address=mac_address)]

        await run_command(ser =ser, command_arr=set_dev_add)

        addr_to=get_device_id(ser=ser)



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


        all_response=await run_command(ser=ser, command_arr=command_arr)

        for response in all_response:
            try:
                parse(response)
            except Exception as e:
                print("error at: ",response, "with error", e)

        ser.close()
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())

