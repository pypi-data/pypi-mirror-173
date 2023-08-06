from scipy import integrate
import numpy as np
from abc import abstractmethod
import time
import json
import websocket
import _thread


class InvPenEnvironment():
    def __init__(self, ic=[0.0, 0.0, np.pi, 0.01], dt=0.1,
                 m=5, M=10, L=1, g=-9.8, ):
        self.x = ic
        self.m = m
        self.M = M
        self.L = L
        self.g = g
        self.d = 1  # friction(damping) term
        self.u = 0  # ctrl input
        self.dt = dt
        self.r = integrate.ode(self.get_dx).set_integrator(
            "dopri5")  # dori5= runge kutta 45

    def get_next(self, u):
        t = np.array([0, self.dt])
        # intital state = current state & initial time = 0
        self.r.set_initial_value(self.x, t[0])
        self.u = u
        self.x = self.r.integrate(self.dt)
        # self.x = self.x + self.get_dx(0, self.x)*self.dt
        return self.x

    def get_dx(self, t, x):
        sinx = np.sin(x[2])
        cosx = np.cos(x[2])
        denom = self.m*self.L**2*(self.M+self.m*(1-cosx**2))
        dx = ([0, 0, 0, 0])
        dx[0] = x[1]
        dx[1] = (1/denom)*(-self.m**2*self.L**2*self.g*cosx*sinx + self.m*self.L**2 *
                           (self.m*self.L*x[3]**2*sinx - self.d*x[1])) + self.m*self.L**2*(1/denom)*self.u
        dx[2] = x[3]
        dx[3] = (1/denom)*((self.m+self.M)*self.m*self.g*self.L*sinx - self.m*self.L*cosx *
                           (self.m*self.L*x[3]**2*sinx - self.d*x[1])) - self.m*self.L*cosx*(1/denom)*self.u
        return dx


class IPControlBase:
    def __init__(self):
        self.hist_list = []
        self.state = None

    @abstractmethod
    def calc_new_input(self):
        pass

    def step(self):
        self.state = self.env.get_next(self.u)
        new_list = [time.time(), *self.state, self.u]
        self.hist_list.append(new_list)

    def get_msg(self):
        return json.dumps({
            "id": "jupyter",
            "states_msg": {
                "position": self.state[0],
                "angle": self.state[2]*180/np.pi,
            }
        })

    def get_states_info(self):
        return np.array(self.hist_list, dtype=object)


class IPSimManager:
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
            ws.close()
            print("thread terminating...")
        _thread.start_new_thread(run, ())
