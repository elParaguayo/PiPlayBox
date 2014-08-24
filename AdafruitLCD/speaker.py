import RPi.GPIO as GPIO

class Speaker(object):

    def __init__(self, speakerpin):

        self.__speaker = speakerpin
        self.Unmute()

    def Mute(self):

        GPIO.__speaker(self.__speaker, GPIO.LOW)
        self.__state = False

    def Unmute(self):

        GPIO.__speaker(self.__speaker, GPIO.HIGH)
        self.__state = True

    def Toggle(self):

        if self.__state:
            self.Mute()
            
        else:
            self.Unmute()
