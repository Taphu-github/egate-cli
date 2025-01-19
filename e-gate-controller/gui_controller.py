import tkinter as tk
from tkinter import ttk
from command_utils import get_and_create_command, generate_checksum, convert_deci_to_hex
from serial_utils import get_addr_to, connect_to_serial, run_command
import time

class ControlPanelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")
        self.root.geometry("550x800")

        self.serial_connection=connect_to_serial()
        self.addr_to="02"
        # self.addr_to=get_addr_to(self.serial_connection)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Set styles for background colors
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f8ff")  # Style for TFrame (ttk.Frame)

        self.create_status_control_tab()
        self.create_input_output_tab()

    def create_status_control_tab(self):
        status_control_tab = ttk.Frame(self.notebook, style="TFrame")  # Apply the style here
        self.notebook.add(status_control_tab, text="Status & Control")

        # Upper Frame
        upper_frame = tk.Frame(status_control_tab, bg="#f0f8ff")
        upper_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(upper_frame, text="Passed Counter (Entry):", bg="#f0f8ff").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        self.entry_counter_spinbox = tk.Spinbox(upper_frame, from_=0, to=9999, width=10)
        self.entry_counter_spinbox.grid(row=0, column=2, padx=5, pady=5)
        tk.Button(upper_frame, text="Refresh", bg="#add8e6", command=self.refresh_counter_status).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(upper_frame, text="Set Counter", bg="#add8e6", command=self.set_counter).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Passed Counter (Exit):", bg="#f0f8ff").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.exit_counter_spinbox = tk.Spinbox(upper_frame, from_=0, to=9999, width=10)
        self.exit_counter_spinbox.grid(row=1, column=2, padx=5, pady=5)

        separator = tk.Frame(upper_frame, height=2, relief="sunken")
        separator.grid(row=2, column=0, columnspan=10, sticky="ew", pady=10)

        buttons = [
            ("Startup Set Start Position", self.startup_set_start_position),
            ("Set Start Position", self.set_start_position),
            ("Open For Entry", self.open_for_entry),
            ("Always Open For Entry", self.always_open_for_entry),
            ("Close For Entry", self.close_for_entry),
            ("Open For Exit", self.open_for_exit),
            ("Always Open For Exit", self.always_open_for_exit),
            ("Close For Exit", self.close_for_exit),
            ("Lock Door", self.lock_door),
            ("Unlock Door", self.unlock_door),
            ("External Alarm", self.external_alarm),
            ("Cancel External Alarm", self.cancel_external_alarm),
        ]

        row = 3
        for i, (text, command) in enumerate(buttons):
            tk.Button(
                upper_frame,
                text=text,
                height=1,
                width=18,
                bg="#add8e6",
                command=command,
            ).grid(row=row, column=(i % 3) + 1, padx=5, pady=5)
            if i % 3 == 2:
                row += 1

        # Lower Frame
        lower_frame = tk.Frame(status_control_tab, bg="#f0f8ff")
        lower_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_area = tk.Text(lower_frame, wrap=tk.WORD, font=("Arial", 12), bg="#e6f7ff")
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(lower_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.config(yscrollcommand=scrollbar.set)

    def create_input_output_tab(self):
        input_output_tab = ttk.Frame(self.notebook, style="TFrame")  # Apply the style here
        self.notebook.add(input_output_tab, text="Input & Output")

        upper_frame = tk.Frame(input_output_tab, bg="#f0f8ff")
        upper_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Button(upper_frame, text="Refresh", bg="#f0f8ff", command=self.refresh_input_output).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        tk.Label(upper_frame, text="Power Voltage:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.power_voltage= tk.Entry(upper_frame)
        self.power_voltage.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(upper_frame, text="Battery Voltage:", bg="#f0f8ff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.battery_voltage= tk.Entry(upper_frame)
        self.battery_voltage.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Entrance Indicator:", bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.d1_button=tk.Button(upper_frame, text="D1", bg="white", command=self.d1)
        self.d1_button.grid(row=2, column=1, padx=5, pady=5)

        self.d2_button=tk.Button(upper_frame, text="D2", bg="white", command=self.d2)
        self.d2_button.grid(row=2, column=2, padx=5, pady=5)

        self.d3_button=tk.Button(upper_frame, text="D3", bg="white", command=self.d3)
        self.d3_button.grid(row=2, column=3, padx=5, pady=5)

        self.d4_button=tk.Button(upper_frame, text="D4", bg="white", command=self.d4)
        self.d4_button.grid(row=2, column=4, padx=5, pady=5)

        tk.Label(upper_frame, text="RGB LED:", bg="#f0f8ff").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.r_button=tk.Button(upper_frame, text="R", bg="white", command=self.r_led)
        self.r_button.grid(row=3, column=1, padx=5, pady=5)
        self.g_button=tk.Button(upper_frame, text="G", bg="white", command=self.g_led)
        self.g_button.grid(row=3, column=2, padx=5, pady=5)
        self.b_button=tk.Button(upper_frame, text="B", bg="white", command=self.b_led)
        self.b_button.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Relay:", bg="#f0f8ff").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.relay_button=tk.Button(upper_frame, text="Relay 1", bg="#f0f8ff", command=self.relay_1)
        self.relay_button.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(upper_frame, text="Battery:", bg="#f0f8ff").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.charging_button=tk.Button(upper_frame, text="Charging", bg="#f0f8ff", command=self.charging)
        self.charging_button.grid(row=5, column=1, padx=5, pady=5)

        # Lower Frame
        lower_frame = tk.Frame(input_output_tab, bg="#f0f8ff")
        lower_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollable Text Area
        self.input_output_text_area = tk.Text(lower_frame, wrap=tk.WORD, font=("Arial", 12), bg="#e6f7ff")
        self.input_output_text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(lower_frame, orient=tk.VERTICAL, command=self.input_output_text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_output_text_area.config(yscrollcommand=scrollbar.set)

    # Add corresponding functions
    def refresh_counter_status(self):
        #AA 00 01 02 00 02 08 FF 00 00 00 00 00 00 00 0C
        #AA 00 01 02 00 02 08 01 00 00 00 0A 00 00 0A 22
        #AA 00 01 02 00 02 08 FF 00 00 00 00 00 00 00 0C
        command="00 01 02 00 "+self.addr_to+" 08 FF 00 00 00 00 00 00 00"
        command="AA "+command+" "+generate_checksum(command)

        response=run_command(ser=self.serial_connection, command=command)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        if response:
            formatted_response=[response[0][i: i+2] for i in range(0,32,2)]

            entry_passed_counter="".join(formatted_response[9:12])
            entry_passed_counter_int=int(entry_passed_counter, 16)
            exit_passed_counter="".join(formatted_response[12:15])
            exit_passed_counter_int=int(exit_passed_counter, 16)
            self.entry_counter_spinbox.delete(0, tk.END)
            self.entry_counter_spinbox.insert(0, entry_passed_counter_int)

            self.exit_counter_spinbox.delete(0, tk.END)
            self.exit_counter_spinbox.insert(0, exit_passed_counter_int)

            self.text_area.insert(tk.END, f"\nRESPONSE: "+str(response))
        else:
            self.text_area.insert(tk.END, "\nError: ")

    def refresh_input_output(self):
        #AA 00 01 02 04 02 08 FF 00 00 00 00 00 00 00 10
        output_refresh_command="00 01 02 04 "+self.addr_to+" 08 FF 00 00 00 00 00 00 00"
        output_refresh_command="AA "+output_refresh_command+" "+generate_checksum(output_refresh_command)
        output_refresh_response=run_command(ser=self.serial_connection, command=output_refresh_command)

        self.input_output_text_area.insert(tk.END, "\nINPUT: "+output_refresh_command)
        if output_refresh_response:

            #AA 00 02 12 04 00 08 00 00 00 00 01 04 00 00 25


            #CID1-2: 12 04
            #D_4: d1:01, d2:02, d3:04, d4:08
            #D_5: r:01, g:02, b:03
            #D-6: 01, 00 [relay]
            #D-7: 01, 00 [charging]
            formatted_output_response=[output_refresh_response[0][i:i+2] for i in range(0,32,2)]
            self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_output_response))

            d_4=formatted_output_response[11]
            dd=[8, 4, 2, 1]
            dd_output=self.calculate(d_4, dd)

            self.d4_button.config(bg="green") if dd_output[0]==1 else self.d4_button.config(bg="red")

            if dd_output[1]==1:
                self.d3_button.config(bg="green")
            else:
                self.d3_button.config(bg="red")

            if dd_output[2]==1:
                self.d2_button.config(bg="green")
            else:
                self.d2_button.config(bg="red")

            if dd_output[3]==1:
                self.d1_button.config(bg="green")
            else:
                self.d1_button.config(bg="red")

            d_5=formatted_output_response[12]
            rgb=[3, 2, 1]
            rgb_output=self.calculate(d_5,rgb)

            if rgb_output[0]==1:
                self.b_button.config(bg="green")
            else:
                self.b_button.config(bg="red")

            if rgb_output[1]==1:
                self.g_button.config(bg="green")
            else:
                self.g_button.config(bg="red")

            if rgb_output[2]==1:
                self.r_button.config(bg="green")
            else:
                self.r_button.config(bg="red")

            d_6=formatted_output_response[13]
            if d_6=="01":
                self.relay_button.config(bg="green")
            else:
                self.relay_button.config(bg="red")

            d_7=formatted_output_response[14]
            if d_7=="01":
                self.charging_button.config(bg="green")
            else:
                self.charging_button.config(bg="red")
        else:
            self.input_output_text_area.insert(tk.END, "\nError: Input Refresh Command Unsuccesful")



        time.sleep(0.5)

        input_refresh_command="00 01 02 02 "+self.addr_to+" 01 00 00 00 00 00 00 00 00"
        input_refresh_command="AA "+input_refresh_command+" "+generate_checksum(input_refresh_command)
        input_refresh_response=run_command(ser=self.serial_connection, command=input_refresh_command)

        self.input_output_text_area.insert(tk.END, "\nINPUT: "+input_refresh_command)
        if input_refresh_response:
            #AA 00 01 02 02 02 01 00 00 00 00 00 00 00 00 08
            #AA 00 02 12 02 00 08 00 00 00 00 00 EE 00 C2 CE
            #CID1-2: 12 02
            #D4-5: Power Voltage
            #D6-7: Battery Voltage
            formatted_input_response=[input_refresh_response[0][i:i+2] for i in range(0,32,2)]
            self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_input_response))
            power_voltage=formatted_input_response[11]+formatted_input_response[12]
            battery_voltage=formatted_input_response[13]+formatted_input_response[14]

            power_voltage=int(power_voltage, 16)
            battery_voltage=int(battery_voltage, 16)
            self.power_voltage.delete(0, tk.END)
            self.power_voltage.insert( 0,str(power_voltage)+" V")
            self.battery_voltage.delete(0, tk.END)
            self.battery_voltage.insert(0, str(battery_voltage)+" V")

        else:
            self.input_output_text_area.insert(tk.END, "\nError: Ouput Refresh Command Unsuccesful")

    def calculate(self,hex_val,dic):
        int_val=int(hex_val, 16)
        # print(int_val)
        return_arr=[]
        for i in range(len(dic)):
            if int_val>=dic[i]:
                int_val-=dic[i]
                return_arr.append(1)
            else:
                return_arr.append(0)
        print(return_arr)
        return return_arr

    def set_counter(self):
        entry_counter=self.entry_counter_spinbox.get()
        exit_counter=self.exit_counter_spinbox.get()

        entry_counter_hex=convert_deci_to_hex(int(entry_counter), 3)
        enxit_counter_hex=convert_deci_to_hex(int(exit_counter), 3)
        #AA 00 01 02 00 02 08 01 00 00 00 0A 00 00 0A 22
        command ="00 01 02 00 "+self.addr_to+" 08 01 00 "+entry_counter_hex+" "+enxit_counter_hex
        command = "AA "+command+" "+generate_checksum(command)
        #AA 00 01 01 02 02 08 01 00 00 00 00 00 00 00
        #AA 00 01 01 02 02 08 A1 02 F0 A1 B4 A5 96 87 B8 - for changing mac-address

        #AA 00 01 02 00 02 08 01 00 00 00 00 00 00 00 0E
        self.text_area.insert(tk.END, "\nINPUT: "+command)

        response=run_command(ser=self.serial_connection, command=command)

        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, f"\nRESPONSE: "+" ".join(formatted_response))
            if " ".join(formatted_response[9:12])==entry_counter_hex and " ".join(formatted_response[12:15])==enxit_counter_hex:

                self.text_area.insert(tk.END, f"\nSUCCESS: entery and exit passed counter set to {entry_counter} and {exit_counter}")
        else:
            self.text_area.insert(tk.END, "ERROR: ")

    def startup_set_start_position(self):
        command=get_and_create_command(command_name="Startup Set Start Position", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+formatted_response)
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def set_start_position(self):
        command=get_and_create_command(command_name="Set Start Position", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+formatted_response)
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def open_for_entry(self):
        command=get_and_create_command(command_name="Open For Entry", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def always_open_for_entry(self):
        command=get_and_create_command(command_name="Always Open For Entry", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def close_for_entry(self):
        command=get_and_create_command(command_name="Close For Entry", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def open_for_exit(self):
        command=get_and_create_command(command_name="Open For Exit", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def always_open_for_exit(self):
        command=get_and_create_command(command_name="Always Open For Exit", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def close_for_exit(self):
        command=get_and_create_command(command_name="Close For Exit", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def lock_door(self):
        command=get_and_create_command(command_name="Lock", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def unlock_door(self):
        command=get_and_create_command(command_name="Unlock", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def external_alarm(self):
        command=get_and_create_command(command_name="External Alarm", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def cancel_external_alarm(self):
        command=get_and_create_command(command_name="Cancel External Alarm", addr_to=self.addr_to)
        self.text_area.insert(tk.END, "\nINPUT: "+command)
        response=run_command(ser=self.serial_connection, command=command)
        if response:
            formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
            self.text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
        else:
            self.text_area.insert(tk.END, "\nERROR: ")

    def d1(self):
        if self.d1_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 03 01 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 03 01 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.d1_button["bg"] == "red":
                    self.d1_button.config(bg="green")
                else:
                    self.d1_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def d2(self):
        if self.d2_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 03 02 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 03 02 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.d2_button["bg"] == "red":
                    self.d2_button.config(bg="green")
                else:
                    self.d2_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def d3(self):
        if self.d3_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 03 03 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 03 03 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.d3_button["bg"] == "red":
                    self.d3_button.config(bg="green")
                else:
                    self.d3_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def d4(self):
        if self.d4_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 03 04 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 03 04 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.d4_button["bg"] == "red":
                    self.d4_button.config(bg="green")
                else:
                    self.d4_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def r_led(self):
        if self.r_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 04 01 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 04 01 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.r_button["bg"] == "red":
                    self.r_button.config(bg="green")
                else:
                    self.r_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def g_led(self):
        if self.g_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 04 02 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 04 02 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.g_button["bg"] == "red":
                    self.g_button.config(bg="green")
                else:
                    self.g_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "HINT: Refresh First")

    def b_led(self):
        if self.b_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 04 03 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 04 03 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.b_button["bg"] == "red":
                    self.b_button.config(bg="green")
                else:
                    self.b_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")

    def relay_1(self):
        if self.relay_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 05 01 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 05 01 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.relay_button["bg"] == "red":
                    self.relay_button.config(bg="green")
                else:
                    self.relay_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:

                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "Refresh First")

    def charging(self):
        if self.charging_button["bg"] == "red":
            command="00 01 02 04 "+self.addr_to+" 08 05 01 01 01 00 00 00 00"
        else:
            command="00 01 02 04 "+self.addr_to+" 08 05 01 00 01 00 00 00 00"

        if command:
            command="AA "+command+" "+generate_checksum(command)
            self.input_output_text_area.insert(tk.END, "\nINPUT: "+command)
            response=run_command(ser=self.serial_connection, command=command)

            if response:
                if self.charging_button["bg"] == "red":
                    self.charging_button.config(bg="green")
                else:
                    self.charging_button.config(bg="red")
                formatted_response=[response[0][i:i+2] for i in range(0,32,2)]
                self.input_output_text_area.insert(tk.END, "\nRESPONSE: "+" ".join(formatted_response))
            else:
                self.input_output_text_area.insert(tk.END, "\nERROR: ")
        else:
            self.input_output_text_area.insert(tk.END, "\nHINT: Refresh First")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPanelApp(root)
    root.mainloop()
