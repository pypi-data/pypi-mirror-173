from .DataReaderUtils import unpack_json
import pandas as pd
import numpy as np

class DataReader():
    def __init__(self, fName, scale=True):
        self.fName = fName
        ts, eul, angVel, gyro, acc, mag = unpack_json(self.fName)
        self.timeStamp = ts
        self.euler = eul
        self.angVel = angVel
        self.gyro = gyro
        self.acc = acc
        self.mag = mag

        if scale:
            # scale data
            self.scaleData()

    def scaleData(self):
        self.euler *= np.pi/180
        self.acc *= 2.*9.81/32768.
        self.gyro *= (250 * np.pi / 180)/32768.
        self.mag *= 200./32768.
