import json

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


    with open("response_conversion.json", "r") as file:
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
