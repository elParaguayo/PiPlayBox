from subprocess import call
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from time import sleep
from random import choice, randint

import pygame

import RPi.GPIO as GPIO

class BaseMode(object):
    """Base class for plugins. Sets out key methods available to plugins."""

    def __init__(self, buttons=None, 
                       display=None, 
                       speaker=None, 
                       trafficlight=None,
                       mixer=None):
        """Initialises base class. Should not be overriden by plugins."""

        self.display = display
        self.buttons = buttons
        self.speaker = speaker
        self.trafficlight = trafficlight
        self.mixer = mixer

        self.mixer.music.set_endevent()
        self.mixer.music.set_endevent(pygame.USEREVENT)

        #self.clearEvents()

        self.modename = "Default Mode"
        self.subtext = "To be overriden"

        self.plugindir = os.path.dirname(sys.modules[self.__class__.__module__].__file__)

        self.music = None
        self.sound = None

        # Call setup function
        self.setup()

    def clearEvents(self):

        for button in self.buttons:
            GPIO.remove_event_detect(button)

    def setup(self):
        """Specific plugin setup functions can be implemented by overriding
        this method.
        """

        pass

    def Welcome(self):
        """Display a message to show the mode has been selected."""
        self.setDisplayText("** NEW MODE **",
                            "** NEW MODE **")

    def setDisplayColour(self, colour):
        
        raise NotImplementedError


    def setDisplayText(self, topline, bottomline, colour=None):

        if colour:
            setDisplayColour(colour)

        self.display.message("%s\n%s" % (topline,
                                         bottomline))

    def __auto_mute(self):

        if pygame.mixer.get_busy:
            self.Unmute()
        
        else:
            Mute()

    def playSound(self, mixerobject):

        if self.sound:
            self.sound.stop()

        self.sound = mixerobject
        self.Unmute()
        self.sound.play()

    def Mute(self):

        if self.speaker:
            self.speaker.Mute()

    def Unmute(self):

        if self.speaker:
            self.speaker.Unmute()

    def ToggleSpeaker(self):

        if self.speaker:
            self.speaker.Toggle()

    def event(self, eventtype):
        '''\
        Method to handle events received by main script.

        e.g. Modes can add events for when sounds finish 
        '''
        pass

    def playMusic(self, music):
        self.mixer.music.stop()
        sleep(0.02)
        self.mixer.music.load(music)
        self.Unmute()
        #self.mixer.music.set_volume(0.05)
        self.mixer.music.play()
    
    def Disco(self):
        d = self.display
        colours = [d.RED, d.BLUE, d.GREEN, d.WHITE, 
                   d.YELLOW, d.VIOLET, d.TEAL]

        sleep(0.5)

        while (self.mixer.get_init() and self.mixer.music.get_busy()):
            x = randint(5,15)
            self.display.changeColour(choice(colours))
            z = 0

            while z < x and (self.mixer.get_init() and 
                           self.mixer.music.get_busy()):
                sleep(0.05)
                z += 1

        self.display.changeColour(self.modecolour)

    def event(self, event):
        self.Mute()

    def quit(self):
        pass
        