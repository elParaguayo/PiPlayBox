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

        self.modecolour = self.display.VIOLET

        self.actions = {0: {"text": "Mariposita esta\nen la cocina",
                            "sound": "mariposita.ogg"},
                        1: {"text": "Mariana\ncuenta uno",
                            "sound": "mariana.ogg"},
                        2: {"text": "Cucaracha\ntu que tienese",
                            "sound": "cucaracha.ogg"},
                        3: {"text": "La aranita subio\nsubio subio",
                            "sound": "aranita.ogg"},
                        4: {"text": "Sol solecito\nLuna lunera",
                            "sound": "solsolecito.ogg"},
                        5: {"text": "El sapo no\nse lava el pie",
                            "sound": "elsapo.ogg"},
                        6: {"text": "Mi pollito\namarillito",
                            "sound": "pollito.ogg"},
                        7: {"text": "Vamos Pocoyo\nes un carrera",
                            "sound": "carrera.ogg"}}
        self.modename = "Cantamos"
        self.subtext = "en Espanol!"
        self.musicdir = os.path.join(self.plugindir, "music")
        self.display.backlight(self.modecolour)
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
        print "%s pressed" % button
        action = self.actions[button]

        self.display.Update(action["text"])
        self.playMusic(self.soundFile(action["sound"]))
        self.colourthread = threading.Thread(target=self.Disco)
        self.colourthread.start()

    def event(self, event):
        self.Mute()

