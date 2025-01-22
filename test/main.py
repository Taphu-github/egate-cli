import threading
import queue
import websockets
import json
import asyncio
from utils import chunk_bytearray
import serial
import time
from aioserial import AioSerial


shared_message=queue.Queue()

def listening_stream(ser):
    temp_buffer=bytearray()
    while True:
        response = bytearray()
        if ser.in_waiting > 0:
            response.extend(ser.read(ser.in_waiting))
        if response:

            if len(response)==16:
                response_chunks = chunk_bytearray(response)
                shared_message.put(response_chunks[0])
            else:
                temp_buffer.extend(response)

            if len(temp_buffer)==16:
                response_chunks = chunk_bytearray(temp_buffer)
                shared_message.put(response_chunks[0])
                temp_buffer.clear()




def write_command(ser, command_name):
    pass


def handle_gate_response(response):
    cid1cid2=response[6:10]
    data_0=response[14:16]
    data_1=response[16:18]
    entered_count=int(response[18:24], 16)

    if cid1cid2 is not "1200":
        return None
    else:
        if data_0=="06" or data_0=="0C":
            return "before entering", entered_count
        if data_0=="08" or data_0=="00":
            return "after entering", entered_count








async def handle_client(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            try:
                # Parse the JSON message
                request = json.loads(message)
                status = request.get("status")
                data = request.get("data", {})
                print(data)
                if status=="Allowed":
                    await write_command(ser="serialization", command_name="open for entry")
                    response=shared_message.get()
                    gate_state, enteredcount=handle_gate_response(response=response)





                # command=get_command(command_name=data)
                # Check if the command exists
                # if command in COMMANDS:
                #     # Run the corresponding method
                #     result = COMMANDS[command](data)
                #     response = {"status": "success", "result": result}
                # else:
                #     response = {"status": "error", "message": f"Unknown command: {command}"}
                response = {"status": "success", "result": "recieved"}

            except Exception as e:
                response = {"status": "error", "message": str(e)}

            # Send the response back to the client
            await websocket.send(json.dumps(response))

    except websockets.ConnectionClosed:
        print("Client disconnected.")

# Start the WebSocket server
async def main():
    try:
        SERIAL_PORT = '/dev/ttyUSB0'
        BAUD_RATE = 38400
        TIMEOUT = 6

        ser = AioSerial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    except Exception as e:
        print("Couldn't connect to the serial port")
        exit(0)



    listening_stream_thread=threading.Thread(target=listening_stream, args=(ser,))
    listening_stream_thread.start()
    listening_stream_thread.join()

    async with websockets.serve(handle_client, "localhost", 8000):
        print("WebSocket server started on ws://localhost:8000")
        await asyncio.Future()  # Run forever


asyncio.run(main())
