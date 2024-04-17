import pygame
import time

class Joyst:
    def __init__(self, joystic):
        self.move = [] 
        self.rotate = [] 
        self.kicker = 0
        self.joystick = joystic
        
    def addDevice(self, joystic):
        self.joystick = joystic
        
    def printValue(self):
        move = [self.joystick.get_axis(0), -self.joystick.get_axis(1)]
        rotate = [-(self.joystick.get_axis(2) + 1)/2,(self.joystick.get_axis(5) + 1)/2]
        kicker = self.joystick.get_button(0)

        if(move != self.move):
            self.move = move
            print(f"X  {self.move[0]:>6.3f}; Y {self.move[1]:>6.3f}")
            
        if(rotate != self.rotate):
            self.rotate = rotate
            print(f"Rotate {self.rotate[0]} {self.rotate[1]}")
            
        if(kicker != self.kicker):
            self.kicker = kicker
            print(f"Button {self.kicker}")

class JoysticReader:
    def __init__(self, joystic):
        self.joysticks = {}
        self.done = False
        pygame.init()


    def mainLoop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.JOYDEVICEADDED:
                    joy = Joyst(pygame.joystick.Joystick(event.device_index))
                    self.joysticks[joy.joystick.get_instance_id()] = joy
                    print(f"Joystick {joy.joystick.get_instance_id()} connencted")
                    
                if event.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")

            for joystick in self.joysticks.values():
                joystick.printValue()
            time.sleep(0.05)           

if __name__ == "__main__":
    # Если вы забудете эту строку, программа «зависнет»
    # при выходе, если работает из IDLE.
    pygame.quit()
