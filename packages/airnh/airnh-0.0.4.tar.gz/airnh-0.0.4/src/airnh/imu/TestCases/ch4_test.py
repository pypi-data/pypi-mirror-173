from .testbase import *
from ..Functions.DataReader import DataReader
from ..Functions.SO3 import SO3

class ch4_test():
    def __init__(self, fName):
        self.fName = fName

    #rotm multiplication
    def ch4_ex1_a_test(self,foo):
        eul = np.random.rand(3)*np.pi
        R = SO3.eul2rotm(eul)
        v = np.array([1, 1, 1])
        v_est = foo(R, v)
        v_true = np.matmul(R,v)
        cond = compArraySim(v_est, v_true)
        checker(cond, "Rotation Matrix Multiplication")

    # inverse rotm
    def ch4_ex1_b_test(self,foo):
        eul = (np.random.rand(3)-1)*np.pi/2
        R = SO3.eul2rotm(eul)
        Rinv_est = foo(R)
        Rinv_true = np.linalg.inv(R)
        cond = compArraySim(Rinv_est, Rinv_true)
        checker(cond, "Rotation Marix Inverse")

    # inverse rotm by transpose
    def ch4_ex1_c_test(self,foo):
        eul = (np.random.rand(3)-1)*np.pi/2
        R = SO3.eul2rotm(eul)
        Rinv_est = foo(R)
        Rinv_true = R.T
        cond = compArraySim(Rinv_est, Rinv_true)
        checker(cond, "Rotation Marix Transpose")

    # get rotationMat
    def ch4_ex2_a_test(self,foo):
        ang = 0.11 # rad
        cond = True
        for i in range(0, 3):
            cond = cond and compArraySim(SO3.getRotationMat(i, ang), foo(i, ang), 10**-3)
        checker(cond, "Single Axis Rotation Matirx")

    # eul2rotm
    def ch4_ex2_a2_test(self,foo):
        eul = (np.random.rand(3)-1)*np.pi/2
        R = SO3.eul2rotm(eul)
        cond = compArraySim(R, foo(eul))
        checker(cond, "Euler Angle to Rotation Matrix")

    # matrix concat
    def ch4_ex2_a3_test(self, foo):
        eul_01 = np.array([30, 0, 0])*np.pi/180
        eul_12 = np.array([0, 10, 30])*np.pi/180
        Rt0 = np.eye(3)
        R_est = foo(Rt0, eul_01, eul_12)
        R_true = np.matmul(np.matmul(Rt0, SO3.eul2rotm(eul_01)), SO3.eul2rotm(eul_12))
        cond = compArraySim(R_est, R_true)
        checker(cond, "Matrix Concatenation")

    # rotm 2 eul
    def ch4_ex2_b_test(self, foo):
        eul = (np.random.rand(3)-1)*np.pi/2
        R = SO3.eul2rotm(eul)
        eul_est = foo(R)
        eul_true = SO3.rotm2eul(R)
        cond = compArraySim(eul_est, eul_true)
        checker(cond, "Rotation Matrix to Euler Angle")

    # get_skew
    def ch4_ex3_a_test(self,foo):
        w = (np.random.rand(3)-1)*np.pi/2*0.01
        skew_est = foo(w)
        skew_true = SO3.get_skew(w)
        cond = compNPArray(skew_est, skew_true)
        checker(cond, "Skew Symmetric Matrix")

    # exp map
    def ch4_ex3_a2_test(self,foo):
        w = (np.random.rand(3)-1)*np.pi/2*0.01
        dt = 0.02
        dR_est = foo(w, dt)
        dR_true = SO3.get_dR(w, dt)
        cond = compArraySim(dR_est, dR_true, 10**-3)
        checker(cond, "Exponential Map")

    def ch4_ex3_b_test(self, foo):
        w = (np.random.rand(3)-1)*np.pi/2*0.01
        dt = 0.02
        R_est = foo(np.eye(3), w, dt)
        R_true = SO3.get_nextR(np.eye(3), w, dt)
        cond = compArraySim(R_est, R_true, 10**-3)
        checker(cond, "Next Rotation Matrix")

    def ch4_ex3_c_test(self, so3, fName):
        dr = DataReader(fName)
        i = 1234
        print(so3.acc2eul(dr.acc[i]))
        cond1 = compArraySim(SO3.acc2eul(dr.acc[i]), so3.acc2eul(dr.acc[i]),10**-3)
        cond2 = compArraySim(SO3.mag2eul(dr.mag[i], dr.euler[i]), so3.mag2eul(dr.mag[i], dr.euler[i]),10**-3)
        R1 = SO3.eul2rotm(dr.euler[i])
        R2 = so3.eul2rotm(dr.euler[i])
        cond3 = compArraySim(R1, R2, 10**-3)
        cond4 = compArraySim(SO3.rotm2eul(R1), so3.rotm2eul(R1), 10**-3)
        cond5 = compArraySim(SO3.get_nextR(np.eye(3), dr.angVel[i], 0.02), so3.get_nextR(np.eye(3), dr.angVel[i], 0.02), 10**-3)
        checker(cond1, "SO3.acc2eul")
        checker(cond2, "SO3.mag2eul")
        checker(cond3, "SO3.eul2rotm")
        checker(cond4, "SO3.rotm2eul")
        checker(cond5, "SO3 - get_dR / get_skew / get_nextR")
