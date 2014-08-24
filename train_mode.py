import RPi.GPIO as GPIO
from basemode import BaseMode 

class PiPlayBoxMode(BaseMode):

    def __setup(self):
        self.modename = "Train Mode"
        self.subtext = "Let's play trains!!"
        self.display.Update(self.modename)

        self.addInterrupts()

    def addInterrupts(self):

        e = GPIO.add_event_detect

        e(self.buttons[0], )
        e(self.buttons[1], )
        e(self.buttons[2], )
        e(self.buttons[3], )
        e(self.buttons[4], )
        e(self.buttons[5], )
        e(self.buttons[6], )
        e(self.buttons[7], )