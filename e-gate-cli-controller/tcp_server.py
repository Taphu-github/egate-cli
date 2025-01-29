# tcp_server.py
import socket
import threading
from commands_and_variables import run_command, shared_message

# Function to handle the serial connection and TCP commands
def handle_tcp_connection(client_socket, address):
    print(f"Accepted connection from {address}")

    try:
        while True:
            # Receive data from the TCP client
            data = client_socket.recv(1024)  # Buffer size of 1024 bytes
            if not data:
                print("No data received. Closing connection.")
                break

            command_text = data.decode('utf-8').strip()  # Decode and strip whitespace

            print(f"Received command: {command_text}")

            # Use the send_command_and_listen function from GateController.py
            run_command(command_text)
            response_message=shared_message.get()


            # Send response back to the client
            client_socket.sendall(response_message.encode('utf-8'))

    except Exception as e:
        print(f"Error handling connection from {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed.")


# Function to start the TCP server
def start_tcp_server(shutdown_event, host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"TCP server listening on {host}:{port}")

        while not shutdown_event.is_set():
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_tcp_connection, args=(conn, shutdown_event), daemon=True).start()
            except socket.error as e:
                print(f"Socket error: {e}")
                break