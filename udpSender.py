import socket
import struct
import time
import threading


class UDPConvers:
    state = "idle"
    localPort = 5005
    broadCastPort = 5006
    robot_ips = []
    robotsData = []
    msg4 = struct.pack('!B', 3)
    msg1 = struct.pack('!B', 1)

    def __init__(self):

        self.localSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.localSock.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.localSock.bind(('', self.localPort))

        self.broadCastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadCastSock.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadCastSock.bind(("0.0.0.0", self.broadCastPort))

    def stopSession(self):
        print("Stop session")
        self.state = "Stop"

    def startSession(self):
        print("Start session")
        self.state = "init"

    def init(self):
        print("Start init")
        self.broadCastSock.sendto(
            self.msg1, ('<broadcast>', self.broadCastPort))
        start_time = time.time()
        self.broadCastSock.settimeout(1.0)
        responses = 0

        while responses < 5 and time.time() - start_time < 5:
            try:
                data, addr = self.broadCastSock.recvfrom(1024)
                if (data[0] == 2):
                    print(
                        f"Received valid response from {addr} and address of robot - {data[1]}")
                    responses += 1
                    recMsg = Robotdata
                    recMsg.robot_id = data[1]
                    recMsg.robot_ip = addr
                    self.robotsData.append(recMsg)
                    # self.robot_ips.append(addr)
                    break
            except socket.timeout:
                print("Error in receive")

        if (responses != 0):
            self.state = "work"
        time.sleep(5)

    def work(self):
        start_time = time.time()
        self.localSock.settimeout(1.0)  # set timeout to 1 second

        while True:

            for data in self.robotsData:
                msg = struct.pack('!BBBB', data.first_motor_speed,
                                  data.second_motor_speed, data.third_motor_speed, data.kicker)
                self.localSock.sendto(msg, (data.robot_ip, self.localPort))

            time.sleep(0.05)  # wait for 10 milliseconds

            if time.time() - start_time >= 5:
                for robot in self.robotsData:
                    self.localSock.sendto(
                        self.msg4, (robot.robot_ip, self.localPort))
                    try:
                        data, addr = self.localSock.recvfrom(1024)
                        if (data[0] == 2):
                            print(
                                f"Received valid response from {addr} and address of robot - {data[1]}")
                            robot.battery = data[2]
                    except socket.timeout:
                        print("Error in receive")
                        self.startSession()
                start_time = time.time()

    def stateMachine(self):
        start_time = time.time()

        while (1):
            match self.state:
                case "idle":
                    self.startSession()
                case "init":
                    self.init()
                case "work":
                    self.work()

            if time.time() - start_time >= 20:
                print(self.state)

            time.sleep(0.01)


def main(args=None):
    udpConvers = UDPConvers()
    threading.Thread(target=udpConvers.stateMachine).start()


if __name__ == '__main__':
    main()
