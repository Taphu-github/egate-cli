import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import asyncio
import signal

class GateControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("eGate Controller")

        # Set the window to full screen
        self.attributes('-fullscreen', False)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.quit_fullscreen)

        # Create the tab control
        self.tab_control = ttk.Notebook(self)

        # Create tabs
        self.device_config_tab = ttk.Frame(self.tab_control)
        self.communication_parameters_tab = ttk.Frame(self.tab_control)
        self.control_parameters_tab = ttk.Frame(self.tab_control)
        self.input_output_tab = ttk.Frame(self.tab_control)
        self.status_control_tab = ttk.Frame(self.tab_control)

        # Add tabs to the tab control
        self.tab_control.add(self.device_config_tab, text="Device Configuration")
        self.tab_control.add(self.communication_parameters_tab, text="Communication Parameters")
        self.tab_control.add(self.control_parameters_tab, text="Control Parameters")
        self.tab_control.add(self.input_output_tab, text="Input And Output")
        self.tab_control.add(self.status_control_tab, text="Status And Control")


        self.tab_control.pack(expand=1, fill="both")

        # Status Control Tab
        self.create_status_control_tab()
        # Device Configuration Tab
        self.create_device_configuration_tab()
        # Communication Parameters Tab
        self.create_communication_parameters_tab()
        # Control Parameters Tab
        self.create_control_parameters_tab()
        # Input and Output Tab
        self.create_input_output_tab()

    def create_device_configuration_tab(self):
        # Device configuration tab layout
        frame = ttk.Frame(self.device_config_tab, padding=10)
        frame.pack(expand=True, fill='both')

        self.device_config_label = tk.Label(frame, text="Device Configuration", font=('Arial', 16))
        self.device_config_label.pack(pady=10)

        self.device_status_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80, font=('Arial', 10))
        self.device_status_area.pack(pady=10)

    def create_communication_parameters_tab(self):
        frame = ttk.Frame(self.communication_parameters_tab, padding=10)
        frame.pack(expand=True, fill='both')

    def create_control_parameters_tab(self):
        frame = ttk.Frame(self.control_parameters_tab, padding=10)
        frame.pack(expand=True, fill='both')

    def create_input_output_tab(self):
        frame = ttk.Frame(self.input_output_tab, padding=10)
        frame.pack(expand=True, fill='both')

    def create_status_control_tab(self):
        # Status control tab layout
        frame = ttk.Frame(self.status_control_tab, padding=10)
        frame.pack(expand=True, fill='both')

        # self.command_var = tk.StringVar(value=list(COMMANDS.keys())[0])
        command_label = tk.Label(frame, text="Select Command:", font=('Arial', 12))
        command_label.pack(pady=5)
        # self.command_menu = ttk.Combobox(frame, textvariable=self.command_var, values=list(COMMANDS.keys()), state='readonly')
        # self.command_menu.pack(pady=5)

        # self.send_button = ttk.Button(frame, text="Send Command", command=self.send_command)
        # self.send_button.pack(pady=10)

        self.response_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80, font=('Arial', 10))
        self.response_area.pack(pady=5)



#     def send_command(self):
#         command = self.command_var.get()

#         hex_command = COMMANDS.get(command)
#         if command:
#             self.response_area.delete(1.0, tk.END)
#             self.response_area.insert(tk.END, f"Sending command: {command} ({hex_command})\n")

#             # Indicate that the application is waiting for a reply
#             self.response_area.insert(tk.END, "Waiting for reply from the gate...\n")

#             # Update the GUI to show the current text
#             self.update_idletasks()

#             print("hexCommand sent", hex_command)
#             response = send_command_and_listen(command)
#             print("response hex", response)
#             self.response_area.insert(tk.END, f"Response: {response}\n")


    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

# def start_websocket_loop():
#     asyncio.run(websocket_handler())

# def signal_handler(sig, frame):
#     print('Shutting down...')
#     shutdown_event.set()
#     app.quit()

if __name__ == "__main__":
    app = GateControllerApp()

    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    # websocket_thread = threading.Thread(target=start_websocket_loop, daemon=True)
    # websocket_thread.start()

    app.mainloop()

    # if 'ser' in globals():
    #     ser.close()
    #     print("Serial connection closed.")
