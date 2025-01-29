import threading
import queue
import websockets
import json
import asyncio
from utils import chunk_bytearray,get_device_id,get_max_passage_time
import serial
import time
from aioserial import AioSerial
import signal

shared_message = queue.Queue()

try:
    SERIAL_PORT = 'COM3'
    BAUD_RATE = 38400
    TIMEOUT = 6

    ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print("Couldn't connect to the serial port")
    exit(0)

PASSAGE_TIME=get_max_passage_time(ser)
ADDR_TO=get_device_id(ser)

print("PASSAGE TIME", PASSAGE_TIME)

def listening_stream(ser):
    temp_buffer = bytearray()
    while True:
        try:
            response = bytearray()
            if ser.in_waiting > 0:
                response.extend(ser.read(ser.in_waiting))
            if response:
                if len(response) == 16:
                    response_chunks = chunk_bytearray(response)
                    shared_message.put(response_chunks[0])
                else:
                    temp_buffer.extend(response)

                if len(temp_buffer) == 16:
                    response_chunks = chunk_bytearray(temp_buffer)
                    shared_message.put(response_chunks[0])
                    temp_buffer.clear()
        except Exception as e:
            print(f"Error in listening stream: {e}")
            break

async def write_command(ser, command_arr):
    print(f"Command: {command_arr}")
    for com in command_arr:
        command_bytes = bytes.fromhex(com)
        ser.write(command_bytes)

def handle_gate_response(response):
    cid1cid2 = response[6:10]
    data_0 = response[14:16]
    entered_count = int(response[18:24], 16)

    if cid1cid2 != "1200":
        return None
    else:
        if data_0 in ["06", "0C", "08", "00"]:
            return entered_count

async def handle_client(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            try:
                request = json.loads(message)
                status = request.get("status")
                if status == "Allowed":
                    command_arr = ["AA00010200020800000000000000000D"]
                    await write_command(ser=ser, command_arr=command_arr)
                    start_time = time.time()

                    gate_state_set = set()
                    while time.time() - start_time < (PASSAGE_TIME/10):
                        if not shared_message.empty():
                            response = shared_message.get()
                            entered_count = handle_gate_response(response=response)

                            if entered_count and entered_count not in gate_state_set:
                                gate_state_set.add(entered_count)

                    print(gate_state_set)
                    if len(gate_state_set) == 1:
                        message = "No one passed through the gate!"
                    elif len(gate_state_set) == 2:
                        message = "Passed the gate successfully"
                    else:
                        message = "Abnormality"
                elif status=="Not Allowed":
                    make_alarm=["AA000102000208020100000000000010"]
                    await write_command(ser=ser, command_arr=make_alarm)
                    time.sleep(5)
                    stop_alarm=["AA00010200020802000000000000000F"]
                    await write_command(ser=ser, command_arr=stop_alarm)
                    message="alarm sounded"

                response = {"status": "success", "result": message}

            except Exception as e:
                response = {"status": "error", "message": str(e)}

            await websocket.send(json.dumps(response))
    except websockets.ConnectionClosed:
        print("Client disconnected.")

async def main():
    # Start the listening thread
    listening_stream_thread = threading.Thread(target=listening_stream, args=(ser,))
    listening_stream_thread.daemon = True
    listening_stream_thread.start()

    # Create an event to manage graceful shutdown
    stop_event = asyncio.Event()

    def shutdown():
        print("Shutting down server...")
        stop_event.set()

    # Register signal handlers for shutdown
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown())
    signal.signal(signal.SIGTERM, lambda sig, frame: shutdown())

    async with websockets.serve(handle_client, "localhost", 8004):
        print("WebSocket server started on ws://localhost:8004")
        await stop_event.wait()

# Run the main function
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    ser.close()  # Ensure the serial port is closed
    print("Serial connection closed.")
