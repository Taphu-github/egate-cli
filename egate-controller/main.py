import threading
import asyncio
import signal
import sys
from gui import GateControllerApp, start_websocket_loop, shutdown_event

from tcp_server import start_tcp_server  # Import the TCP server

# from websocket_server import start_websocket_server_loop

def main():
    app = GateControllerApp()

    def signal_handler(sig, frame):
        print('Shutting down...')
        shutdown_event.set()
        app.quit()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

     # Start WebSocket client loop in a separate thread
    # websocket_thread = threading.Thread(target=start_websocket_loop, daemon=True)
    # websocket_thread.start()

    #  # Start WebSocket server loop in a separate thread
    # websocket_server_thread = threading.Thread(target=start_websocket_server_loop, daemon=True)
    # websocket_server_thread.start()

    # Start the TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server, args=(shutdown_event, ), daemon=True)
    tcp_thread.start()

    app.menu()

    if 'ser' in globals():
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
