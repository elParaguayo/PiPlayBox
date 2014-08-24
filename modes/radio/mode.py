import RPi.GPIO as GPIO
from basemode import BaseMode 
from time import sleep
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import threading
from subprocess import check_call, CalledProcessError

from mplayer import Player

class PiPlayBoxMode(BaseMode):

    def setup(self):
        self.modecolour = self.display.RED
        self.display.changeColour(self.modecolour)
        self.enabled = self.__ping()
        self.mplayer = None

        if self.enabled:

            self.actions = {0: {"text": "Capital FM",
                                "sound": "http://ice-sov.musicradio.com:80/CapitalMP3"},
                            1: {"text": None,
                                "sound": None},
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
            self.addInterrupts()                    
            self.modename = "Internet Radio"
            self.subtext = "ONLINE"
            self.mplayer = Player()

        else:

            self.modename = "No Internet"
            self.subtext = "Connection"


        self.display.Update("%s\n%s" % (self.modename,
                                        self.subtext))


    def __ping(self):
        self.display.Update("Checking if\nonline...")
        try:
            a = check_call(["/bin/ping", "www.bbc.co.uk", "-c", "1", "-t", "200"])
            return True 
        except CalledProcessError:
            return False


    def addInterrupts(self):

        e = GPIO.add_event_detect
        for i in range(8):
            e(self.buttons[i], 
              GPIO.RISING, 
              lambda channel, x=i: self.buttonAction(x),
              bouncetime=600)

    def buttonAction(self, button):
        action = self.actions[button]
        if action["text"] is not None:

            self.display.Update(action["text"])
            self.mplayer.stop()
            self.speaker.Unmute()
            self.mplayer.loadfile(action["sound"])

    def quit(self):
        if self.mplayer is not None and self.mplayer.is_alive():
            self.mplayer.stop()
            self.mplayer.quit()
            self.speaker.Mute()
            self.mplayer = None



