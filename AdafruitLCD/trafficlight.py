import RPi.GPIO as GPIO

class TrafficLight(object):

	def __init__(self, redlight, yellowlight, greenlight):

		self.__RED = redlight
		self.__YELLOW = yellowlight
		self.__GREEN = greenlight

		self.lights = [self.__RED,
		               self.__YELLOW,
		               self.__GREEN]

	def state(self, on):

		return GPIO.HIGH if on else GPIO.LOW

	def GREEN(self, on=True):

		GPIO.output(self.__GREEN, state(on))

	def RED(self, on=True):

		GPIO.output(self.__RED, state(on))

	def YELLOW(self, on=True):

		GPIO.output(self.__YELLOW, state(on))

	def AllOn(self):

		for light in self.lights:
			GPIO.output(light, GPIO.HIGH)

	def AllOff(self):

		for light in self.lights:
			GPIO.output(light, GPIO.LOW)

