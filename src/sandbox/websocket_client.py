import websockets
import asyncio
import datetime
import json


PORT = 7890

async def ws_connect():
    url = f"ws://localhost:{PORT}"

    async with websockets.connect(url) as ws:
        client_id = { "id": f"{datetime.datetime.now().time()}"}
        await ws.send(json.dumps(client_id))
        while True:
            msg = await ws.recv()
            print(msg)


asyncio.get_event_loop().run_until_complete(ws_connect())
