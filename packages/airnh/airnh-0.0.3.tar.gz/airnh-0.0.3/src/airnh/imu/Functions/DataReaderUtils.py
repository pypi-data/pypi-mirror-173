import json
import numpy as np

def unpack_json(fName):
    f = open(fName)
    data = json.load(f)
    
    ts = data["time_stamp"]
    ts = np.array(ts)
    ts -= ts[0]
    eul = unspool(data["eul"])
    angvel = unspool(data["angvel"])
    gyro = unspool(data["gyro"])
    acc = unspool(data["acc"])
    mag = unspool(data["mag"])
    return ts, eul, angvel, gyro, acc, mag

def unspool(list_xyz):
    N = len(list_xyz)
    data_N3 = np.zeros((N,3))
    for i in range(0, N):
        xyz = list_xyz[i]
        data_N3[i, 0] = xyz["x"]
        data_N3[i, 1] = xyz["y"]
        data_N3[i, 2] = xyz["z"]
    return data_N3