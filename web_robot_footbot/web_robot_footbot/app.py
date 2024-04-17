import rclpy
from rclpy.node import Node
from robot_msg.msg import Robotdata
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

import socket
import random
import time
from flask import Flask, render_template, request
from flask import jsonify
import threading

app = Flask(__name__, template_folder="/home/dima/ros2_ws/src/web_robot_footbot/web_robot_footbot/templates", 
            static_folder='/home/dima/ros2_ws/src/web_robot_footbot/web_robot_footbot/static')

class Robot:
    robotIndex = '_1'
    myData = Robotdata
    
    def __init__(self, index):
        self.robotIndex = index
        self.myData.status = 1
        self.myData.robot_id = 1
        self.myData.robot_ip = 1
        self.myData.first_motor_speed = 1
        self.myData.second_motor_speed = 1
        self.myData.third_motor_speed = 1
        self.myData.kicker = 1
        self.myData.battery = 1


    def updParam(self):
        self.myData.robot_id = random.randint(0, 100)
        self.myData.robot_ip = random.randint(0, 100)
        self.myData.first_motor_speed = random.randint(0, 100)
        self.myData.second_motor_speed = random.randint(0, 100)
        self.myData.third_motor_speed = random.randint(0, 100)
        self.myData.kicker = random.randint(0, 100)
        self.myData.battery = random.randint(0, 100)
        self.myData.status = random.randint(0,1)
        if self.myData.status == 1:
            self.status = "Connected"
        else:
            self.status = "Offline"
            
    def generateJson(self):
        file = jsonify({
            'robot_ip_address': self.myData.robot_ip,
            'robot_id': self.myData.robot_id,
            'first_motor_speed': self.myData.first_motor_speed,
            'second_motor_speed': self.myData.second_motor_speed,
            'third_motor_speed': self.myData.third_motor_speed,
            'kicker_status': self.myData.kicker,
            'battery_life': self.myData.battery,
            'status': self.myData.status   
        })
        return file
    
    
robotList = [Robot('_' + str(i)) for i in range(5)]


class MinimalSubscriber(Node, ):
    def __init__(self):
        super().__init__('minimal_subscriber')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1
        )
        self.publisher_ = self.create_subscription(Robotdata, 'topic', 10,qos_profile=qos_profile)

    def listener_callback(self, msg):
        robotList[msg.robot_id].myData = msg
        self.get_logger().info('I heard: "%d"' % msg.robot_id)

def ros2_thread(node):
    print('entering ros2 thread')
    rclpy.spin(node)
    print('leaving ros2 thread')


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
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    threading.Thread(target=ros2_thread, args=[minimal_subscriber]).start()
    threading.Thread(target=app.run(host='0.0.0.0', port=5000 ,debug=True)).start()
    
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()