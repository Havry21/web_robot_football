import random
import time
from flask import Flask, render_template, request
from flask import jsonify
import threading

app = Flask(__name__)

class Robot:
    robotIndex = '_1'
    robot_ip_address = 192
    robot_id = 12345
    first_motor_speed = 0
    second_motor_speed = 0
    third_motor_speed = 0
    kicker_status = 0
    battery_life = 10
    
    def __init__(self,index):
        self.robotIndex = index
    
    def updParam(self):
        self.robot_ip_address = random.randint(0, 100)
        self.robot_id = random.randint(0, 100)
        self.first_motor_speed = random.randint(0, 100)
        self.second_motor_speed = random.randint(0, 100)
        self.third_motor_speed = random.randint(0, 100)
        self.kicker_status = random.randint(0, 100)
        self.battery_life = random.randint(0, 100)
        
    def generateJson(self):
        file = jsonify({
            'robot_ip_address': self.robot_ip_address,
            'robot_id': self.robot_id,
            'first_motor_speed': self.first_motor_speed,
            'second_motor_speed': self.second_motor_speed,
            'third_motor_speed': self.third_motor_speed,
            'kicker_status': self.kicker_status,
            'battery_life': self.battery_life
        })
        return file
        
robotList = [Robot('_' + str(i)) for i in range(5)]

def updData():
    while True:
        for robot in robotList:
            robot.updParam()
        time.sleep(1)
        
@app.route('/')
def index():
    return render_template('index.html')
    
    
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


if __name__ == '__main__':
    battery_thread = threading.Thread(target=updData)
    battery_thread.start()
    app.run()

    