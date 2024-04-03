import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import random
import time
from flask import Flask, render_template, request
from flask import jsonify
import threading

app = Flask(__name__, template_folder="/home/dima/ros2_ws/src/web_robot_footbot/web_robot_footbot/templates", 
            static_folder='/home/dima/ros2_ws/src/web_robot_footbot/web_robot_footbot/static')

class Robot:
    robotIndex = '_1'
    robot_ip_address = 192
    robot_id = 12345
    first_motor_speed = 0
    second_motor_speed = 0
    third_motor_speed = 0
    kicker_status = 0
    battery_life = 10

    def __init__(self, index):
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


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 2 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

robotList = [Robot('_' + str(i)) for i in range(5)]

def ros2_thread(node):
    print('entering ros2 thread')
    rclpy.spin(node)
    print('leaving ros2 thread')

def updData():
    while True:
        for robot in robotList:
            robot.updParam()
        time.sleep(1)

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

    minimal_publisher = MinimalPublisher()
    threading.Thread(target=updData).start()
    threading.Thread(target=ros2_thread, args=[minimal_publisher]).start()
    threading.Thread(target=app.run(host='0.0.0.0', port=5000 ,debug=True)).start()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()