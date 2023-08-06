from abc import ABC, abstractmethod
import json
from logging import exception
import numpy as np
import websocket
import time
import _thread
from enum import Enum


class CONTROL_MODE(Enum):
    REMOTE = 0
    ONBOARD = 1


class CONTROL_TYPE(Enum):
    PID_BLACKBOX_DEFAULT = 0
    PID_BLACKBOX_CASCADE = 1
    STATE_SPACE = 2


class ControlParams:
    def __init__(self):
        self.default_value = -10**5
        self.kp: float = self.default_value  # pid default only
        self.kd: float = self.default_value  # pid default only
        self.ki: float = self.default_value  # pid default only
        self.kp_pos: float = self.default_value  # for pid cascade only
        self.ki_pos: float = self.default_value  # for pid cascade only
        self.kp_vel: float = self.default_value  # for pid cascade only
        self.ki_vel: float = self.default_value  # for pid cascade only
        self.pos_err_lim: float = self.default_value  # for pid defualt & cascase
        self.vel_err_lim: float = self.default_value  # for pid cascade only
        self.target_pos: float = self.default_value   # for all
        self.A: np.ndarray = np.ones((2, 2))*self.default_value  # for state space only
        self.B: np.ndarray = np.ones((2, 1))*self.default_value  # for state space only
        self.K: np.ndarray = np.ones((1, 2))*self.default_value  # for state space only

    def validate(self, ctrl_type: CONTROL_TYPE):
        if (ctrl_type == CONTROL_TYPE.PID_BLACKBOX_DEFAULT):
            if (self.isDefault(self.kp) or
                    self.isDefault(self.kd) or
                    self.isDefault(self.ki) or
                    self.isDefault(self.pos_err_lim) or
                    self.isDefault(self.target_pos)):
                print(f"==========================================================")
                print(f"kp: {self.kp}, kd: {self.kd}, ki: {self.ki}, \n \
                        pos_err_lim: {self.pos_err_lim},,\n \
                        self.target_pos: {self.target_pos}")
                raise exception.ValueError(
                    "Some invalid control params for PID_BLACKBOX_DEFAULT")
        elif (ctrl_type == CONTROL_TYPE.PID_BLACKBOX_CASCADE):
            if (self.isDefault(self.kp_pos) or
                    self.isDefault(self.ki_pos) or
                    self.isDefault(self.kp_vel) or
                    self.isDefault(self.ki_vel) or
                    self.isDefault(self.pos_err_lim) or
                    self.isDefault(self.vel_err_lim) or
                    self.isDefault(self.target_pos)):
                print(f"==========================================================")
                print(f"kp_pos: {self.kp_pos}, ki_pos: {self.ki_pos}, \n \
                        kp_vel: {self.kp_vel}, ki_vel: {self.ki_vel}, \n \
                        pos_err_lim: {self.pos_err_lim}, vel_err_lim: {self.vel_err_lim}, \n \
                        self.target_pos: {self.target_pos}")
                raise exception.ValueError(
                    "Some invalid control params for PID_BLACKBOX_CASECADE")

        elif (ctrl_type == CONTROL_TYPE.STATE_SPACE):
            if(self.isDefault(self.A, case=1) or
                    self.isDefault(self.B, case=1) or
                    self.isDefault(self.K, case=1) or
                    self.isDefault(self.target_pos)):
                print(f"==========================================================")
                print(f"A: {self.A}, B: {self.B}, K: {self.K}, \n \
                        self.target_pos: {self.target_pos}")
                raise exception.ValueError(
                    "Some invalid control params for STATE_SPACE")

    def isDefault(self, value, case=0):
        if (case == 0):
            return True if value == self.default_value else False
        else:
            arr = value.reshape(-1)
            size = arr.shape
            comp = np.ones(size)*self.default_value
            diff = np.linalg.norm(arr - comp)
            return True if (diff < 10**-3) else False

    def pack(self, ctrl_type: CONTROL_TYPE):
        self.validate(ctrl_type)
        msg = {}
        msg["kp"] = self.kp
        msg["kd"] = self.kd
        msg["ki"] = self.ki
        msg["kp_pos"] = self.kp_pos
        msg["ki_pos"] = self.ki_pos
        msg["kp_vel"] = self.kp_vel
        msg["ki_vel"] = self.ki_vel
        msg["pos_err_lim"] = self.pos_err_lim
        msg["vel_err_lim"] = self.vel_err_lim
        msg["target_pos"] = self.target_pos
        msg["A"] = self.A.reshape(-1).tolist()
        msg["B"] = self.B.reshape(-1).tolist()
        msg["K"] = self.K.reshape(-1).tolist()
        return msg

    def isDifferent(self, ctrl_type: CONTROL_TYPE, msg):
        # print(self.kp)
        EPSILON = 10**-3

        if(ctrl_type == CONTROL_TYPE.PID_BLACKBOX_DEFAULT):
            cond0 = np.abs(self.kp - msg["kp"]) < EPSILON
            cond1 = np.abs(self.kd - msg["kd"]) < EPSILON
            cond2 = np.abs(self.ki - msg["ki"]) < EPSILON
            cond3 = np.abs(self.pos_err_lim - msg["pos_err_lim"]) < EPSILON
            cond4 = np.abs(self.target_pos - msg["target_pos"]) < EPSILON
            if (cond0 and cond1 and cond2 and cond3 and cond4):
                return False
            else:
                return True
        elif(ctrl_type == CONTROL_TYPE.PID_BLACKBOX_CASCADE):
            cond0 = np.abs(self.kp_pos - msg["kp_pos"]) < EPSILON
            cond1 = np.abs(self.ki_pos - msg["ki_pos"]) < EPSILON
            cond2 = np.abs(self.kp_vel - msg["kp_vel"]) < EPSILON
            cond3 = np.abs(self.ki_vel - msg["ki_vel"]) < EPSILON
            cond4 = np.abs(self.pos_err_lim - msg["pos_err_lim"]) < EPSILON
            cond5 = np.abs(self.vel_err_lim - msg["vel_err_lim"]) < EPSILON
            cond6 = np.abs(self.target_pos - msg["target_pos"]) < EPSILON
            if (cond0 and cond1 and cond2 and cond3 and cond4 and cond5 and cond6):
                return False
            else:
                return True
        elif(ctrl_type == CONTROL_TYPE.STATE_SPACE):
            cond0 = np.linalg.norm(self.A.reshape(-1) - msg["A"]) < EPSILON
            cond1 = np.linalg.norm(self.B.reshape(-1) - msg["B"]) < EPSILON
            cond2 = np.linalg.norm(self.K.reshape(-1) - msg["K"]) < EPSILON
            cond3 = np.linalg.norm(self.target_pos - msg["target_pos"]) < EPSILON
            if (cond0 and cond1 and cond2 and cond3):
                return False
            else:
                return True
        else:
            print("This should not happen")
            print("Invalid control type")
            exit(-1)


