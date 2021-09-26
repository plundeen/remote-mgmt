import websockets
import asyncio
import json

PORT = 7890

print(f"Server listening on port {PORT}")

# Create a dictionary/hash table of connected clients
clients = {}

async def echo(websocket, path):
    print(f"New client connected: {websocket}")
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            msg_obj = json.loads(message)
            if msg_obj.get("id"):
                clients[websocket] = msg_obj["id"]
                print(clients)
            for client in clients:
                await client.send(f"Someone said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")
        print(e)
    finally:
        del clients[websocket]

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
