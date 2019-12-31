import asyncio
import websockets
from configuration import config

async def client():
    uri = "ws://"+config['host']+":"+str(config['port'])
    async with websockets.connect(uri) as websocket:
        await websocket.send(str(278212))
        while True:
            try:
                data = await websocket.recv()
                print(f"{data}")
            except:
                print("server closed")
                break

asyncio.get_event_loop().run_until_complete(client())
asyncio.get_event_loop().run_forever()