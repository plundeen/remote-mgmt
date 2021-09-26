import websockets
import asyncio
import json

PORT = 7890

print(f"Server listening on port {PORT}")

# Create a dictionary/hash table of connected clients
clients = {}


def handle_client_id(msg: str, websocket):
    # Example contents:
    # {"type": "client_id", "id": <client id>}
    clients[websocket] = msg["id"]
    print(clients)


async def handle_client_heartbeat(msg: str, websocket):
    await websocket.send("pong")


# Create map of msg_handlers, so we can easily dispatch the appropriate one
msg_handlers = {"client_id": handle_client_id, "heartbeat": handle_client_heartbeat}


async def echo(websocket, path):
    print(f"New client connected: {websocket}")
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            msg_obj = json.loads(message)
            msg_type = msg_obj["type"]
            handler = msg_handlers[msg_type]
            handler(msg_obj, websocket)
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
