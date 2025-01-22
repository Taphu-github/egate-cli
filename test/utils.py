
def get_command(command_name):
    pass

def chunk_bytearray(byte_array, chunk_size=16):
    # print(byte_array)
    chunks = [
        byte_array[i : i + chunk_size] for i in range(0, len(byte_array), chunk_size)
    ]
    # Convert each chunk to a hex string
    hex_chunks = ["".join(f"{byte:02X}" for byte in chunk) for chunk in chunks]

    return hex_chunks