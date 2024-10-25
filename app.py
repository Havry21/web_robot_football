import socket
import time
from flask import Flask, render_template, request
from flask import jsonify
import threading
from Robot import Robot, RobotData
import Joystick
import udpSender
import sys

app = Flask(__name__)

robotList = [Robot("_0"), Robot("_1"), Robot("_2"), Robot("_3")]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_parameters_0', methods=['GET'])
def get_parameters_0():
    return robotList[0].generateJson()


@app.route('/get_parameters_1', methods=['GET'])
def get_parameters_1():
    return robotList[1].generateJson()


@app.route('/get_parameters_2', methods=['GET'])
def get_parameters_2():
    return robotList[2].generateJson()


@app.route('/get_parameters_3', methods=['GET'])
def get_parameters_3():
    return robotList[3].generateJson()


def main(args=None):
    thread = list()
    sender = udpSender.UDPConvers(int(sys.argv[1]))
    print(int(sys.argv[1]))
    joysticks = Joystick.JoystickReader()

    print("Start web")
    thread.append(threading.Thread(target=lambda : app.run(host="0.0.0.0")))

    for thr in thread:
        thr.start()

    print("Start loop")
    start_time = time.time()
    loop_time  = time.time()
    while True:
        elapsed_time = time.time() - loop_time
        loop_time = time.time()
        
        start_time = time.time()
        sender.stateMachine()
        state_machine_time  = start_time - time.time()
        
        start_time = time.time()
        joysticks.worker()
        joysticks_time  = start_time - time.time()

        if sender.state == "work":
            i = 0
            # get id, ip, state и battery
            for data in sender.robotsData.values():
                robotList[i].robotData = data
                i += 1

            # get speed and kicker
            for i in range(len(joysticks.joysticks)):
                robotList[i].updData(joysticks.joysticks[i])

            # update data for udp sender
            for robot in robotList:
                if sender.robotsData.get(robot.robotData.robot_id) is not None:
                    sender.robotsData[robot.robotData.robot_id] = robot.robotData
        time.sleep(0.01)


if __name__ == '__main__':
    main()
