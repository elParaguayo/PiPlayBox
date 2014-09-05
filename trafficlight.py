import RPi.GPIO as GPIO
from time import sleep
import multiprocessing
from subprocess import call

class TrafficLight(object):

    def __init__(self, red, amber, green):

        self.process = None
        self.RED = 1
        self.AMBER = 2
        self.GREEN = 4
        self.binary = [self.RED, self.AMBER, self.GREEN]
        GPIO.setmode(GPIO.BOARD)
        self.red = red
        self.amber = amber
        self.green = green
        self.alllights = [red, amber, green]
        self.lookup = {self.RED: self.red,
                       self.AMBER: self.amber,
                       self.GREEN: self.green}
        for light in self.alllights:
            GPIO.setup(light, GPIO.OUT)
        self.allOff()

    def on(self, light):
        GPIO.output(light, GPIO.HIGH)

    def off(self, light):
        GPIO.output(light, GPIO.LOW)

    def allOff(self):
        for light in self.alllights:
            GPIO.output(light, GPIO.LOW)

    def binaryLight(self, combination):
        for light in self.binary:
            if combination & light:
                self.on(self.lookup[light])
            else:
                self.off(self.lookup[light])

    def sequence(self, seq):
        for phase in seq:
            self.binaryLight(phase[0])
            sleep(phase[1])


    def RedToGreen(self):
        self.allOff()
        self.on(self.red)
        sleep(5)
        self.off(self.red)
        for i in range(10):
            self.on(self.amber)
            sleep(0.5)
            self.off(self.amber)
            if i < 9:
                sleep(0.5)
        self.on(self.green)

    def stop(self):
        if self.process is not None:
            #self.process.terminate()
            call(["sudo", "kill", "-9", str(self.process.pid)])
            self.allOff()
            #self.process.join()

    def start(self, target=None, args=None):

        method = getattr(self, target)

        if args:
            self.process = multiprocessing.Process(target=method,
                                                   args=(args,))
        else:
            self.process = multiprocessing.Process(target=method)

        self.process.start()

