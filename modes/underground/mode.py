import RPi.GPIO as GPIO
from basemode import BaseMode 
from time import sleep
import os
from random import choice, randint
import threading

class PiPlayBoxMode(BaseMode):

    def setup(self):
        self.SOUND = 1
        self.LCD = 2
        self.LCDCOLOUR = 4
        self.TRAFFICLIGHT = 8

        self.modecolour = self.display.BLUE

        self.actions = {0: {"text": "Next station:\nMorden!",
                            "sound": "morden.ogg"},
                        1: {"text": "Please mind the\nclosing doors",
                            "sound": "doors.ogg"},
                        2: {"text": None,
                            "sound": None},
                        3: {"text": None,
                            "sound": None},
                        4: {"text": None,
                            "sound": None},
                        5: {"text": None,
                            "sound": None},
                        6: {"text": None,
                            "sound": None},
                        7: {"text": None,
                            "sound": None}}
        self.modename = "London"
        self.subtext = "Underground"
        self.musicdir = os.path.join(self.plugindir, "sounds")
        self.display.changeColour(self.modecolour)
        self.display.Update("%s\n%s" % (self.modename,
                                        self.subtext))
        self.addInterrupts()

    def addInterrupts(self):

        e = GPIO.add_event_detect
        for i in range(8):
            e(self.buttons[i], 
              GPIO.RISING, 
              lambda channel, x=i: self.buttonAction(x),
              bouncetime=600)

    def soundFile(self, sound):
        return os.path.join(self.musicdir, sound)

    def buttonAction(self, button):
        action = self.actions[button]
        if action["text"] is not None:

            self.display.Update(action["text"])
            self.playMusic(self.soundFile(action["sound"]))
            



