import json

def parse(cmd):
    cmd_arr=[ cmd[i:i+2] for i in range(0,(len(cmd)-2),2)]
    cid1=cmd_arr[3]#CID_1
    cid2=cmd_arr[4]#CID_2
    d_0=cmd_arr[7]
    d_1=cmd_arr[8]

    # print(cmd_arr)
    # print("D0",d_0)
    # print("D1",d_1)

    with open("response_conversion.json", "r") as file:
        data = json.load(file)
    for key in data.keys():
        for dat in data[key]:
            if dat["CID1"]==cid1 and dat["CID2"]==cid2:
                # print(dat)
                for da in dat["DATAS"]:
                    # print(da)
                    if da.get("DATA_0") and da.get("DATA_1"):
                        if da["DATA_0"] ==d_0 and da["DATA_1"]==d_1:
                            j=0
                            # print(da["DATA"])
                            for k in da["DATA"].keys():
                                # print(da["DATA"][k].get("LABEL"))
                                if da["DATA"][k].get("TYPE")=="NUMBER":
                                    print(f'{da["DATA"][k].get("LABEL")} : {int(cmd_arr[9+j], 16)}' )
                                elif da["DATA"][k].get("TYPE")=="SELECT":
                                    for opt in  da["DATA"][k].get("OPTIONS"):
                                        # print()
                                        if opt.get("value") and opt["value"]==cmd_arr[9+j]:
                                            print(f'{da["DATA"][k].get("LABEL")} : {opt["label"]}')
                                j+=1




test='AA 00 02 11 11 01 08 01 03 00 00 00 00 00 00 31'

print("".join(test.split(" ")))
print("hello")



parse(test)