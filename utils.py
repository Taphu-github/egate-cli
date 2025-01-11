import json
import time

def generate_payload(data):
    pass

def generate_checksum(data):
    hex_pairs=data.split(" ")

    sums= 0
    for hexi in hex_pairs[1:]:
        sums+=int(hexi, 16)

    hex_val=hex(sums)
    meaningful_val_of_hex=hex_val.split("x")[1]

    if len(meaningful_val_of_hex)==1:
        return "0"+meaningful_val_of_hex

    elif len(meaningful_val_of_hex)==2:
        return meaningful_val_of_hex

    else:
        return meaningful_val_of_hex[-2:]

def convert_hex_to_num(data):
    pass

def convert_num_to_hex(data):
    pass

def chunk_bytearray(byte_array, chunk_size=16):
    """
    Breaks a byte array into chunks of `chunk_size` bytes each.

    :param byte_array: The byte array to be chunked.
    :param chunk_size: The size of each chunk in bytes.
    :return: List of byte array chunks.
    """
    chunks = [byte_array[i:i + chunk_size] for i in range(0, len(byte_array), chunk_size)]
    # Convert each chunk to a hex string
    hex_chunks = [''.join(f'{byte:02X}' for byte in chunk) for chunk in chunks]

    return hex_chunks

def get_device_id(ser):

    with open("commands.json", "r") as file:
        data = json.load(file)

    if not data:
        print("there is no data")

    checksum=generate_checksum(data["CHECKING ONLINE UNIT"])
    command_hex = data["CHECKING ONLINE UNIT"]+" "+checksum

    command_bytes=bytes.fromhex(command_hex)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 6:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        time.sleep(0.2)

    # if not res
    response_chunks = chunk_bytearray(response)

    if not response_chunks:
        print("There has been a problem with the command")
    # print(response_chunks)
    return response_chunks[0][4:6]

def run_commands(ser, hex_commands):
    commands=hex_commands.replace()
    checksum = generate_checksum(hex_commands)
    command_hex= hex_commands+" "+checksum

    command_bytes=bytes.fromhex(command_hex)
    ser.write(command_bytes)

    start_time = time.time()
    response = bytearray()

    while time.time() - start_time < 6:
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        time.sleep(0.2)

    # if not res
    response_chunks = chunk_bytearray(response)
    print(response_chunks)

'''
ADR_S: !!
CID1: @@
CID2: ##
ADR_T: $$
DLC: %%
DATA_0: ^^
DATA_1: &&
DATA_2: **
DATA_3: <<
DATA_4: >>
DATA_5: ??
DATA_6: --
DATA_7: ++
'''
def replace_values(
    command,
    ADR_T=None, ADR_S=None, CID1=None, CID2=None, DLC=None,
    DATA0=None, DATA1=None, DATA2=None, DATA3=None,
    DATA4=None, DATA5=None, DATA6=None, DATA7=None
):
    com = command  # Start with the original command string

    # Replace placeholders with their respective values if provided
    if ADR_S:
        com = com.replace("!!", ADR_S)
    if ADR_T:
        com = com.replace("$$", ADR_T)
    if CID1:
        com = com.replace("@@", CID1)
    if CID2:
        com = com.replace("##", CID2)
    if DLC:
        com = com.replace("%%", DLC)
    if DATA0:
        com = com.replace("^^", DATA0)
    if DATA1:
        com = com.replace("&&", DATA1)
    if DATA2:
        com = com.replace("**", DATA2)
    if DATA3:
        com = com.replace("<<", DATA3)
    if DATA4:
        com = com.replace(">>", DATA4)
    if DATA5:
        com = com.replace("??", DATA5)
    if DATA6:
        com = com.replace("--", DATA6)
    if DATA7:
        com = com.replace("++", DATA7)

    return com

