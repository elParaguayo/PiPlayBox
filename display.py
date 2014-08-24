from AdafruitLCD.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class Display(Adafruit_CharLCDPlate):

    def __init__(self):
        super(Display, self).__init__()
        self.begin(16,2)
        self.clear()
        self.message("PiPlayBox\nWarming up...")
        self.colour = self.WHITE

    def Update(self, message):
    	self.clear()
    	self.message(message)

    def Test(self):
        """Displays a test message. Useful for checking that screen is
        working.
        """
        self.message("LCD screen\nON!")

    def Off(self):
        self.backlight(self.OFF)

    def On(self):
        self.backlight(self.colour)

    def changeColour(self, colour):
        self.colour = colour
        self.backlight(self.colour)

