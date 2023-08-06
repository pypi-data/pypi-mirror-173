import numpy as np

class SO3:
    @classmethod
    def acc2eul(cls, acc):
        g = 9.81
        theta = np.arcsin(acc[0]/g)
        phi = -np.arcsin(acc[1]/(g*np.cos(theta)))
#        phi = np.arctan2(-acc[:,1], -acc[:,2])
#        theta = np.arctan2(acc[:,0], np.sqrt(acc[:,1]**2 + acc[:,2]**2))
        return np.array([phi, theta, 0])
    
    @classmethod
    def mag2eul(cls, mag, euler_xy):
        phi = euler_xy[0]
        theta = euler_xy[1]
        norm = np.linalg.norm(mag)
        mag /= norm 
        cosPsi = mag[0]/np.cos(theta)
        lhs = mag[2] - np.cos(phi)*np.sin(theta)*cosPsi
        epsilon = 10**-5
        sinPsi = lhs / (np.sin(phi) + epsilon)
        psi = np.arctan2(sinPsi, cosPsi)
        return np.array([0, 0, psi])

    @classmethod
    def getRotationMat(cls, axis, rad):
        R = -1
        if axis == 0:
            R = np.array([[1, 0, 0],
                          [0, np.cos(rad), -np.sin(rad)],
                          [0, np.sin(rad), np.cos(rad)]],)
        elif axis == 1:
            R = np.array([[np.cos(rad), 0,  np.sin(rad)],
                          [0, 1,  0],
                          [-np.sin(rad), 0, np.cos(rad)]])
        elif axis == 2:
            R = np.array([[np.cos(rad), -np.sin(rad),  0],
                          [np.sin(rad), np.cos(rad), 0],
                          [0, 0, 1]])
        else:
            pass
        return R
        
    @classmethod
    def eul2rotm(cls, euler):
        Rx = cls.getRotationMat(0, euler[0])
        Ry = cls.getRotationMat(1, euler[1])
        Rz = cls.getRotationMat(2, euler[2])
        return np.dot(np.dot(Rz, Ry), Rx )

    @classmethod
    def rotm2eul(cls, R):
        sy = np.sqrt(R[0,0]**2 + R[1,0]**2)
        phi = np.arctan2(R[2,1], R[2,2])
        theta = np.arctan2(-R[2,0], sy)
        psi = np.arctan2(R[1,0], R[0,0])
        return np.array([phi, theta, psi])
    
    @classmethod
    def get_skew(cls, w):
        skew = np.array([[0, -w[2], w[1]],
                         [w[2], 0, -w[0]],
                         [-w[1], w[0], 0]])
        return skew

    @classmethod
    def get_dR(cls, w, dt):
        skew = cls.get_skew(w)*dt
        th = np.sqrt(np.dot(w, w))
        if th == 0:
            dR = np.eye(3) 
        else:
            dR = np.eye(3)
            dR += np.sin(th) / th * skew 
            dR += (1 - np.cos(th)) / th ** 2 * np.matmul(skew, skew)
        return dR
    
    @classmethod
    def get_nextR(cls, R, w, dt):
        dR = cls.get_dR(w, dt)
        R_next = np.matmul(R, dR)
        return R_next
    

