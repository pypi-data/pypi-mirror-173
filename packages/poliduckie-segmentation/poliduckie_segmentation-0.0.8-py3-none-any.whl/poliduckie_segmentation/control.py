import os

import casadi as ca
import numpy as np

class MPC:
    def __init__(self, dt=10):
        pkg_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'mpc_model', 'MPC.casadi')
        self.model = ca.Function.load(model_path)
        self.delay = round(0.15/dt)
        self.u_delay0 = ca.DM(np.zeros((2, self.delay)))

    def get_model(self):
        return self.model

    def mpc(self, x, r, tr=None, u_delay=None,  Q1=1e3, Q2=5e-4, Q3=1, R=1e-3):
        """
        x: state
        r: reference
        tr: angular reference
        u_delay: delayed control input
        Q1: weight on position error
        Q2: weight on angular error
        Q3: weight on max speed
        R: weight on control input
        """
        if tr is None:
            Q2 = 0
            tr = 0
        if u_delay is None:
            u_delay = self.u_delay0
        return self.model(x, r, tr, u_delay, Q1, Q2, Q3, R)
