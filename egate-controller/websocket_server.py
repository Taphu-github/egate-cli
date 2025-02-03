import asyncio
import websockets
import json

# Define the shutdown event
shutdown_event = asyncio.Event()
connected_clients = set()  # Track connected clients

async def websocket_handler(websocket, path):
    print("Client connected")
    connected_clients.add(websocket)  # Add to the client list
    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Construct a JSON response
            response_data = {
                "type": "echo",
                "received_message": message,
                "status": "success",
                "details": {
                    "description": "This is an echo of your message.",
                    "additional_info": "You can customize this response."
                }
            }
            json_response = json.dumps(response_data)

            # Send the JSON response
            await websocket.send(json_response)
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)  # Remove from the client list
# async def broadcast_message(message):
#     if connected_clients:  # Check if there are connected clients
#         # Create tasks for each client to send the message
#         tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
        
#         # Wait for all tasks to finish
#         await asyncio.gather(*tasks)

async def broadcast_message(event_type, document_type, status, details=None):
    """
    Broadcasts a JSON message to all connected WebSocket clients.

    Args:
        event_type (str): The type of event (e.g., 'passport_scanned', 'invalid_document').
        document_type (str): The type of document ('passport' or 'id_card').
        status (str): The status of the document ('scanned', 'invalid', 'verified').
        details (dict): Additional details (e.g., person's information, nationality).
    """
    if not connected_clients:
        print("No connected clients to broadcast to.")
        return

    # Construct the JSON message
    message = {
        "event_type": event_type,
        "document_type": document_type,
        "status": status,
        "details": details or {}
    }
    json_message = json.dumps(message)

    # Create tasks for each client to send the message
    tasks = [asyncio.create_task(client.send(json_message)) for client in connected_clients]

    # Wait for all tasks to finish
    await asyncio.gather(*tasks)

# WebSocket server entry point
async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 65431)
    print("WebSocket server started on ws://0.0.0.0:65431")

    # Periodically broadcast messages
    async def periodic_broadcast():
        while not shutdown_event.is_set():
            await broadcast_message(event_type="ECHO", documenttype="NONE", status="prob" )
            await asyncio.sleep(5)  # Broadcast every 5 seconds

    # Start the broadcast task
    broadcaster = asyncio.create_task(periodic_broadcast())

    await shutdown_event.wait()
    broadcaster.cancel()  # Cancel the broadcast task on shutdown
    server.close()
    await server.wait_closed()
    print("WebSocket server shut down.")

# Run the WebSocket server in its own asyncio loop
def start_websocket_server_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_websocket_server())
    finally:
        loop.close()
