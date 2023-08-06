import datetime
import websocket
import time
import _thread
import json
import numpy as np
import os
from .TestCases import ch3_test, ch4_test, ch5_test
from .Functions.DataReaderUtils import unpack_json
from .Functions.SimComm import request_data, send_replay_data

# def request_data():
#     comm_req = RequestIMUData()
#     comm_req.start()


# def send_replay_data(eul_gt, eul_est):
#     N = eul_gt.shape[0]
#     N2 = eul_est.shape[0]
#     if ( N != N2):
#         print("The ground truth and the estiamted data sets need to be the same size")
#         return 
    
#     ts_list, eul_gt_list, eul_est_list = [], [], []
#     for i in range(0, N):
#         ts_list.append(i)
#         eul_gt_list.append({"x": eul_gt[i,0], "y": eul_gt[i,1], "z": eul_gt[i,2] })
#         eul_est_list.append({"x": eul_est[i,0], "y": eul_est[i,1], "z": eul_est[i,2] })
#     data = {
#             "time_stamp": ts_list,
#             "eul_gt": eul_gt_list,
#             "eul_est": eul_est_list,
#         }
#     comm_send = ReplayDataSender(data)
#     comm_send.start()


# # def unpack_json(fName):
# #     f = open(fName)
# #     data = json.load(f)
# #     ts = data["time_stamp"]
# #     ts = np.array(ts)
# #     ts -= ts[0]
# #     eul = unspool(data["eul"])
# #     angvel = unspool(data["angvel"])
# #     gyro = unspool(data["gyro"])
# #     acc = unspool(data["acc"])
# #     mag = unspool(data["mag"])
# #     return ts, eul, angvel, gyro, acc, mag

# # def unspool(list_xyz):
# #     N = len(list_xyz)
# #     data_N3 = np.zeros((N,3))
# #     for i in range(0, N):
# #         xyz = list_xyz[i]
# #         data_N3[i, 0] = xyz["x"]
# #         data_N3[i, 1] = xyz["y"]
# #         data_N3[i, 2] = xyz["z"]
# #     return data_N3

# class RequestIMUData:
#     def __init__(self) -> None:
#         websocket.enableTrace(False)
#         self.stop_flag = False
#         self.tic = time.time()
#         self.ws = websocket.WebSocketApp("ws://localhost:12740",
#                                          on_open=self.on_open,
#                                          on_message=self.on_message,
#                                          on_error=self.on_error,
#                                          on_close=self.on_close)

#     def start(self):
#         self.ws.run_forever()

#     def on_message(self, ws, message):
#         data = json.loads(message)
#         if ("ignore" not in data or data["ignore"] == 0):
#             if (data["msg_type"] == 1):
#                 i = 0
#                 while os.path.exists("sim_data_%s.json" % i):
#                     i += 1
#                 with open(f'sim_data_{i}.json', "w") as write_file:
#                     json.dump(data["logged_sim_data"], write_file, indent=4)
#                 self.stop_flag = True

#     def on_error(self, ws, error):
#         print("Force closing...")

#     def on_close(self, ws, close_status_code, close_msg):
#         print("Closing now.")

#     def on_open(self, ws):
#         def run(*args):
#             while(True):
#                 if ((time.time() - self.tic)>5):
#                     print('Failed to fetch the data. Is the connection established?')
#                     break
#                 time.sleep(1)
#                 x = {"id": "jupyter", "debug": 0}
#                 ws.send(json.dumps(x))
#                 if (self.stop_flag):
#                     print('Received the data.')
#                     break

#             ws.close()
#         _thread.start_new_thread(run, ())

# def get_data2send(replay_data):
#     return {
#         "id": "jupyter",
#         "msg_type": 2,
#         "replay_data": replay_data
#     }

# class ReplayDataSender:
#     def __init__(self,  replay_data):
#         self.replay_data = replay_data
#         websocket.enableTrace(False)
#         self.ws = websocket.WebSocketApp("ws://localhost:12740",
#                                          on_open=self.on_open,
#                                          on_message=self.on_message,
#                                          on_error=self.on_error,
#                                          on_close=self.on_close)
#     def start(self):
#         self.ws.run_forever()

#     def on_message(self, ws, message):
#         pass

#     def on_error(self, ws, error):
#         print("Force closing...")

#     def on_close(self, ws, close_status_code, close_msg):
#         print("Closing now.")

#     def on_open(self, ws):
#         def run(*args):
#             for i in range(10**2):

#                 # time.sleep(0.1)
#                 x = get_data2send(self.replay_data)
#                 ws.send(json.dumps(x))
#                 print("Data has been sent.")
#                 break
            
#             ws.close()
#         _thread.start_new_thread(run, ())



