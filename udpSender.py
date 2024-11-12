import copy
import socket
import struct
import time
import threading
from Robot import RobotData


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class UDPConvers(metaclass=SingletonMeta):
    state = "idle"
    localPort = 5005
    broadCastPort = 5006
    start_time = time.time()

    msg4 = struct.pack('!B', 3)
    msg1 = struct.pack('!B', 1)

    robotsData = dict()
    prev_robots_data = dict()

    def __init__(self,id):
        print("Construct class")
        self.localSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.localSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.localSock.bind(("255.255.255.255", self.localPort)) # 0.0.0.0
        if(id == 1 or id == 0):
            self.msg1 = struct.pack('!B', id)
        else:
            print("error in adress")

    def stopSession(self):
        print("Stop session")
        self.state = "Stop"

    def startSession(self):
        print("Start session")
        self.state = "init"

    def init(self):
        print("Start init")
        start_time = time.time()
        responses = 0
        self.localSock.sendto(self.msg1, ('<broadcast>', self.localPort))
        self.localSock.settimeout(1.0)

        while responses < 2: #and time.time() - start_time < 10:
            try:
                data, addr = self.localSock.recvfrom(1024)
                if data[0] == 2:
                    if not (data[1] in self.robotsData):
                        print(f"Received valid response from {addr} and address of robot - {data[1]}")
                        responses += 1
                        _robotData = RobotData()
                        _robotData.status = 1
                        _robotData.robot_id = data[1]
                        _robotData.robot_ip = addr[0]
                        self.robotsData[data[1]] = copy.deepcopy(_robotData)

            except socket.timeout:
                self.localSock.sendto(self.msg1, ('<broadcast>', self.localPort))
                self.localSock.settimeout(2.0)
                print("Error in receive")


        self.prev_robots_data = copy.deepcopy(self.robotsData)
        if responses != 0:
            self.state = "work"

    def work(self):
        # self.start_time = time.time()
        self.localSock.settimeout(1.0)  # set timeout to 1 second

        for key, data in self.robotsData.items():
            if data != self.prev_robots_data[key]:
                print(f"send msg1 to {data.robot_ip}")
                try:
                    msg = struct.pack('!bbbB', data.first_motor_speed, data.second_motor_speed, data.third_motor_speed,
                                  data.kicker)
                    self.localSock.sendto(msg, (data.robot_ip, self.localPort))
                except Exception:
                    print(f"Error in send data for {data.robot_ip}")
                    pass

        if time.time() - self.start_time >= 5:
            for key, robot in self.robotsData.items():
                if robot != self.prev_robots_data[key]:
                    self.localSock.sendto(self.msg4, (robot.robot_ip, self.localPort))
                    try:
                        data, addr = self.localSock.recvfrom(1024)
                        if data[0] == 2:
                            print(f"Received valid response from {addr} and address of robot - {data[1]}")
                            robot.battery = data[2]
                        self.start_time = time.time()
                    except socket.timeout:
                        print("Error in receive")
                        self.startSession()

        self.prev_robots_data = copy.deepcopy(self.robotsData)
    def stateMachine(self):
        # time.sleep(1)

        match self.state:
            case "idle":
                self.startSession()
            case "init":
                self.init()
            case "work":
                self.work()

        if time.time() - self.start_time >= 20:
            print(self.state)
            self.start_time = time.time()

            # time.sleep(0.01)
