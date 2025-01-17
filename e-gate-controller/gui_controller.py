import tkinter as tk
from tkinter import ttk

class ControlPanelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")
        self.root.geometry("550x800")

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
        tk.Button(upper_frame, text="Set Counter", bg="#add8e6", command=self.set_counter).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Passed Counter (Exit):", bg="#f0f8ff").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.exit_counter_spinbox = tk.Spinbox(upper_frame, from_=0, to=9999, width=10)
        self.exit_counter_spinbox.grid(row=1, column=2, padx=5, pady=5)

        separator = tk.Frame(upper_frame, height=2, relief="sunken", bg="#000000")
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

        text_area = tk.Text(lower_frame, wrap=tk.WORD, font=("Arial", 12), bg="#e6f7ff")
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(lower_frame, orient=tk.VERTICAL, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area.config(yscrollcommand=scrollbar.set)

    def create_input_output_tab(self):
        input_output_tab = ttk.Frame(self.notebook, style="TFrame")  # Apply the style here
        self.notebook.add(input_output_tab, text="Input & Output")

        upper_frame = tk.Frame(input_output_tab, bg="#f0f8ff")
        upper_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(upper_frame, text="Power Voltage:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(upper_frame).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(upper_frame, text="Battery Voltage:", bg="#f0f8ff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(upper_frame).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Motor(1):", bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Button(upper_frame, text="Turn On", bg="#add8e6", command=self.turn_on_motor_1).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(upper_frame, text="Rev. Turn On", bg="#add8e6", command=self.rev_turn_on_motor_1).grid(row=2, column=2, padx=5, pady=5)
        tk.Spinbox(upper_frame, from_=1, to=100, width=5).grid(row=2, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Motor(2):", bg="#f0f8ff").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Button(upper_frame, text="Turn On", bg="#add8e6", command=self.turn_on_motor_2).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(upper_frame, text="Rev. Turn On", bg="#add8e6", command=self.rev_turn_on_motor_2).grid(row=3, column=2, padx=5, pady=5)
        tk.Spinbox(upper_frame, from_=1, to=100, width=5).grid(row=3, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Entrance Indicator:", bg="#f0f8ff").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Button(upper_frame, text="D1", bg="#add8e6", command=self.d1).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(upper_frame, text="D2", bg="#add8e6", command=self.d2).grid(row=4, column=2, padx=5, pady=5)
        tk.Button(upper_frame, text="D3", bg="#add8e6", command=self.d3).grid(row=4, column=3, padx=5, pady=5)
        tk.Button(upper_frame, text="D4", bg="#add8e6", command=self.d4).grid(row=4, column=4, padx=5, pady=5)

        tk.Label(upper_frame, text="RGB LED:", bg="#f0f8ff").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Button(upper_frame, text="R", bg="#ff6347", command=self.r_led).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(upper_frame, text="G", bg="#32cd32", command=self.g_led).grid(row=5, column=2, padx=5, pady=5)
        tk.Button(upper_frame, text="B", bg="#1e90ff", command=self.b_led).grid(row=5, column=3, padx=5, pady=5)

        tk.Label(upper_frame, text="Relay:", bg="#f0f8ff").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        tk.Button(upper_frame, text="Relay 1", bg="#add8e6", command=self.relay_1).grid(row=6, column=1, padx=5, pady=5)

        tk.Label(upper_frame, text="Battery:", bg="#f0f8ff").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        tk.Label(upper_frame, text="Charging", bg="#f0f8ff").grid(row=7, column=1, padx=5, pady=5)

        # Lower Frame
        lower_frame = tk.Frame(input_output_tab, bg="#f0f8ff")
        lower_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollable Text Area
        text_area = tk.Text(lower_frame, wrap=tk.WORD, font=("Arial", 12), bg="#e6f7ff")
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(lower_frame, orient=tk.VERTICAL, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area.config(yscrollcommand=scrollbar.set)

    # Add corresponding functions
    def set_counter(self): pass
    def startup_set_start_position(self): pass
    def set_start_position(self): pass
    def open_for_entry(self): pass
    def always_open_for_entry(self): pass
    def close_for_entry(self): pass
    def open_for_exit(self): pass
    def always_open_for_exit(self): pass
    def close_for_exit(self): pass
    def lock_door(self): pass
    def unlock_door(self): pass
    def external_alarm(self): pass
    def cancel_external_alarm(self): pass
    def turn_on_motor_1(self): pass
    def rev_turn_on_motor_1(self): pass
    def turn_on_motor_2(self): pass
    def rev_turn_on_motor_2(self): pass
    def d1(self): pass
    def d2(self): pass
    def d3(self): pass
    def d4(self): pass
    def r_led(self): pass
    def g_led(self): pass
    def b_led(self): pass
    def relay_1(self): pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPanelApp(root)
    root.mainloop()
