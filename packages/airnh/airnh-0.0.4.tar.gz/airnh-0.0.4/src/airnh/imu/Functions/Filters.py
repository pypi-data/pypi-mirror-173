import numpy as np

def avgFilter(data, wLen):
    sum = 0
    avgFilt = np.zeros_like(data)
    indice = []
    for i in range(0, data.shape[0]):
        if np.mod(i, wLen) == 0 and i!=0:
            avg = sum/(wLen-1)
            avgFilt[indice] = avg
            sum = 0
            indice = []
        sum += data[i]
        indice.append(i)
    return avgFilt


def lowpassFilter(data, w):
    lp = np.zeros_like(data)
    for i in range(1, data.shape[0]):
        lp[i] = lp[i-1]*w + (1-w)*data[i]
    return lp


class DCM:
 
    @classmethod
    def orthonormalization(cls, R):
        error = np.dot(R[:,0], R[:,1])
        # orthogonalization
        R0 = R[:,0] - error/2*R[:,1]
        R1 = R[:,1] - error/2*R[:,0]
        R2 = np.cross(R0, R1)
        # renormalization
        R[:,0] = 0.5*(3 - np.dot(R0, R0))*R0
        R[:,1] = 0.5*(3 - np.dot(R1, R1))*R1
        R[:,2] = 0.5*(3 - np.dot(R2, R2))*R2
        return R

    @classmethod
    def err_meas_acc(cls, R_b2g, acc_bdy):
        acc_scaled = acc_bdy/9.81
        g_true = [0, 0, -1]
        acc_gnd = R_b2g@acc_scaled
        err_gnd = np.cross(acc_gnd, g_true)
        return err_gnd
    
    @classmethod
    def err_meas_mag(cls, R, mag):
        mag_scaled = mag/np.linalg.norm(mag)
        mag_true = [1, 0, 0]
        mag_gnd = R@mag_scaled
        mag_gnd[2] = 0
        err_mag_gnd = np.cross(mag_gnd, mag_true)
        return err_mag_gnd

    @classmethod
    def err_meas_bdy(cls, R, acc, mag):
        err_meas_gnd = DCM.err_meas_acc(R, acc) + DCM.err_meas_mag(R, mag)
        err_meas_bdy = np.matmul(R.T, err_meas_gnd)        
        return err_meas_bdy



        