def decrypt_response(response):
    for res in response:
        if res[6:8]=="11" and res[8:10]=="0A":
            #decryption for status control
            '''
                D[0]= Main ACK Device [(Checked, 01), (Unchecked, 00)]
            '''
            pass
        if res[6:8]=="11" and res[8:10]=="08":
            #decryption for status control
            '''
                When D[1]==00, 01, 02, 03
                    D[2]-D[7]-> stringencoded to utf-8 and converted to hex and transfered
            '''
            pass

        if res[6:8]=="12" and res[8:10]=="04":
            #decryption for status control
            '''
                D[4]: Intrance Indicator [(D1, 01),(D2, 02), (D3, 04), (D4,08), (None, 00)]
                D[5]: RGB LED [(R,01),(G,02),(B,03),(None, 00)]
                D[6]: Relay [(Checked, 01), (Unchecked, 00)]
                D[7]: Charging [(Checked, 00), (Unchecked, FF)]
            '''
            pass


        if res[6:8]=="11" and res[8:10]=="0D":
            #decryption for status control
            '''
                D[0]=FF->Get, 00->Set
                D[1]=Year
                D[2]=Month
                D[3]=Days
                D[4]=Hours
                D[5]=Minutes
                D[6]=Seconds
            '''
            pass
        if res[6:8]=="12" and res[8:10]=="00":
            #decryption for status control
            '''
                D[0]== [(Gate was closed(free), 00),(Gate was closed(Fire alarm))]
            '''
            pass

        if res[6:8]=="12" and res[8:10]=="02":
            '''
                when D[1]==00 and D[0]==00,
                    D[4] and D[5]= Power Supply Voltage
                    D[6] and D[7]= Battery Volatge
            '''
            pass



        if (res[6:8]=="11" and res[8:10]=="12") or (res[6:8]=="11" and res[8:10]=="11"):
            #decyrption for control parameters
            #decryption for device parameter and pass through parameters and event list and switch list
            '''
                when D[1]==00 and D[0]==00,
                    D[2]==Entry Open Door Motor Speed for Motor 1
                    D[3]==Entry Open Door Motor Speed for Motor 2
                    D[4]==Entry Close Door Motor Speed for Motor 1
                    D[5]==Entry Close Door Motor Speed for Motor 2
                    D[6]==Exit Open Door Motor Speed for Motor 1
                    D[7]==Exit Open Door Motor Speed for Motor 2

                when D[1]==01 and D[0]==00,
                    D[2]==Exit Close Door Motor Speed for Motor 1
                    D[3]==Exit Close Door Motor Speed for Motor 2
                    D[4]==Motor Overcurrent Protection
                    D[5]==IR Sensor Type [(PNP (Hi Trig),00),(NPN (Lo Trig), 01)]
                    D[6]==IR Logic [(Disabled, 00), (Local Interface, 01), ([External For Entry, (0, 40), (1, 41), ...]), ([External For Exit, (0, 80), (1, 81), ..]), ([External For Both, (0, C0), (1, C1), ...]) ]
                    D[7]==Relay For Passed Counter [(Entry, 01), (Disabled, 00), (Exit, 02), (Both, 03)],

                when D[1]==02 and D[0]==00,
                    D[2]==Barriers Count [(Single,01 , (Double, 00))]
                    D[3]==IR Sensitivity
                    D[4]==[Normally Open Direction [(Exit, 12), (Entry, 02)], Action On Power Lost [(None, 00),(Closed, 01),(Always Open For Entry, 02),(Always Open For Exit, 03)  ]
                    D[5]==Base Speed Level for Motor 1
                    D[6]==Base Speed Level for Motor 2
                    D[7]==Gate Mode [("Normally Closed, Both Card", 01), (Normally Closed, Both Free, 02),(Normally Closed, Both Reject,03 ), ("Normally Closed, Entry Card & Exit Free",04), ("Normally Closed, Entry Card & Exit Reject",05),("Normally Closed, Entry Free & Exit Card",06), ("Normally Closed, Entry Free & Exit Reject",07), ("Normally Closed, Entry Reject & Exit Free",08),("Normally Closed, Entry Reject & Exit Card",09), ("Normally Open, Both Free, ",10),("Normally Closed, Both Card",11),("Normally Open, Entry Free & Exit Card",12), ("Normally Open, Entry Card & Exit Free",13)]

                When D[1]==03 and D[0]==00,
                    D[2]==Authorized With Memory [(Both Disabled, 00),(Entry Allowed, 01),(Exit Allowed, 02), (Both Allowed , 03) ]
                    D[3]==Maxium Passage Time
                    D[4]==Authorized Open Door Delay
                    D[5]==Close Door Delay
                    D[6]==Authroized In Lane ([Unchecked, 00),(Checked, 01)])
                    D[7]==Passage End IR Check at ([(Safety, 01), (Exit, 00)])

                When D[1]==04 and D[0]==00,
                    D[2]==Automatic Report Status [(Uncheck, 00), (Check, 01)]
                    D[3]==Intrusion Alarm [(None, F0), (Alarm, 01), (Alarm & Closed Door, 02)]
                    D[4]==Reverse Alarm [(None, F0), (Alarm, 01), (Alarm & Closed Door, 02)]
                    D[5]==Tailing Alarm [(None, F0), (Alarm, 01), (Alarm & Closed Door, 02)]
                    D[6]==Power On Self Check [(Uncheck, 00), (Check, 01)]
                    D[7]==

                When D[1]==00 and D[0]==01,
                    D[2]= Normally Closed, Both Card [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[3]= Normally Closed, Both Free [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[4]= Normally Closed, Both Reject [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[5]= Normally Closed, Entry Card, Exit Free [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[6]= Normally Closed, Entry Card, Exit Reject [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[7]= Normally Closed, Entry Card, Exit Card [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]

                When D[1]==01 and D[0]==01,
                    D[2]= Normally Closed, Entry Card, Exit Reject [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[3]= Normally Closed, Entry Card, Exit Free [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[4]= Normally Closed, Entry Card, Exit Card [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[5]= Normally Open, Both Free [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[6]= Normally Open, Both Card [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[7]= Normally Open, Entry Card, Exit Card [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]

                When D[1]==02 and D[0]==01,
                    D[2]= Normally Open, Entry Card, Exit Free [(D1, 01), (D2, 02), (D3, 04), (D4, 08), (R, 16), (G, 32), (B, 64) ]
                    D[3]=
                    D[4]= Automatic Switch 1, On Trigger [(None, 00), (Idle(Default State),01 ),(Open For Entry, 02 ), (Always Open For Entry, 03), (Close For Entry, 04), (Open For Exit, 05), (Always Open For Exit, 06),(Close For Exit, 07))], On Release  [(None, 00), (Idle(Default State),+16 ),(Open For Entry, +16*2 ), (Always Open For Entry, +16*3), (Close For Entry, +16*4), (Open For Exit, +16*5), (Always Open For Exit, +16*6),(Close For Exit, +16*7))]
                    D[5]= Automatic Switch 2, On Trigger [(None, 00), (Idle(Default State),01 ),(Open For Entry, 02 ), (Always Open For Entry, 03), (Close For Entry, 04), (Open For Exit, 05), (Always Open For Exit, 06),(Close For Exit, 07))], On Release  [(None, 00), (Idle(Default State),+16 ),(Open For Entry, +16*2 ), (Always Open For Entry, +16*3), (Close For Entry, +16*4), (Open For Exit, +16*5), (Always Open For Exit, +16*6),(Close For Exit, +16*7))]
                    D[6]= Fire Alarm, On Trigger [(None, 00), (Idle(Default State),01 ),(Open For Entry, 02 ), (Always Open For Entry, 03), (Close For Entry, 04), (Open For Exit, 05), (Always Open For Exit, 06),(Close For Exit, 07))], On Release  [(None, 00), (Idle(Default State),+16 ),(Open For Entry, +16*2 ), (Always Open For Entry, +16*3), (Close For Entry, +16*4), (Open For Exit, +16*5), (Always Open For Exit, +16*6),(Close For Exit, +16*7))]
                    D[7]= Manual Switch, On Trigger [(None, 00), (Idle(Default State),01 ),(Open For Entry, 02 ), (Always Open For Entry, 03), (Close For Entry, 04), (Open For Exit, 05), (Always Open For Exit, 06),(Close For Exit, 07))], On Release  [(None, 00), (Idle(Default State),+16 ),(Open For Entry, +16*2 ), (Always Open For Entry, +16*3), (Close For Entry, +16*4), (Open For Exit, +16*5), (Always Open For Exit, +16*6),(Close For Exit, +16*7))]

                When D[1]==03 and D[0]==01,
                    D[2]=
                    D[3]=
                    D[4]=
                    D[5]=
                    D[6]=
                    D[7]=

                When D[1]==04 and D[0]==01,
                    D[2]=
                    D[3]=
                    D[4]=
                    D[5]=
                    D[6]=
                    D[7]=

                When D[1]==00 and D[0]==02,
                    D[3]==Open For Entry, Entrance Indicator [(None, F0), (Black(All Off), 00), (D1,01), (D2,02), (D1+D2,03), (D3,04), (D3+D1,05), (D3+D1+D2,06), (D4,07), (D4+D1,08), (D4+D1+D2,09), (D4+D1+D2+D3,10)]
                    D[4]==Open For Entry, Entrance Indicator, Blink On Delay
                    D[5]==Open For Entry, Entrance Indicator, Blink Off Delay
                    D[6]==Open For Entry, Entrance Indicator, Repetitions
                    D[7]==Open For Entry, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==01 and D[0]==02,
                    D[2]=Open For Entry, RGD LED, Blink On Delay
                    D[3]=Open For Entry, RGD LED, Blink Off Delay
                    D[4]=Open For Entry, RGD LED, Repetitions
                    D[5]=Open For Entry, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]=Open For Entry, Relay, Blink On Delay
                    D[7]=Open For Entry, Relay, Blink Off Delay

                When D[1]==02 and D[0]==02,
                    D[2]= Open For Entry, Relay, Repetitions
                    D[3]= Open For Entry, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Open For Entry, Voice Module, Repetitions
                    D[6]= Close For Entry, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= Close For Entry, Entrance Indicator, Blink On Delay

                When D[1]==03 and D[0]==02,
                    D[2]= Close For Entry, Entrance Indicator, Blink Off Delay
                    D[3]= Close For Entry, Entrance Indicator, Repetitions
                    D[4]= Close For Entry, RGB LED  [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= Close For Entry, RGD LED, Blink On Delay
                    D[6]= Close For Entry, RGD LED, Blink Off Delay
                    D[7]= Close For Entry, RBG LED, Repetitions

                When D[1]==04 and D[0]==02,
                    D[2]= Close For Entry, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= Close For Entry, Relay, Blink On Delay
                    D[4]= Close For Entry, Relay, Blink Off Delay
                    D[5]= Close For Entry, Relay, Repetitions
                    D[6]= Close For Entry, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= Close For Entry, Voice Module, Repetitions

                When D[1]==00  and D[0]==03,
                    D[2]= Open For Exit, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[3]= Open For Exit, Entrance Indicator, Blink On Delay
                    D[4]= Open For Exit, Entrance Indicator, Blink Off Delay
                    D[5]= Open For Exit, Entrance Indicator, Repetitions
                    D[6]=
                    D[7]= Open For Exit, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==01  and D[0]==03,
                    D[2]= Open For Exit, RGD LED, Blink On Delay
                    D[3]= Open For Exit, RGD LED, Blink Off Delay
                    D[4]= Open For Exit, RGD LED, Repetitions
                    D[5]= Open For Exit, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]= Open For Exit, Relay, Blink On Delay
                    D[7]= Open For Exit, Relay, Blink Off Delay

                When D[1]==02  and D[0]==03,
                    D[2]= Open For Exit, Relay, Repetitions
                    D[3]= Open For Exit, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Open For Exit, Voice Module, Repetitions
                    D[5]=
                    D[6]= Close For Exit, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= Close For Exit, Entrance Indicator, Blink On Delay

                When D[1]==03  and D[0]==03,
                    D[2]= Close For Exit, Entrance Indicator, Blink Off Delay
                    D[3]= Close For Exit, Entrance Indicator, Repetitions
                    D[4]= Close For Exit, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= Close For Exit, RGD LED, Blink On Delay
                    D[6]= Close For Exit, RGD LED, Blink Off Delay
                    D[7]= Close For Exit, RGD LED, Blink Repetitions

                When D[1]==04  and D[0]==03,
                    D[2]= Close For Exit, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= Close For Exit, Relay, Blink On Delay
                    D[4]= Close For Exit, Relay, Blink Off Delay
                    D[5]= Close For Exit, Relay, Blink Repitions
                    D[6]= Close For Exit, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= Close For Exit, Voice Module, Repetitions

                When D[1]==00 and D[0]==04,
                    D[2]=
                    D[3]= Device Lost Power, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[4]= Device Lost Power, Entrance Indicator, Blink On Delay
                    D[5]= Device Lost Power, Entrance Indicator, Blink Off Delay
                    D[6]= Device Lost Power, Entrance Indicator, Repetitions
                    D[7]= Device Lost Power, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==02 and D[0]==04,
                    D[2]= Device Lost Power, RGD LED, Blink On Delay
                    D[3]= Device Lost Power, RGD LED, Blink Off Delay
                    D[4]= Device Lost Power, RGD LED, Blink Repetitions
                    D[5]= Device Lost Power, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]= Device Lost Power, Relay, Blink On Delay
                    D[7]= Device Lost Power, Relay, Blink Off Delay

                When D[1]==03 and D[0]==04,
                    D[2]= Device Lost Power, Relay, Blink Repitions
                    D[3]= Device Lost Power, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Device Lost Power, Voice Module, Repetitions
                    D[5]=
                    D[6]= External Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= External Alarm, Entrance Indicator, Blink On Delay

                When D[1]==03 and D[0]==04,
                    D[2]= External Alarm, Entrance Indicator, Blink Off Delay
                    D[3]= External Alarm, Entrance Indicator, Repetitions
                    D[4]= External Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= External Alarm, RGD LED, Blink On Delay
                    D[6]= External Alarm, RGD LED, Blink Off Delay
                    D[7]= External Alarm, RGD LED, Blink Repetitions

                When D[1]==04 and D[0]==04,
                    D[2]= External Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= External Alarm, Relay, Blink On Delay
                    D[4]= External Alarm, Relay, Blink Off Delay
                    D[5]= External Alarm, Relay, Blink Repitions
                    D[6]= External Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= External Alarm, Voice Module, Repetitions

                When D[1]==00 and D[0]==05,
                    D[2]=
                    D[3]= Fire Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[4]= Fire Alarm, Entrance Indicator, Blink On Delay
                    D[5]= Fire Alarm, Entrance Indicator, Blink Off Delay
                    D[6]= Fire Alarm, Entrance Indicator, Repetitions
                    D[7]= Fire Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==01 and D[0]==05,
                    D[2]= Fire Alarm, RGD LED, Blink On Delay
                    D[3]= Fire Alarm, RGD LED, Blink Off Delay
                    D[4]= Fire Alarm, RGD LED, Blink Repetitions
                    D[5]= Fire Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]= Fire Alarm, Relay, Blink On Delay
                    D[7]= Fire Alarm, Relay, Blink Off Delay

                When D[1]==02 and D[0]==05,
                    D[2]= Fire Alarm, Relay, Blink Repitions
                    D[3]= Fire Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Fire Alarm, Voice Module, Repetitions
                    D[5]=
                    D[6]= Intrusion Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= Intrusion Alarm, Entrance Indicator, Blink On Delay

                When D[1]==03 and D[0]==05,
                    D[2]= Intrusion Alarm, Entrance Indicator, Blink Off Delay
                    D[3]= Intrusion Alarm, Entrance Indicator, Repetitions
                    D[4]= Intrusion Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= Intrusion Alarm, RGD LED, Blink On Delay
                    D[6]= Intrusion Alarm, RGD LED, Blink Off Delay
                    D[7]= Intrusion Alarm, RGD LED, Blink Repetitions

                When D[1]==04 and D[0]==05,
                    D[2]= Intrusion Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= Intrusion Alarm, Relay, Blink On Delay
                    D[4]= Intrusion Alarm, Relay, Blink Off Delay
                    D[5]= Intrusion Alarm, Relay, Blink Repitions
                    D[6]= Intrusion Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= Intrusion Alarm, Voice Module, Repetitions

                When D[1]==00 and D[0]==06,
                    D[2]=
                    D[3]= Reverse Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[4]= Reverse Alarm, Entrance Indicator, Blink On Delay
                    D[5]= Reverse Alarm, Entrance Indicator, Blink Off Delay
                    D[6]= Reverse Alarm, Entrance Indicator, Repetitions
                    D[7]= Reverse Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==01 and D[0]==06,
                    D[2]= Reverse Alarm, RGD LED, Blink On Delay
                    D[3]= Reverse Alarm, RGD LED, Blink Off Delay
                    D[4]= Reverse Alarm, RGD LED, Blink Repetitions
                    D[5]= Reverse Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]= Reverse Alarm, Relay, Blink On Delay
                    D[7]= Reverse Alarm, Relay, Blink Off Delay

                When D[1]==02 and D[0]==06,
                    D[2]= Reverse Alarm, Relay, Blink Repitions
                    D[3]= Reverse Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Reverse Alarm, Voice Module, Repetitions
                    D[5]=
                    D[6]= Tailing Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= Tailing Alarm, Entrance Indicator, Blink On Delay

                When D[1]==03 and D[0]==06,
                    D[2]= Tailing Alarm, Entrance Indicator, Blink Off Delay
                    D[3]= Tailing Alarm, Entrance Indicator, Repetitions
                    D[4]= Tailing Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= Tailing Alarm, RGD LED, Blink On Delay
                    D[6]= Tailing Alarm, RGD LED, Blink Off Delay
                    D[7]= Tailing Alarm, RGD LED, Blink Repetitions

                When D[1]==04 and D[0]==06,
                    D[2]= Tailing Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= Tailing Alarm, Relay, Blink On Delay
                    D[4]= Tailing Alarm, Relay, Blink Off Delay
                    D[5]= Tailing Alarm, Relay, Blink Repitions
                    D[6]= Tailing Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= Tailing Alarm, Voice Module, Repetitions

                When D[1]==00 and D[0]==07,
                    D[2]=
                    D[3]= Stayed Alarm, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[4]= Stayed Alarm, Entrance Indicator, Blink On Delay
                    D[5]= Stayed Alarm, Entrance Indicator, Blink Off Delay
                    D[6]= Stayed Alarm, Entrance Indicator, Repetitions
                    D[7]= Stayed Alarm, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]

                When D[1]==01 and D[0]==07,
                    D[2]= Stayed Alarm, RGD LED, Blink On Delay
                    D[3]= Stayed Alarm, RGD LED, Blink Off Delay
                    D[4]= Stayed Alarm, RGD LED, Blink Repetitions
                    D[5]= Stayed Alarm, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[6]= Stayed Alarm, Relay, Blink On Delay
                    D[7]= Stayed Alarm, Relay, Blink Off Delay

                When D[1]==02 and D[0]==07,
                    D[2]= Stayed Alarm, Relay, Blink Repitions
                    D[3]= Stayed Alarm, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[4]= Stayed Alarm, Voice Module, Repetitions
                    D[5]=
                    D[6]= Reverse, Entrance Indicator [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[7]= Reverse, Entrance Indicator, Blink On Delay

                When D[1]==03 and D[0]==07,
                    D[2]= Reverse, Entrance Indicator, Blink Off Delay
                    D[3]= Reverse, Entrance Indicator, Repetitions
                    D[4]= Reverse, RGB LED [(None, F0), (Black(All Off), 00), (Red, 01), (Green, 02), (Yellow(R+G), 03), (Blue, 04), (Magenta(R+B), 05), (Cyan, 06), (White(R+G+B), 07)]
                    D[5]= Reverse, RGD LED, Blink On Delay
                    D[6]= Reverse, RGD LED, Blink Off Delay
                    D[7]= Reverse, RGD LED, Blink Repetitions

                When D[1]==04 and D[0]==07,
                    D[2]= Reverse, Relay [(None, F0),(All Opened, 00), (Relay 1 Closed, 01)]
                    D[3]= Reverse, Relay, Blink On Delay
                    D[4]= Reverse, Relay, Blink Off Delay
                    D[5]= Reverse, Relay, Blink Repitions
                    D[6]= Reverse, Voice Module [(N9200, 01),(None, F0), (BY-F610 V1.2, 02),(BY-F610V1.3, 03))]
                    D[7]= Reverse, Voice Module, Repetitions








            '''

            pass

        if res[6:8]=="11" and res[8:10]=="0D":
            #decryption for communication parameters
            pass

        if res[6:8]=="11" and res[8:10]=="0E":
            #decryption for communication parameters
            pass

