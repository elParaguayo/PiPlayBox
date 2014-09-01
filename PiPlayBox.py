#!/usr/bin/env python
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

'''
    This script uses the following GPIO pins:

    3,5: I2C (controls LED display)
    7,11,12,13,15,16,18,19: inputs (buttons)
    21: speaker mute
    22, 23, 24: outputs (LED trafficlight)
    26: unallocated
'''

from time import sleep
import threading
import os 
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import imp
from subprocess import call

import pygame
import RPi.GPIO as GPIO

from speaker import Speaker
#from trafficlight import TrafficLight 
from display import Display

# PiPlayBox modes
from modes.train_mode.mode import PiPlayBoxMode as TrainMode
from modes.canciones_espanoles.mode import PiPlayBoxMode as SpanishSongs
from modes.tunes.mode import PiPlayBoxMode as Tunes
from modes.radio.mode import PiPlayBoxMode as Radio
from modes.underground.mode import PiPlayBoxMode as Underground

my_modes = {1: TrainMode,
            2: SpanishSongs,
            3: Tunes,
            4: Radio,
            5: Underground}

class PiPlayBox(object):

    def __init__(self):

        self.display = Display()
        self.quit = False
        self.stopped = False
        self.mode = None

        # Time in seconds until screen turns off if no activity
        self.screentimeout = 30

        # Time in seconds until box turns off if no activity
        self.powertimeout = 300

        self.display.Update("Setting up\nbuttons...")

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(26, GPIO.IN)
        GPIO.setup(24, GPIO.IN)

        self.__speakerpin = 21

        self.__button1 = 7
        self.__button2 = 11
        self.__button3 = 12
        self.__button4 = 13
        self.__button5 = 15
        self.__button6 = 16
        self.__button7 = 18
        self.__button8 = 19       

        self.__redpin = 22
        self.__yellowpin = 23
        self.__greenpin = 24

        self.__unallocatedpins = [26]

        self.GPIOpins = {"buttons": [self.__button1,
                                     self.__button2,
                                     self.__button3,
                                     self.__button4,
                                     self.__button5,
                                     self.__button6,
                                     self.__button7,
                                     self.__button8],
                         "speaker":  self.__speakerpin,
                         "leds":    [self.__redpin,
                                     self.__yellowpin,
                                     self.__greenpin],
                         "unused":   self.__unallocatedpins}
        for button in self.GPIOpins["buttons"]:
            GPIO.setup(button, GPIO.IN)

        for button in (self.GPIOpins["leds"] + [self.__speakerpin]):
            GPIO.setup(button, GPIO.OUT)

        self.speaker = Speaker(self.__speakerpin)

        self.display.Update("Initialising\nsystem...")

        pygame.init()
        pygame.display.set_mode((1,1))
        pygame.mixer.init(frequency=22050, channels=1, buffer=1024) 
        
        #self.trafficlight = TrafficLight(self.__redpin,
        #                                 self.__yellowpin,
        #                                 self.__greenpin)
        #self.automute = True
        #self.startAutoMute()

        self.display.Update("Looking for\nplugins...")
        self.modes = self.__getModes()
        #train = self.__loadMode(self.modes[0])
        self.switchMode(1)

        self.override_thread = threading.Thread(target=self.__override_monitor)
        self.override_thread.start()

        self.powersave_thread = threading.Thread(target=self.__power_save)
        self.powersave_thread.start()

    def playNext(self, channel):
        self.play(self.ratherbe)

    def clearInterrupts(self):
        for pin in self.GPIOpins["buttons"]:
            GPIO.remove_event_detect(pin)

    def switchMode(self, mode):
        if self.mode is not None:
            self.mode.quit()
        self.clearInterrupts()
        pygame.mixer.music.stop()
        self.speaker.Mute()
        self.display.Update("Changing\nmode")
        self.display.changeColour(self.display.WHITE)
        sleep(2)
        if not my_modes.get(mode, None) is None:
           self.mode = my_modes[mode](display=self.display,
                                      buttons=self.GPIOpins["buttons"],
                                      speaker=self.speaker,
                                      mixer=pygame.mixer)

    def __getModes(self):

        PluginFolder = "./modes"
        PluginScript = "mode.py"
        MainModule = "mode"
        plugins = []
        possibleplugins = os.listdir(PluginFolder)
        a=1
        for i in possibleplugins:
            location = os.path.join(PluginFolder,i)
            if not os.path.isdir(location) or not (PluginScript in 
                                                   os.listdir(location)):
                continue
            inf = imp.find_module(MainModule, [location])
            plugins.append({"name": i, "info": inf, "id": a})
            a=a+1
        return plugins

    def __loadMode(self, plugin):
        return imp.load_module("mode", *plugin["info"])        

    def __auto_mute(self):

        while (pygame.mixer.get_init() and self.automute):

            if pygame.mixer.get_busy():
                self.speaker.Unmute()
            else:
                self.speaker.Mute()

            sleep(10)

    def __power_save(self):
        a = 0
        while not self.quit:
            if (pygame.mixer.get_init() and pygame.mixer.music.get_busy()):
                a = 0
                self.display.On()
            else:
                a += 1

            if a == (self.screentimeout * 10):
                self.display.Off()
            #elif a == (self.powertimeout * 10):
            #    self.quit = True

            sleep(0.1)


    def __override_monitor(self):
        '''Thread to work in backgroun. Should be used to handle long-press
        events e.g. to trigger shutdown of device.'''
        stopcount = settingcount = 0
        a = b = c = d = e = f = g = h = 0
        self.poweroff = False
        self.restart = False

        while not self.quit:
            if GPIO.input(self.__button1) and GPIO.input(self.__button2):
                stopcount = stopcount + 1
            elif GPIO.input(self.__button7) and GPIO.input(self.__button8):
                settingcount += 1
            elif GPIO.input(self.__button1):
                a += 1
            elif GPIO.input(self.__button2):
                b += 1
            elif GPIO.input(self.__button3):
                c += 1
            elif self.singlePin(self.__button4):
                d += 1
            elif self.singlePin(self.__button5):
                e += 1
            elif (self.restart or self.poweroff) and not self.inputList(self.GPIOpins["buttons"]):
                self.quit = True
            else:
                stopcount = settingcount = 0
                a = b = c = d = e = f = g = h = 0
            
            if stopcount == 10:
                self.display.Update("Stopped")
                self.speaker.Lock()
                self.speaker.Mute()
                self.stopped = True
            elif settingcount == 20:
                self.display.Update("Restart")
                self.restart = True
            elif settingcount == 40:
                self.display.Update("Power off")
                self.restart = False
                self.poweroff = True
            elif a == 20:
                self.switchMode(1)
            elif b == 20:
                self.switchMode(2)
            elif c == 20:
                self.switchMode(3)
            elif d == 20:
                self.switchMode(4)
            elif e == 20:
                self.switchMode(5)
            sleep(0.1)

    def inputList(self, pins):
        '''Returns True if any pin in the list is high.'''
        for pin in pins:
            if GPIO.input(pin):
                return True

        return False

    def singlePin(self, target):
        pinlist = list(self.GPIOpins["buttons"])
        pinlist.remove(target)
        return GPIO.input(target) and not self.inputList(pinlist)

    def startAutoMute(self):
        
        self.mutethread = threading.Thread(target=self.__auto_mute)
        self.mutethread.start()

    def play(self, file):
        self.music.stop()
        self.music.load(file)
        self.music.play()

    def start(self):

        while not self.quit:
            try:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.quit=True

                    if event >= pygame.USEREVENT:
                        self.mode.event(event)

                if self.stopped:
                    #pygame.mixer.music.stop()
                    sleep(2)
                    pygame.mixer.music.stop()
                    self.speaker.Mute()
                    self.speaker.Unlock()
                    self.stopped = False

            except KeyboardInterrupt:
                self.quit = True
                
        pygame.mixer.stop()
        pygame.mixer.quit()
        sleep(0.5)
        GPIO.cleanup()
        self.display.clear()
        self.display.Off()

        if self.restart:
            call("/sbin/reboot")

        elif self.poweroff:
            call("/sbin/poweroff")
  
        # while True:
        #     sleep(1)

a = PiPlayBox()
a.start()
