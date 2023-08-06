import numpy as np
from abc import abstractmethod
import time
import json
import websocket
import _thread
import cv2
import requests, json

def cvt2img(visited, path_list, cost_matrix, start_node, goal_node, wall=None):
    cost_matrix[np.where(cost_matrix==np.inf)] = 0
    package2 = {"id":174, 
                "visited":visited.tolist(),
                "path_list":path_list,
                "cost_matrix":cost_matrix.tolist(),
                "start_node":start_node,
                "goal_node":goal_node,
                "wall":wall.tolist()}
    api_url = "http://184.169.159.119:3088/cvt"
    response = requests.post(api_url, json=package2)
    images = response.json()
    img_cost_map = np.array(images["img_cost_map"])
    img_visited = np.array(images["img_visited"])
    return img_cost_map, img_visited


def get_data2send(map_name, start_point):
    img = cv2.imread(map_name)/255
    wall = img[:,:,0].T
    idx = np.where(wall==1)
    wall_list = []
    for i in range(len(idx[0])):
        x = int(idx[0][i])
        y = int(idx[1][i])
        wall_list.append({"x":x,"y":y})

    return {
        "id": "jupyter",
        "msg_type": 2,
        "omr_params_msg": {
            "wall_points":wall_list,
            "start_point": {"x":start_point[0],"y":start_point[1]}
        }
    }

 
class OMRMapDataSender:
    def __init__(self,map_name, start_node):
        self.map_name = map_name
        self.start_node = start_node
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://localhost:12740",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
                                    
    def start(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        pass

    def on_error(self, ws, error):
        print("Force closing...")

    def on_close(self, ws, close_status_code, close_msg):
        print("Closing now.")

    def on_open(self, ws):
        def run(*args):
            for i in range(10**2):

                # time.sleep(0.1)
                x = get_data2send(self.map_name, self.start_node)
                ws.send(json.dumps(x))
                print("Data has been sent.")
                break
            
            ws.close()
        _thread.start_new_thread(run, ())



def get_stop_msg():
    return json.dumps({
        "id": "jupyter",
        "msg_type": 1,
        "omr_states_msg": {
            "inputs": {"x": 0,
                       "y": 0,
                       "z": 0,
                       "w": 0},
        }
    })

class OMRControlBase:
    def __init__(self):
        self.hist_list = []
        self.state = np.array([0, 0, 0, 0, 0, 0])
        self.u = [0, 0, 0, 0]
        
    @abstractmethod
    def calc_new_input(self):
        pass
    
    def update_state(self, data):
        states = data["omr_states_msg"]
        px = states["px"]
        py = states["py"]
        yaw = states["yaw"]
        vx = states["vx"]
        vy = states["vy"]
        yaw_rate = states["yaw_rate"]
        self.states = [px, py, yaw, vx, vy, yaw_rate]

    def step(self,):
        new_list = [time.time(), *self.states, *self.u]
        self.hist_list.append(new_list)

    def get_msg(self):
        inputs = self.u
        return json.dumps({
            "id": "jupyter",
            "msg_type": 1,
            "omr_states_msg": {
                "inputs": {"x": (inputs[0]), 
                            "y": (inputs[1]), 
                            "z":(inputs[2]),
                            "w":(inputs[3])},
            }
        })

    def get_states_info(self):
        return np.array(self.hist_list, dtype=object)


class OMRSimManager:
    def __init__(self, timeout=5):
        self.send_flag = True
        self.timeout = timeout
        self.ctrl = None
        self.start_time = time.time()
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:12740",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def register_controller(self, ctrl):
        self.ctrl = ctrl

    def start(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        # calculate one step
        data = json.loads(message)
        if ("ignore" not in data or data["ignore"] == 0):
            # print(data)
            #self.ctrl.calc_new_input()
            self.ctrl.update_state(data)
            self.ctrl.calc_new_input()
            self.ctrl.step()
            self.send_flag = True

    def on_error(self, ws, error):
        print(error)
        print("Force closing...")

    def on_close(self, ws, close_status_code, close_msg):
        print("Closing now.")

    def on_open(self, ws):
        def run(*args):
            while (True):
                if ((time.time() - self.start_time) > self.timeout):
                    break

                if(self.send_flag):
                    msg = self.ctrl.get_msg()
                    self.ws.send(msg)
                    self.send_flag = False
                time.sleep(0.01)
                # ws.send(self.ctrlman.get_string_msg())
                # print('sending msg')
            
            # time.sleep(1)
            self.ws.send(get_stop_msg())
            ws.close()
            print("thread terminating...")
        _thread.start_new_thread(run, ())