class ControllerBase(ABC):
    def __init__(self, ctrl_mode, ctrl_type):
        super().__init__()
        if (ctrl_mode is None):
            self.ctrl_mode = CONTROL_MODE.REMOTE
        else:
            self.ctrl_mode: CONTROL_MODE = ctrl_mode
        self.ctrl_type: CONTROL_TYPE = ctrl_type
        self.ctrl_params: ControlParams = ControlParams()
        self.input_acc = 0

    def get_datapack_remote_control(self):
        return {
            "id": "jupyter",
            "debug": 0,
            "msg_type": 0,
            "states_msg": {
                "input_acc": self.input_acc,
            },
        }

    def need_to_setup_ctrl_mode(self, msg):
        if (self.ctrl_mode.name != msg["sim_params_msg"]["ctrl_mode"]):
            return True, self.get_controlmode_setup_msg()
        else:
            # print("im here 1")
            return False, {}

    def get_controlmode_setup_msg(self):
        return {
            "id": "jupyter",
            "debug": 0,
            "msg_type": 1,
            "sim_params_msg": {
                "ctrl_mode": self.ctrl_mode.name,
                "ctrl_type": self.ctrl_type.name, }
        }

    # def need_to_setup_ctrl_params(self, msg):
    #     if (self.ctrl_mode == CONTROL_MODE.ONBOARD):
    #         # print("im here 2")
    #         # return True, {}
    #         return True, self.get_controlparams_onboard_control()

    #     if (self.ctrl_params.isDifferent(self.ctrl_type, msg["control_params_msg"])):
    #         return True, self.get_controlparams_onboard_control()
    #     else:
    #         # print("im here 3")
    #         return False, {}
    def need_to_setup_ctrl_params(self, msg):
        if (self.ctrl_mode == CONTROL_MODE.ONBOARD):
            # print("im here 2")
            # return True, {}
            #return True, self.get_controlparams_onboard_control()

            if (self.ctrl_params.isDifferent(self.ctrl_type, msg["control_params_msg"])):
                return True, self.get_controlparams_onboard_control()
            else:
                # print("im here 3")
                return False, {}
        else:
            return False, {}


    def get_controlparams_onboard_control(self):
        return {
            "id": "jupyter",
            "debug": 0,
            "msg_type": 2,
            "control_params_msg": self.ctrl_params.pack(self.ctrl_type)
        }

    def process_control_update(self, states_msg):
        # put data probe here for onboard control
        # data_logger.update(states_msg)
        if (self.ctrl_mode == CONTROL_MODE.REMOTE):
            self.input_acc = self.updateControlOutput(states_msg)
            # put data probe here for remote control
            data_logger.update_remote_case(states_msg, self.input_acc)
        else:
            self.input_acc = self.updateControlOutput(states_msg)
            data_logger.update(states_msg)

    @ abstractmethod
    def updateControlOutput(self, states_msg):
        """
        Update the control output based on the states_msg
        :param states_msg: dictionary of states
        :return: input acceleration (scalar value)
        """
        pass


