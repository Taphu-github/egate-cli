import tkinter as tk
from tkinter import scrolledtext, ttk
from gate_controller import COMMANDS, send_command_and_listen
import threading
import asyncio
import signal
# from passport_reader import websocket_handler, shutdown_event

# class GateControllerApp(tk.Tk):
class GateControllerApp:
    def __init__(self):
        pass
        # super().__init__()
        # self.title("eGate Controller")

        # # Set the window to full screen
        # self.attributes('-fullscreen', False)
        # self.bind("<F11>", self.toggle_fullscreen)
        # self.bind("<Escape>", self.quit_fullscreen)

        # # Create the tab control
        # self.tab_control = ttk.Notebook(self)

        # # Create tabs
        # self.status_control_tab = ttk.Frame(self.tab_control)
        # self.device_config_tab = ttk.Frame(self.tab_control)

        # # Add tabs to the tab control
        # self.tab_control.add(self.status_control_tab, text="Status Control")
        # self.tab_control.add(self.device_config_tab, text="Device Configuration")

        # self.tab_control.pack(expand=1, fill="both")

        # # Status Control Tab
        # self.create_status_control_tab()

        # # Device Configuration Tab
        # self.create_device_configuration_tab()

    # def create_status_control_tab(self):
    #     # Status control tab layout
    #     frame = ttk.Frame(self.status_control_tab, padding=10)
    #     frame.pack(expand=True, fill='both')

    #     self.command_var = tk.StringVar(value=list(COMMANDS.keys())[0])
    #     command_label = tk.Label(frame, text="Select Command:", font=('Arial', 12))
    #     command_label.pack(pady=5)
    #     self.command_menu = ttk.Combobox(frame, textvariable=self.command_var, values=list(COMMANDS.keys()), state='readonly')
    #     self.command_menu.pack(pady=5)

    #     self.send_button = ttk.Button(frame, text="Send Command", command=self.send_command)
    #     self.send_button.pack(pady=10)

    #     self.response_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80, font=('Arial', 10))
    #     self.response_area.pack(pady=5)

    # def create_device_configuration_tab(self):
    #     # Device configuration tab layout
    #     frame = ttk.Frame(self.device_config_tab, padding=10)
    #     frame.pack(expand=True, fill='both')

    #     self.device_config_label = tk.Label(frame, text="Device Configuration", font=('Arial', 16))
    #     self.device_config_label.pack(pady=10)

    #     self.device_status_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80, font=('Arial', 10))
    #     self.device_status_area.pack(pady=10)

    def menu(self):
        exit_status=False
        COMMANDS = {
            'OPEN FOR ENTRY': 'AA00010200020800000000000000000D',
            'OPEN FOR EXIT': 'AA000102000208000300000000000010',
            'CLOSE FOR ENTRY': 'AA00010200020800020000000000000F',
            'CLOSE FOR EXIT': 'AA000102000208000500000000000012',
            'OPEN ALWAYS FOR ENTRY': 'AA00010200020800010000000000000E',
            'OPEN ALWAYS FOR EXIT': 'AA000102000208000400000000000011',
            'SEND ALARM': 'AA000102000208020100000000000010',
            'STOP ALARM': 'AA00010200020802000000000000000F'
        }
        while not exit_status:
            print("*****************EGATE-CONTROLLER***********************")
            print("Choose the option:\n1 for 'OPEN FOR ENTRY'\n2 for 'OPEN FOR EXIT'\n3 for 'CLOSE FOR ENTRY'\n4 for 'CLOSE FOR EXIT'\n5 for 'OPEN ALWAYS FOR ENTRY'\n6 for 'OPEN ALWAYS FOR EXIT'\n7 for 'SEND ALARM'\n8 for 'STOP ALARM'")
            option=int(input("INPUT: "))
            if option==1:
                command="OPEN FOR ENTRY"
            elif option==2:
                command="OPEN FOR EXIT"
            elif option==3:
                command="CLOSE FOR ENTRY"
            elif option==4:
                command="CLOSE FOR EXIT"
            elif option==5:
                command="OPEN ALWAYS FOR ENTRY"
            elif option==6:
                command="OPEN ALWAYS FOR EXIT"
            elif option==7:
                command="SEND ALARM"
            elif command==8:
                command="STOP ALARM"
            else:
                print("Wrong Message")
                continue
            self.send_command(command=command)




    def send_command(self, command):
        # command = self.command_var.get()

        hex_command = COMMANDS.get(command)
        if command:
            # self.response_area.delete(1.0, tk.END)
            print(f"Sending command: {command} ({hex_command})\n")
            # self.response_area.insert(tk.END, f"Sending command: {command} ({hex_command})\n")

            # Indicate that the application is waiting for a reply
            print("Waiting for reply from the gate...\n")
            # self.response_area.insert(tk.END, "Waiting for reply from the gate...\n")

            # Update the GUI to show the current text
            # self.update_idletasks()

            print("hexCommand sent", hex_command)
            response = send_command_and_listen(command)
            print("response hex", response)
            # self.response_area.insert(tk.END, f"Response: {response}\n")


    # def toggle_fullscreen(self, event=None):
    #     self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    # def quit_fullscreen(self, event=None):
    #     self.attributes('-fullscreen', False)

# def start_websocket_loop():
#     asyncio.run(websocket_handler())

def signal_handler(sig, frame):
    print('Shutting down...')
    # shutdown_event.set()
    app.quit()

if __name__ == "__main__":
    # shutdown_event = asyncio.Event()
    app = GateControllerApp()

    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    # websocket_thread = threading.Thread(target=start_websocket_loop, daemon=True)
    # websocket_thread.start()

    # app.mainloop()
    app.menu()

    if 'ser' in globals():
        ser.close()
        print("Serial connection closed.")
