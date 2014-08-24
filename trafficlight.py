import RPi.GPIO as GPIO
from time import sleep

class TrafficLight(object):

    def __init__(self, red, amber, green):
        GPIO.setmode(GPIO.BOARD)
        self.red = red
        self.amber = amber
        self.green = green
        self.alllights = [red, amber, green]
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