class PIDSimple(ControllerBase, ABC):
    def __init__(self,):
        self.ctrl_type = CONTROL_TYPE.PID_BLACKBOX_DEFAULT
        super().__init__(CONTROL_MODE.REMOTE, self.ctrl_type)
        self.kp = 0
        self.kd = 0
        self.ki = 0
        self.pos_err_lim = 0
        self.target_pos = 0
        self.pos_err_int = 0
        self.set_ctrl_params_onboard(kp=0, kd=0, ki=0, pos_err_lim=0, target_pos=0)

    def set_ctrl_params_onboard(self, kp, kd, ki, pos_err_lim, target_pos):
        self.ctrl_params.kp = kp
        self.ctrl_params.kd = kd
        self.ctrl_params.ki = ki
        self.ctrl_params.pos_err_lim = pos_err_lim
        self.ctrl_params.target_pos = target_pos

    @abstractmethod
    def updateControlOutput(self, states_msg):
        pass


class PID_Default(ControllerBase, ABC):
    def __init__(self, ctrl_mode):
        self.ctrl_type = CONTROL_TYPE.PID_BLACKBOX_DEFAULT
        super().__init__(ctrl_mode, self.ctrl_type)
        self.kp = 0
        self.kd = 0
        self.ki = 0
        self.pos_err_lim = 0
        self.target_pos = 0
        self.pos_err_int = 0
        #self.set_ctrl_params_onboard(kp=0, kd=0, ki=0, pos_err_lim=0, target_pos=0)

    def set_ctrl_params_onboard(self, kp, kd, ki, pos_err_lim, target_pos):
        self.ctrl_params.kp = kp
        self.ctrl_params.kd = kd
        self.ctrl_params.ki = ki
        self.ctrl_params.pos_err_lim = pos_err_lim
        self.ctrl_params.target_pos = target_pos

    @abstractmethod
    def updateControlOutput(self, states_msg):
        pass


class PID_Cascade(ControllerBase, ABC):
    def __init__(self, ctrl_mode):
        self.ctrl_type = CONTROL_TYPE.PID_BLACKBOX_CASCADE
        super().__init__(ctrl_mode, self.ctrl_type)

    def set_ctrl_params_onboard(self, kp_pos, ki_pos, kp_vel, ki_vel, pos_err_lim, vel_err_lim, target_pos):
        self.ctrl_params.kp_pos = kp_pos
        self.ctrl_params.ki_pos = ki_pos
        self.ctrl_params.kp_vel = kp_vel
        self.ctrl_params.ki_vel = ki_vel
        self.ctrl_params.pos_err_lim = pos_err_lim
        self.ctrl_params.vel_err_lim = vel_err_lim
        self.ctrl_params.target_pos = target_pos

    @abstractmethod
    def updateControlOutput(self, states_msg):
        pass


