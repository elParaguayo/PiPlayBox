import RPi.GPIO as GPIO
from basemode import BaseMode 
from time import sleep
import os
from random import choice, randint
import threading
import multiprocessing

class PiPlayBoxMode(BaseMode):

    def setup(self):
        self.SOUND = 1
        self.LCD = 2
        self.LCDCOLOUR = 4
        self.TRAFFICLIGHT = 8

        self.modecolour = self.display.YELLOW

        self.actions = {0: {"text": "Wait for the\ngreen man",
                            "method": "RedToGreen"},
                        1: {"text": "Red light\nmeans stop",
                            "method": "binaryLight",
                            "args": 1},
                        2: {"text": "Yellow light\nmeans wait",
                            "method": "binaryLight",
                            "args": 2},
                        3: {"text": "Green light\nmeans go",
                            "method": "binaryLight",
                            "args": 4},
                        4: {"text": None,
                            "method": None},
                        5: {"text": None,
                            "method": None},
                        6: {"text": None,
                            "method": None},
                        7: {"text": None,
                            "method": None}}
        self.modename = "Traffic Lights"
        self.subtext = "Green means go!"
        self.musicdir = os.path.join(self.plugindir, "music")
        self.display.changeColour(self.modecolour)
        self.display.Update("%s\n%s" % (self.modename,
                                        self.subtext))
        self.pattern = None
        self.addInterrupts()

    def addInterrupts(self):

        e = GPIO.add_event_detect
        for i in range(8):
            e(self.buttons[i], 
              GPIO.RISING, 
              lambda channel, x=i: self.buttonAction(x),
              bouncetime=600)

    def buttonAction(self, button):

        self.trafficlight.stop()
        action = self.actions[button]
        if action["text"] is not None:
            args = action.get("args", None)
            self.trafficlight.start(target=action["method"], args=args)
            self.display.Update(action["text"])

    def quit(self):
        self.trafficlight.stop()




