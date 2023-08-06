import asyncio
import websockets
import json
import os
# from distutils.log import warn
import warnings
# import sys


def get_cmd_disconn():
    return {"index": 3}


id = 0


def get_cmd_setId():
    id += 1
    return {"index": 2, "package": id}


def get_cmd_norm():
    return {"index": -1, "package": -1}


def get_data():
    return {"id": 0, "servercmd": None, "data": {}}


def get_disConnData():
    data = get_data()
    data["servercmd"] = get_cmd_disconn()
    return data


class WebSockets:
    def __init__(self):
        self.unityClient = None
        self.jupyterClient = None
        self.disconnData = json.dumps(get_disConnData())

    async def commonRegister(self, clientName):
        try:
            if clientName == "unity":
                await self.unityClient.send(self.disconnData)
            if clientName == "jupyter":
                await self.jupyterClient.send(self.disconnData)
        except Exception as e:
            warnings.warn(e)
            warnings.warn("the previous client should've been disconnected")

    async def registerUnityClient(self, ws):
        if (self.unityClient is not ws) and (self.unityClient is not None):
            await self.commonRegister("unity")
        self.unityClient = ws

    async def registerJupyterClient(self, ws):
        if (self.jupyterClient is not ws) and (self.jupyterClient is not None):
            await self.commonRegister("jupyter")
        self.jupyterClient = ws

    async def handleNew(self, msg, ws):
        if (msg["id"] == "jupyter"):
            await self.registerJupyterClient(ws)

        if (msg["id"] == "unity"):
            await self.registerUnityClient(ws)

        if (msg["id"] == "local_ping"):
            await ws.send(json.dumps({"ok":1}))


    async def relay(self, msg):
        if ("id" not in msg):
            pass
            #print(msg)
        if (msg["id"] == "jupyter"):
            if(self.unityClient is not None):
                await self.handleSend(self.unityClient, json.dumps(msg))
            if ("debug" in msg) and (msg["debug"] == 1):
                await self.handleSend(self.jupyterClient, json.dumps(msg))
        if (msg["id"] == "unity"):
            if(self.jupyterClient is not None):
                await self.handleSend(self.jupyterClient, json.dumps(msg))
            if ("debug" in msg) and (msg["debug"] == 1):
                await self.handleSend(self.unityClient, json.dumps(msg))
            if 'recorded_data' in msg:
                if msg['recorded_data']['path'] == '':
                    return
                try:
                    dirpath = msg['recorded_data']['path']
                    filepath = dirpath + msg['recorded_data']['fname']
                    if not (os.path.exists(dirpath)):
                        os.makedirs(dirpath)
                    data2save = msg['recorded_data']['data']
                    text_file = open(filepath, "w")
                    text_file.write(data2save)
                    text_file.close()
                except Exception as e:
                    warnings.warn(e)

    async def handleSend(self, ws, msg):
        try:
            await ws.send(msg)
        except Exception as e:
            pass
            # warnings.warn(e)


wsManager = WebSockets()


async def echo(websocket):
    # print("back repeater server running")
    # print(websocket)
    try:
        async for message in websocket:
            try:
                # print(f"---:message---")
                # print(message)
                msg = json.loads(message)
                # print(msg)
                await wsManager.handleNew(msg, websocket)
                await wsManager.relay(msg)
            except Exception as ee:
                warnings.warn(msg)
                warnings.warn(ee)
    except Exception as e:
        # warnings.warn(msg)
        warnings.warn(e)


def bridge_main():
    print('simulator server running @ 12740')
    start_server = websockets.serve(echo, "0.0.0.0", 12740)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def ping():
    from websocket import create_connection

    try:
        ws = create_connection("ws://0.0.0.0:12740")
        ws.send(json.dumps({"id":"local_ping"}))
        result =  ws.recv()
        # print(result)
        ws.close()
        return True
    except:
        # print("error")
        return False


if __name__ == "__main__":
    if(not ping()):
        bridge_main()
    
        
        
    
    