class State_Space(ControllerBase, ABC):
    def __init__(self, ctrl_mode):
        self.ctrl_type = CONTROL_TYPE.STATE_SPACE
        super().__init__(ctrl_mode, self.ctrl_type)

    def set_ctrl_params_onboard(self, A, B, K, target_pos):
        self.ctrl_params.A = A
        self.ctrl_params.B = B
        self.ctrl_params.K = K
        self.ctrl_params.target_pos = target_pos

    @abstractmethod
    def updateControlOutput(self, states_msg):
        pass


class ControllerManager:
    def __init__(self):
        # self.config = SimConfig()
        self.controller: ControllerBase = None
        self.msg_incoming = None
        self.prev_pos = 0
        self.stopperCounter = 0
        self.stopFlag = False

    def update(self, data):
        self.msg_incoming = data
        msg_states = data["states_msg"]
        self.controller.process_control_update(msg_states)

    def stopChecker(self):
        if (self.msg_incoming is None):
            return False
        curr_pos = self.msg_incoming["states_msg"]["position"]
        diff = np.abs(self.prev_pos - curr_pos)
        if (diff < 10**-2):
            self.stopperCounter += 1

        self.prev_pos = curr_pos
        if(self.stopperCounter > 500):
            print('steady state reached. stopping now.')
            return True
        else:
            return False

    def get_msg(self):
        if (self.msg_incoming is not None):
            # check if sim mode is set
            needToSetupCtrlMode, msg = self.controller.need_to_setup_ctrl_mode(self.msg_incoming)
            if (needToSetupCtrlMode):
                return msg

            # check if sim control params are set
            needToSetupCtrlParams, msg = self.controller.need_to_setup_ctrl_params(self.msg_incoming)
            # print(needToSetupCtrlParams)
            # print(msg)
            if(needToSetupCtrlParams):
                return msg

        return self.controller.get_datapack_remote_control()

    def get_string_msg(self):
        return json.dumps(self.get_msg())


ctrlman = ControllerManager()



class DataLogger:
    def __init__(self):
        self.state_data = []
        self.input_data = []
        self.time_stamp = []

    def clear(self):
        self.state_data = []
        self.input_data = []
        self.time_stamp = []

    def update_remote_case(self, states_msg, input):
        new_pos = states_msg["position"]
        new_vel = states_msg["velocity"]
        new_input = input
        time_stamp = states_msg["time_stamp"]
        self.state_data.append([new_pos, new_vel])
        self.input_data.append(new_input)
        self.time_stamp.append(time_stamp)

    def update(self, states_msg):
        new_pos = states_msg["position"]
        new_vel = states_msg["velocity"]
        new_input = states_msg["input_acc"]
        time_stamp = states_msg["time_stamp"]
        self.state_data.append([new_pos, new_vel])
        self.input_data.append(new_input)
        self.time_stamp.append(time_stamp)

    def get_data(self):
        time_stamps = np.array(self.time_stamp)
        states = np.array(self.state_data)
        inputs = np.array(self.input_data)
        time_stamps = time_stamps - time_stamps[0]
        return time_stamps, states, inputs

    def clear_data(self):
        self.state_data = []
        self.input_data = []


data_logger = DataLogger()



class SimManager:
    def __init__(self, timeout=5) -> None:
        data_logger.clear()
        self.ctrlman = ControllerManager()
        websocket.enableTrace(False)
        self.timeout = timeout
        self.tic = time.time()
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:12740",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def start(self):
        self.ws.run_forever()

    def register_controller(self, controller):
        self.ctrlman.controller = controller

    def on_message(self, ws, message):
        data = json.loads(message)
        if ("ignore" not in data or data["ignore"] == 0):
            try:
                self.ctrlman.update(data)
            except Exception as e:
                print(e)

    def on_error(self, ws, error):
        print(error)
        print("Force closing...")

    def on_close(self, ws, close_status_code, close_msg):
        print("Closing now.")

    def on_open(self, ws):
        def run(*args):
            while(True):
                # if(self.ctrlman.stopChecker()):
                if ((time.time() - self.tic) > self.timeout):
                    print("Time out. Stopping now.")
                    self.ws.close()
                    break

                time.sleep(0.019)
                ws.send(self.ctrlman.get_string_msg())
            ws.close()
            print("thread terminating...")
        _thread.start_new_thread(run, ())
