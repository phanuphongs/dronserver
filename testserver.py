import socketio
import json
import eventlet
import atexit 
import time
##import pigpio



class PWMSoftware(object):
    def __init__(self):
        self.throttle = 0
        self.yaw = 0
        self.roll = 0
        self.pitch = 0
        ##pi = pigpio.pi() # Connect to local Pi
        ##
        ##pi.set_mode(14, pigpio.OUTPUT)
        ##pi.set_servo_pulsewidth(15, 0)
        ##
        ##pi.set_mode(15, pigpio.OUTPUT)
        ##pi.set_servo_pulsewidth(18, 1500)
        ##
        ##pi.set_mode(17, pigpio.OUTPUT)
        ##pi.set_servo_pulsewidth(17, 1500)
        ##
        ##pi.set_mode(18, pigpio.OUTPUT)
        ##pi.set_servo_pulsewidth(18, 1500)
      
        
    def convertData(self, command, speed, angle):
        if command == 'up' or command == 'down':
            self.throttle = round(1500 + ((speed*1000/2)))
            self.yaw = 0
            self.roll = 0
            self.pitch = 0
        
        elif command == 'left' or command == 'right':
            self.throttle = round(1500 + ((speed*1000/2)))
            self.yaw = 0
            self.roll = round(1500 + ((angle*1000)))
            self.pitch = 0

        elif command == 'forward' or command == 'backward':
            self.throttle = round(1500 + ((speed*1000/2)))
            self.yaw = 0
            self.roll = 0
            self.pitch = round(1500 + ((angle*1000)))

        elif command == 'turnleft' or command == 'turnright':
            self.throttle = round(1500 + ((speed*1000/2)))
            self.yaw = round(1500 + ((angle*1000)))
            self.roll = 0
            self.pitch = 0

    def sendData(self):
        pi.set_servo_pulsewidth(14, self.throttle)
        pi.set_servo_pulsewidth(15, self.roll)
        pi.set_servo_pulsewidth(17, self.pitch)
        pi.set_servo_pulsewidth(18, self.yaw)
        
    def printData(self):
        print(self.throttle)
        print(self.roll)
        print(self.pitch)
        print(self.yaw)
        print("")

sio = socketio.Server(async_mode='eventlet')
pwm = PWMSoftware()

@sio.on('send data')
def message(sid, data):
    print(data)
    data1 = json.loads(data)
    pwm.convertData(data1['command'],data1['speed'],data1['angle'])
##    pwm.printData()
    

app = socketio.Middleware(sio)
eventlet.wsgi.server(eventlet.listen(('localhost', 8000)),app)
