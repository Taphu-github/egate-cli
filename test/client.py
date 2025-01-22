import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:8004"
    async with websockets.connect(uri) as websocket:
        # Send a command to the server
        data={
                "full_name":"Tandin Phuntsho",
                "cid":"10305002226",
                "nationality":"Bhutanese",
                "date_of_birth":"27/05/2001"
            }
        command = {"status": "Allowed", "data": data}
        await websocket.send(json.dumps(command))
        print(f"Sent: {command}")

        # Wait for a response
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(client())
