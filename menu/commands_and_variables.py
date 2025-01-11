import json
with open(r"C:\Users\Gaming\Desktop\Padestrian_Terminal\egate-cli\command_mapping.json", "r") as file:
    COMMANDS = json.load(file)

if not COMMANDS:
    print("Please Check If the 'commands.json' file exists")
    exit()


def get_command(command_name):
    for command in COMMANDS:
        if command.get("command") and command.get("command")==command_name:
            return command
    return {}

def generate_checksum(data):
    hex_pairs=data.split(" ")

    sums= 0
    for hexi in hex_pairs[1:]:
        sums+=int(hexi, 16)

    hex_val=hex(sums)
    meaningful_val_of_hex=hex_val.split("x")[1]

    if len(meaningful_val_of_hex)==1:
        return ("0"+meaningful_val_of_hex).upper()

    elif len(meaningful_val_of_hex)==2:
        return meaningful_val_of_hex.upper()

    else:
        return meaningful_val_of_hex[-2:].upper()

def create_command(command_structure,addr_to):
    commands=[]
    cid1=command_structure.get("cid1")
    cid2=command_structure.get("cid2")
    data_length=command_structure.get("data_length")
    multiple=command_structure.get("multiple")
    data=command_structure.get("data")
    structure=command_structure.get("structure")
    addr_src="00"


    if not cid1 or not cid2 or not data_length:
        print("The Structure of the command is wrong as cid1 or cid2 or datalenght doesn't exist")

    if multiple and len(multiple)!=0:
        #build for multiple structure
        mutiple_command=[ "AA 00"+addr_src+" "+cid1+" "+cid2+" "+addr_to+" "+data_length+" "+cmd for cmd in multiple]
        commands.extend(mutiple_command)

    elif data:
        #build if data is already present
        data_command="AA 00"+" "+addr_src+" "+cid1+" "+cid2+" "+addr_to+" "+data_length+" "+data
        commands.append(data_command)

    elif structure:
        #build the command for structure
        pass

    return [cm + " " + generate_checksum(cm) for cm in commands]

def get_and_create_command(command_name,addr_to):
    command_structure=get_command(command_name)
    if not command_structure:
        print("There is no command structure which matches '{}'".format(command_name))

    commands=create_command(command_structure=command_structure, addr_to=addr_to)
    if not commands:
        print("Something went wrong in the generation of your command")

    return commands
