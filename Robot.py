from dataclasses import dataclass

import numpy as np
from flask import jsonify
from Joystick import Joystick


@dataclass
class RobotData:
    status: int = 0
    robot_id: int = 0
    robot_ip: int = 0
    first_motor_speed: int = 0
    second_motor_speed: int = 0
    third_motor_speed: int = 0
    kicker: int = 0
    battery: int = 0


class Robot:
    robotIndex = '_1'
    robotData = RobotData()
    # построение матрицы преобразования для получения скоростей на моторы
    platform_radius = 1
    wheel_radius = 2
    R = wheel_radius * np.array([[-platform_radius, 1, 0],
                                 [-platform_radius, -0.5, -np.sin(np.pi / 3)],
                                 [-platform_radius, -0.5, np.sin(np.pi / 3)]])
    # r_norm = R.dot(np.array([[1], [0], [0]]))
    r_norm = [1 + platform_radius, platform_radius + 0.5 + np.sin(np.pi / 3), platform_radius + 0.5 + np.sin(np.pi / 3)]

    def __init__(self, index):
        self.robotIndex = index

    def updData(self, data: Joystick):
        v = np.array([[data.rotate], [data.move[0]], [data.move[1]]])
        res = self.R.dot(v)
        res = list(res)
        res = [res[0] / self.r_norm[0], res[1] / self.r_norm[1], res[2] / self.r_norm[2]]
        for i in res:
            if i > 126:
                i = 126
            if i < -128:
                i = -127
        self.robotData.first_motor_speed = int(res[0] * 127)
        self.robotData.second_motor_speed = int(res[1] * 127)
        self.robotData.third_motor_speed = int(res[2] * 127)

        self.robotData.kicker = data.kicker

    def generateJson(self):
        file = jsonify({
            'robot_ip_address': self.robotData.robot_ip,
            'robot_id': self.robotData.robot_id,
            'first_motor_speed': self.robotData.first_motor_speed,
            'second_motor_speed': self.robotData.second_motor_speed,
            'third_motor_speed': self.robotData.third_motor_speed,
            'kicker_status': self.robotData.kicker,
            'battery_life': self.robotData.battery,
            'status': self.robotData.status
        })
        return file
