import websocket, _thread, time, json

class EstimationUploader():
    def __init__(self):
        websocket.enableTrace(False)
        self.data = {"id":"jupyter", "debug":1, 
                        "est_data":{
                            "eul_gt":[{"x":0, "y":0, "z":0}, {"x":0, "y":0, "z":0}],
                            "eul_est":[{"x":0, "y":0, "z":0},{"x":1, "y":2, "z":1}],
                            }
                        }
        
        
    def convert(self, data):
        result = []
        for i in range(0, data.shape[0]):
            temp = {"x":data[i,0], "y":data[i,1], "z":data[i,2]}
            result.append(temp)
        return result
            
    def upload(self, eul_gt, eul_est):
        def on_message(ws, message):
            print(message)
        def on_error(ws, error):
            print(error)
        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            def run(*args):
                for i in range(3):
                    self.data["est_data"]["eul_gt"] = self.convert(eul_gt)
                    self.data["est_data"]["eul_est"] = self.convert(eul_est)
                    ws.send(json.dumps(self.data))
                time.sleep(0.02)
                ws.close()
                print("thread terminating...")
            _thread.start_new_thread(run, ())
        self.ws = websocket.WebSocketApp("ws://0.0.0.0:3000",
                                          on_open=on_open,
                                          on_message=on_message,
                                          on_error=on_error,
                                          on_close=on_close)

        self.ws.run_forever()
