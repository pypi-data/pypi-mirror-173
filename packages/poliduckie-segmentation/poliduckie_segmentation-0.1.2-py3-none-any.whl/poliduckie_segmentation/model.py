import os

import casadi as ca
import numpy as np

class Model:
    def __init__(self, dt=10):
        pkg_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'robot_model.casadi')
        self.model = ca.Function.load(model_path)

    def get_model(self):
        return self.model
      
    def step(self, x, y, theta, speed, angular_speed, action):
        return self.model([pose.x, pose.y, pose.theta, 0, 0], action)
