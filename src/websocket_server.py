import websockets
import asyncio

PORT = 7890

print(f"Server listening on port {PORT}")

clients = set()

async def echo(websocket, path):
    print(f"New client connected: {websocket}")
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            for client in clients:
                await client.send(f"Someone said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")
        print(e)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
