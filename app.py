import socket
import random
import time
from flask import Flask, render_template, request
from flask import jsonify
import threading

app = Flask(__name__)

class Robot:
    robotIndex = '_1'
    def __init__(self, index):
        self.robotIndex = index
        self.status = 1
        self.robot_id = 1
        self.robot_ip = 1
        self.first_motor_speed = 1
        self.second_motor_speed = 1
        self.third_motor_speed = 1
        self.kicker = 1
        self.battery = 1


    def updParam(self):
        self.robot_id = random.randint(0, 100)
        self.robot_ip = random.randint(0, 100)
        self.first_motor_speed = random.randint(0, 100)
        self.second_motor_speed = random.randint(0, 100)
        self.third_motor_speed = random.randint(0, 100)
        self.kicker = random.randint(0, 100)
        self.battery = random.randint(0, 100)
        self.status = random.randint(0,1)
        if self.status == 1:
            self.status = "Connected"
        else:
            self.status = "Offline"
            
    def generateJson(self):
        file = jsonify({
            'robot_ip_address': self.robot_ip,
            'robot_id': self.robot_id,
            'first_motor_speed': self.first_motor_speed,
            'second_motor_speed': self.second_motor_speed,
            'third_motor_speed': self.third_motor_speed,
            'kicker_status': self.kicker,
            'battery_life': self.battery,
            'status': self.status   
        })
        return file
    
    
robotList = [Robot('_' + str(i)) for i in range(5)]



@app.route('/')
def index():
    return render_template('homePage.html')


@app.route('/get_parameters_0', methods=['GET'])
def get_parameters_0():
    return robotList[0].generateJson()


@app.route('/get_parameters_1', methods=['GET'])
def get_parameters_1():
    return robotList[2].generateJson()


@app.route('/get_parameters_2', methods=['GET'])
def get_parameters_2():
    return robotList[2].generateJson()


@app.route('/get_parameters_3', methods=['GET'])
def get_parameters_3():
    return robotList[3].generateJson()


@app.route('/get_parameters_4', methods=['GET'])
def get_parameters_4():
    return robotList[4].generateJson()


def main(args=None):
    threading.Thread(target=app.run(host='0.0.0.0', port=5000 ,debug=True)).start()



if __name__ == '__main__':
    main()