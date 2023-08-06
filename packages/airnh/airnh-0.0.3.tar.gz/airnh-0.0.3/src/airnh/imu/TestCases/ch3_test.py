from .testbase import *
from ..Functions.DataReader import DataReader
from ..Functions.SO3 import SO3
from ..Functions.NumericalCalculus import *

class ch3_test():
    def __init__(self, fName):
        self.fName = fName

    def ch3_ex1_a_test(self,foo):
        fName = self.fName
        test_data = DataReader(fName, False).data
        foo_data = foo(fName)
        checker(compArraySim(test_data, foo_data), "Reading Data")

    def ch3_ex1_b_test(self,foo):
        fName = self.fName
        dr = DataReader(fName, scale=False)
        ts, e, av, a, g, m = foo(dr.data)
        checker(compNPArray(ts, dr.timeStamp), "Time Stamp")
        checker(compNPArray(e, dr.euler), "Euler Angle")
        checker(compNPArray(av, dr.angVel), "Angular Velocity")
        checker(compNPArray(a, dr.acc), "Acceleration")
        checker(compNPArray(g, dr.gyro), "Gyroscope")
        checker(compNPArray(m, dr.mag), "Magnetometer")

    def ch3_ex1_c_test(self,foo):
        fName = self.fName
        dr = DataReader(fName, False)
        euler_si, acc_si, gyro_si, mag_si = foo(dr.euler, dr.acc, dr.gyro, dr.mag)
        dr2 = DataReader(fName, True)
        checker(compArraySim(euler_si, dr2.euler), "Euler")
        checker(compArraySim(acc_si, dr2.acc), "acc")
        checker(compArraySim(gyro_si, dr2.gyro), "gyro")
        checker(compArraySim(mag_si, dr2.mag), "mag")

    def ch3_ex1_c2_test(self,foo):
        fName = self.fName
        dr = DataReader(fName, True)
        ts = dr.timeStamp
        ts = foo(ts)
        dr2 = DataReader(fName)
        checker(compArraySim(dr2.timeStamp, ts),"Time Stamp")

    def ch3_ex1_d_test(self,fooClass):
        fName = self.fName
        dr = DataReader(fName)
        dr_test = fooClass(fName)
        cond = compArraySim(dr.euler, dr_test.euler)
        cond &= compArraySim(dr.acc, dr_test.acc)
        cond &= compArraySim(dr.gyro, dr_test.gyro)
        cond &= compArraySim(dr.mag, dr_test.mag)
        cond &= compArraySim(dr.timeStamp, dr_test.timeStamp)
        checker(cond, "Data Reader Class")
        
    #===============================================================
    def ch3_ex2_a_test(self, foo):
        fName = self.fName
        dr = DataReader(fName)
        eul_xyz = dr.euler[500]
        acc = dr.acc[500]
        eul_xy_est = foo(acc)
        eul_xyz[2] = 0
        checker(compArraySim(eul_xy_est, eul_xyz, tolerance=10**-3), 
        "Accelerometer to Euler Roll and Pitch")
    
    def ch3_ex2_b_test(self, foo):
        fName = self.fName
        dr = DataReader(fName)
        eul_xyz = dr.euler[500]
        mag = dr.mag[500]
        eul_z = foo(mag, eul_xyz)
        checker(compArraySim(np.array([0, 0, eul_xyz[2]]), eul_z, tolerance=10**-3), 
        "Magnetometer to Euler Yaw")
    
    #===============================================================
    def ch3_ex3_a_test(self, foo):
        t = np.arange(0, 2*np.pi, 0.02)
        data = np.sin(t)
        der_est = foo(data, t)
        der_true = derivative(data, t)
        cond1 = compArraySim(der_est, der_true)
        cond2 = compArraySim(der_est[1:], der_true)
        cond3 = compArraySim(der_est[:-1], der_true)
        checker(cond1 or cond2 or cond3, "Numerical Derivative")
    
    def ch3_ex3_b_test(self, foo):
        t = np.arange(0, 2*np.pi, 0.02)
        data = np.sin(t)
        itg_est = foo(data, t)
        itg_true = integrate(data, t)
        cond1 = compArraySim(itg_est, itg_true)
        cond2 = compArraySim(itg_est[1:], itg_true)
        cond3 = compArraySim(itg_est[:-1], itg_true)
        checker(cond1 or cond2 or cond3, "Numerical Integaration")
    
    def ch3_ex3_c_test(self, foo):
        dr = DataReader(self.fName)
        ts = dr.timeStamp
        gyro_array = dr.gyro
        gyro_itg_est = foo(gyro_array, ts)
        gyro_itg_true = integrate(gyro_array, ts)
        cond1 = compArraySim(gyro_itg_est, gyro_itg_true, 10**-3)
        checker(cond1, "Gryo Integration")


    
