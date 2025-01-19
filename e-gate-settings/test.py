import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    serial_ports=[]

    for port in ports:
        serial_ports.append(port.device)
    return serial_ports

available_ports = list_serial_ports()

print("Available ports: ", available_ports)