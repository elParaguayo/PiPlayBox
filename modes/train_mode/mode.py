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

        self.modecolour = self.display.GREEN

        self.actions = {0: {"action": self.SOUND + self.LCD,
                            "text": "Chugga chugga\nchoo choo!",
                            "sound": "toot.ogg"},
                        1: {"action": self.SOUND + self.LCD,
                            "text": "Thomas and\nFriends",
                            "sound": "thom.ogg"},
                        2: {"action": self.SOUND + self.LCD,
                            "text": "Next station:\nQueenstown Road",
                            "sound": "qrb.ogg"},
                        3: {"action": self.SOUND + self.LCD,
                            "text": "Next station:\nClapham Junction",
                            "sound": "clj.ogg"},
                        4: {"action": self.SOUND + self.LCD,
                            "text": "Next station:\nVauxhall",
                            "sound": "vxh.ogg"},
                        5: {"action": self.SOUND + self.LCD,
                            "text": "Train not\nstopping!",
                            "sound": "not_stop.ogg"},                                                        
                        6: {"action": self.SOUND + self.LCD,
                            "text": "Train for:\nWaterloo",
                            "sound": "vau.ogg"},
                        7: {"action": None,
                            "text": "Button 8"}} 
        self.modename = "Train Mode"
        self.subtext = "Choo choo!!"
        self.musicdir = os.path.join(self.plugindir, "music")
        self.display.changeColour(self.modecolour)
        self.display.Update("%s\n%s" % (self.modename,
                                        self.subtext))
        self.thomas = os.path.join(self.musicdir, "thom.ogg")
        self.ratherbe = os.path.join(self.musicdir, "rather.ogg")
        self.nextqrb = os.path.join(self.musicdir, "qrb.ogg")
        #self.playMusic(self.thomas)
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

        if action["action"] is not None:

            if self.LCD & action["action"]:
                self.display.Update(action["text"])

            if self.SOUND & action["action"]:
                self.playMusic(self.soundFile(action["sound"]))

            if self.LCDCOLOUR & action["action"]:
                self.colourthread = threading.Thread(target=action["colour"])
                self.colourthread.start()




