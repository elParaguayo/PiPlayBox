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

        self.modecolour = self.display.YELLOW

        self.actions = {0: {"text": "All the ducks\nare swimming",
                            "sound": "ducks.ogg"},
                        1: {"text": "Feel the love",
                            "sound": "feelthelove.ogg"},
                        2: {"text": "And the trumpets\nthey go...",
                            "sound": "trumpets.ogg"},
                        3: {"text": "No no no no no\nRather be",
                            "sound": "rather.ogg"},
                        4: {"text": "Only wanna make\nthings right",
                            "sound": "makeright.ogg"},
                        5: {"text": "I wanna stay\nwith you",
                            "sound": "staywithyou.ogg"},
                        6: {"text": None,
                            "sound": None},
                        7: {"text": None,
                            "sound": None}}
        self.modename = "Wait... wait..."
        self.subtext = "and DANCE!!"
        self.musicdir = os.path.join(self.plugindir, "music")
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
            self.colourthread = threading.Thread(target=self.Disco)
            self.colourthread.start()



