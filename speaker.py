import RPi.GPIO as GPIO

class Speaker(object):

    def __init__(self, pin):

        self.__speakerpin = pin
        self.locked = False
        self.Mute()

    def Mute(self):

        GPIO.output(self.__speakerpin, GPIO.LOW)
        self.muted = True

    def Unmute(self):

        if not self.locked:
            GPIO.output(self.__speakerpin, GPIO.HIGH)
            self.muted = False

    def Toggle(self):

        if self.muted:
            self.Unmute()
        else:
            self.Mute()

    def Lock(self):

        self.locked = True

    def Unlock(self):

        self.locked = False