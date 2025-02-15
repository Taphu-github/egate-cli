import json
import os
import time

def parse_depending_on_type(data_json, datas, cid1, cid2):
    # print(data_json)
    j=0
    data2_7=data_json.get('DATA')
    # print(data2_7)
    family={}
    for k in data2_7.keys():
        if j==8:
            j=0

        # print()
        if data2_7[k].get("FAMILY") and data2_7[k].get("FAMILY") != "" and data2_7[k].get("TYPE")=="NUMBER":
            family_label=data2_7[k].get("FAMILY")
            # print(family_label)
            if family.get(family_label):

                family[family_label]+=datas[j]
            else:
                # print(data2_7.get("LABEL"))
                family[family_label]=datas[j]

        elif data2_7[k].get("TYPE")=="NUMBER":
            print(f'{data2_7[k].get("LABEL")} : {int(datas[j], 16)}' )
        elif data2_7[k].get("TYPE")=="SELECT":
            for opt in  data2_7[k].get("OPTIONS"):
                # print()
                if opt.get("VALUE") and opt["VALUE"]==datas[j]:
                    print(f'{data2_7[k].get("LABEL")} : {opt["LABEL"]}')

        elif data2_7[k].get("TYPE")=="CALCULATIVE":
            value=int(datas[j], 16)
            # print(value)

            arranged_options_hex=data2_7[k].get("OPTIONS")[::-1]
            # print(arranged_options_hex)

            selected_options={}
            for opp in arranged_options_hex:
                if value>=int(opp.get("VALUE"), 16):
                    selected_options[opp.get("LABEL")]="ON"
                    value-=int(opp.get("VALUE"),16)
                else:
                    selected_options[opp.get("LABEL")]="OFF"
            print(data2_7[k].get("LABEL"),selected_options)


        # print(j)
        else:
            # print(data2_7[k])
            print(f"------cid1: {cid1} cid2:{cid2}, data[0]: {datas[0]} data[1]: {datas[1]} position: {j} value: {datas[j]}-----")
        j+=1

    for key in family.keys():
        family_value_hex=family.get(key) or "00"
        family_value_int=int(family_value_hex, 16)
        print(f"HELO: {family_value_int}")
        print(f"{key}: {family_value_int}")



def parse(cmd):
    cmd_arr=[ cmd[i:i+2] for i in range(0,(len(cmd)),2)]
    cid1=cmd_arr[3]#CID_1
    cid2=cmd_arr[4]#CID_2
    # print("commands",cmd_arr)
    d_0=cmd_arr[7]
    d_1=cmd_arr[8]


    # print(cmd_arr)
    # print(f"CID1: {cid1}, CID2: {cid2}, D0: {d_0}, D1: {d_1}")
    cwd=os.getcwd()
    full_file_path=os.path.join(cwd, "response_parser_jsons","response_conversion.json")

    with open(full_file_path, "r") as file:
        data = json.load(file)
    for key in data.keys():
        for dat in data[key]:
            for cid in dat.get("CID"):
                if cid==(cid1+" "+cid2):
                    if len(dat.get("DATAS"))==1:
                        parse_depending_on_type(data_json=dat["DATAS"][0], datas=cmd_arr[7:], cid1=cid1, cid2=cid2)
                    else:
                    # print(dat)
                        for da in dat["DATAS"]:
                            d__0=da.get("DATA_0", "error_0")
                            d__1=da.get("DATA_1", "error_1")
                            # print(f"DATA_0: {d__0}, DATA_1: {d__1}")
                            if da.get("DATA_0") and da.get("DATA_1"):
                                if da["DATA_0"] ==d_0 and da["DATA_1"]==d_1:
                                    parse_depending_on_type(data_json=da, datas=cmd_arr[7:], cid1=cid1, cid2=cid2)


