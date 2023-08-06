from .testbase import *
from ..Functions.DataReader import DataReader
from ..Functions.SO3 import SO3
from ..Functions.Filters import *

class ch5_test():
    def __init__(self, fName):
        self.fName = fName
        noise = np.random.rand(100, 3)
        t = np.linspace(0, 10, 100)
        self.data = np.array([np.sin(t),np.cos(t),np.sin(t)]).T + noise

    def ch5_ex1_a_test(self, foo):
        avgFilt_est = foo(self.data, 10)
        avgFilt_true = avgFilter(self.data, 10)
        cond1 = compArraySim(avgFilt_est, avgFilt_true, 10**-4)
        checker(cond1, "Average Filter")

    def ch5_ex1_b_test(self, foo):
        lpFilt_est = foo(self.data, 0.9)
        lpFilt_true = lowpassFilter(self.data, 0.9)
        cond1 = compArraySim(lpFilt_est, lpFilt_true, 10**-4)
        checker(cond1, "Low Pass Filter")

    def ch5_ex2_a_test(self, foo):
        dr = DataReader(self.fName)
        i = 1234
        eul = dr.euler[i] + (np.random.rand(3)-0.5)*np.pi/3
        R = SO3.eul2rotm(eul)
        acc = dr.acc[i]
        err_est = foo(R, acc)
        err_true = DCM.err_meas_acc(R, acc)
        cond1 = compArraySim(err_est, err_true, 10**-4)
        checker(cond1, "Error Measurement by Accelerometer")

    def ch5_ex2_b_test(self, foo):
        dr = DataReader(self.fName)
        i = 1234
        eul = dr.euler[i] + (np.random.rand(3)-0.5)*np.pi/3
        R = SO3.eul2rotm(eul)
        mag = dr.mag[i]
        err_est = foo(R, mag)
        err_true = DCM.err_meas_mag(R, mag)
        cond1 = compArraySim(err_est, err_true, 10**-4)
        checker(cond1, "Error Measurement by Magnetometer")

    def ch5_ex2_c_test(self, foo):
        dr = DataReader(self.fName)
        i = 1234
        eul = dr.euler[i] + (np.random.rand(3)-0.5)*np.pi/3
        R = SO3.eul2rotm(eul)
        mag = dr.mag[i]
        acc = dr.acc[i]
        err_est = foo(R, acc, mag)
        err_true = DCM.err_meas_bdy(R, acc, mag)
        cond1 = compArraySim(err_est, err_true, 10**-4)
        checker(cond1, "Error Measurement in Body Frame")

    def ch5_ex2_d_test(self, foo):
        dr = DataReader(self.fName)
        i = 1234
        eul = dr.euler[i] + (np.random.rand(3)-0.5)*np.pi/3
        R = SO3.eul2rotm(eul)
        R_est = foo(R)
        R_true = DCM.orthonormalization(R)
        cond1 = compArraySim(R_est, R_true, 10**-4)
        checker(cond1, "Orthonormalization")