def get_parse_depending_on_type(data_json, datas, cid1, cid2):
     # print(data_json)
    j=0
    data2_7=data_json.get('DATA')
    # print(data2_7)
    family={}
    for k in data2_7.keys():
        if j==8:
            j=0

        # print()
        if data2_7[k].get("FAMILY") and data2_7[k].get("FAMILY") != "" and data2_7[k].get("TYPE")=="NUMBER":
            family_label=data2_7[k].get("FAMILY")
            # print(family_label)
            if family.get(family_label):

                family[family_label]+=datas[j]
            else:
                # print(data2_7.get("LABEL"))
                family[family_label]=datas[j]

        elif data2_7[k].get("TYPE")=="NUMBER":
            print(f'{data2_7[k].get("LABEL")} : {int(datas[j], 16)}' )
        elif data2_7[k].get("TYPE")=="SELECT":
            for opt in  data2_7[k].get("OPTIONS"):
                # print()
                if opt.get("VALUE") and opt["VALUE"]==datas[j]:
                    print(f'{data2_7[k].get("LABEL")} : {opt["LABEL"]}')

        elif data2_7[k].get("TYPE")=="CALCULATIVE":
            value=int(datas[j], 16)
            # print(value)

            arranged_options_hex=data2_7[k].get("OPTIONS")[::-1]
            # print(arranged_options_hex)

            selected_options={}
            for opp in arranged_options_hex:
                if value>=int(opp.get("VALUE"), 16):
                    selected_options[opp.get("LABEL")]="ON"
                    value-=int(opp.get("VALUE"),16)
                else:
                    selected_options[opp.get("LABEL")]="OFF"
            
            print(data2_7[k].get("LABEL"),selected_options)


        # print(j)
        else:
            # print(data2_7[k])
            print(f"------cid1: {cid1} cid2:{cid2}, data[0]: {datas[0]} data[1]: {datas[1]} position: {j} value: {datas[j]}-----")
        j+=1

    
    for key in family.keys():
        family_value_hex=family.get(key) or "00"
        family_value_int=int(family_value_hex, 16)
        print(f"HELO: {family_value_int}")
        print(f"{key}: {family_value_int}")






def get_parsed_response(cmd):
    cmd_arr = [cmd[i:i + 2] for i in range(0, len(cmd), 2)]
    cid1 = cmd_arr[3]  # CID_1
    cid2 = cmd_arr[4]  # CID_2
    d_0 = cmd_arr[7]
    d_1 = cmd_arr[8]


    data_0_dict = {
        "00": "GATE_WAS_CLOSED_FREE",
        "01": "GATE_WAS_CLOSED_FIRE_ALARM",
        "02": "GATE_WAS_CLOSED_POWER_OFF",
        "03": "GATE_WAS_OPENED_FREE",
        "04": "GATE_WAS_OPENED_FIRE_ALARM",
        "05": "GATE_WAS_OPENED_MANUAL",
        "06": "GATE_WAS_OPENED_ENTRY",
        "07": "GATE_WAS_OPENED_EXIT",
        "08": "ENTRY_GATE_WAS_CLOSING",
        "09": "EXIT_GATE_WAS_CLOSING",
        "0A": "ENTRY_GATE_WAS_CLOSING_ANTI_PINCH",
        "0B": "Exit gate was closing(Anti-pinch)",
        "0C": "ENTRY_GATE_WAS_OPENING",
        "0D": "Exit gate was opening",
        "0E": "ENTRY_MANUAL_OPEN_GATE",
        "0F": "EXIT_MANUAL_OPEN_GATE",
        "5F": "Stranded Alarm",
        "60": "INTRUSION_ALARM",
        "61": "Reverse Alarm",
        "62": "Tail Alarm",
        "63": "External Alarm",
        "FF": "Power On Self Test"
    }

    data_1_dict = {
        "01": "Entry Open",
        "02": "Entry Close",
        "03": "Exit Open",
        "04": "Exit Close",
        "05": "Equipment Failure",
        "06": "External Alarm",
        "07": "Firm Alarm",
        "08": "Intrusion Alarm",
        "09": "Reverse Alarm",
        "0A": "Tail Alarm",
        "0B": "Stranded Alarm",
        "0C": "Reverse"
    }

    response = {}

    if cid1 == "12" and cid2 == "00":
        response["gate_status"] = data_0_dict.get(d_0, "Unknown Status")
        response["last_action"] = data_1_dict.get(d_1, "Unknown Action")
        response["entry_count"] = int("".join(cmd_arr[9:12]), 16)
        response["exit_count"] = int("".join(cmd_arr[12:15]), 16)
        response["gate_action_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Store current timestamp

    return response


    cwd = os.getcwd()
    full_file_path = os.path.join(cwd, "response_parser_jsons", "response_conversion.json")

    with open(full_file_path, "r") as file:
        data = json.load(file)

    parsed_data = {}

    for key in data.keys():
        for dat in data[key]:
            for cid in dat.get("CID"):
                if cid == (cid1 + " " + cid2):
                    if len(dat.get("DATAS")) == 1:
                        parsed_data = get_parse_depending_on_type(dat["DATAS"][0], cmd_arr[7:], cid1, cid2)
                    else:
                        for da in dat["DATAS"]:
                            if da.get("DATA_0") and da.get("DATA_1"):
                                if da["DATA_0"] == d_0 and da["DATA_1"] == d_1:
                                    parsed_data = get_parse_depending_on_type(da, cmd_arr[7:], cid1, cid2)

    return parsed_data



# data = [
#   "AA 00 02 11 11 01 08 00 00 64 64 64 64 64 64 85",
#   "AA 00 02 11 11 01 08 00 01 64 64 19 00 40 00 4F",
#   "AA 00 02 11 11 01 08 00 02 00 64 02 64 64 05 62",
#   "AA 00 02 11 11 01 08 00 03 00 32 00 00 01 01 64",
#   "AA 00 02 11 11 01 08 00 04 01 02 02 02 00 00 38",
#   "AA 00 02 11 11 01 08 01 00 49 29 10 49 41 49 83",
#   "AA 00 02 11 11 01 08 01 01 41 48 48 29 49 49 BB",
#   "AA 00 02 11 11 01 08 01 02 49 00 02 05 16 13 A9",
#   "AA 00 02 11 11 01 08 01 03 00 00 00 00 00 00 31",
#   "AA 00 02 11 11 01 08 01 04 00 00 00 00 00 00 32",
#   "AA 00 02 11 11 01 08 02 00 00 F0 00 00 00 00 1F",
#   "AA 00 02 11 11 01 08 02 01 00 00 00 F0 00 00 20",
#   "AA 00 02 11 11 01 08 02 02 00 01 01 00 01 00 34",
#   "AA 00 02 11 11 01 08 02 03 00 00 04 00 00 00 36",
#   "AA 00 02 11 11 01 08 02 04 F0 00 00 00 F0 01 14",
#   "AA 00 02 11 11 01 08 03 00 00 08 00 00 00 02 3A",
#   "AA 00 02 11 11 01 08 03 01 03 03 00 F0 00 00 27",
#   "AA 00 02 11 11 01 08 03 02 00 01 01 00 F0 00 24",
#   "AA 00 02 11 11 01 08 03 03 00 00 04 00 00 00 37",
#   "AA 00 02 11 11 01 08 03 04 F0 00 00 00 F0 01 15",
#   "AA 00 02 11 11 01 08 04 00 00 00 00 00 00 01 32",
#   "AA 00 02 11 11 01 08 04 01 02 02 14 F0 00 00 3A",
#   "AA 00 02 11 11 01 08 04 02 00 F0 01 00 00 00 24",
#   "AA 00 02 11 11 01 08 04 03 00 00 01 04 02 00 3B",
#   "AA 00 02 11 11 01 08 04 04 F0 00 00 00 F0 01 16",
#   "AA 00 02 11 11 01 08 05 00 00 09 00 00 00 02 3D",
#   "AA 00 02 11 11 01 08 05 01 03 03 00 F0 00 00 29",
#   "AA 00 02 11 11 01 08 05 02 00 F0 01 00 00 00 25",
#   "AA 00 02 11 11 01 08 05 03 00 00 01 04 02 00 3C",
#   "AA 00 02 11 11 01 08 05 04 F0 00 00 00 F0 01 17",
#   "AA 00 02 11 11 01 08 06 00 00 00 00 00 00 01 34",
#   "AA 00 02 11 11 01 08 06 01 04 02 00 F0 00 00 2A",
#   "AA 00 02 11 11 01 08 06 02 00 F0 01 00 F0 00 16",
#   "AA 00 02 11 11 01 08 06 03 00 00 01 04 02 00 3D",
#   "AA 00 02 11 11 01 08 06 04 F0 00 00 00 F0 01 18",
#   "AA 00 02 11 11 01 08 07 00 00 F0 00 00 00 01 25",
#   "AA 00 02 11 11 01 08 07 01 04 02 00 F0 00 00 2B",
#   "AA 00 02 11 11 01 08 07 02 00 F0 01 00 F0 00 17",
#   "AA 00 02 11 11 01 08 07 03 00 00 F0 00 00 00 27",
#   "AA 00 02 11 11 01 08 07 04 F0 00 00 00 F0 01 19"
# ]

# for dat in data:
#     parse("".join(dat.split(" ")))

# parse("".join("AA 00 02 12 02 00 08 00 00 00 00 00 EF 00 87 94 ".split(" ")))
