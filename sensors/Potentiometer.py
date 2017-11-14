from sensors import Sensor
import time
import os
import RPi.GPIO as GPIO


class Potentiometer(Sensor.Sensor):
    def __init__(self, name, full_name, type, connection=None):
        # super().__init__(name, full_name, type, connection)
        self.name = name
        self.full_name = full_name
        self.type = type
        # self.connection = connection
        GPIO.setmode(GPIO.BCM)
        self.DEBUG = 1

        # change these as desired - they're the pins connected from the
        # SPI port on the ADC to the Cobbler
        self.SPICLK = 18
        self.SPIMISO = 23
        self.SPIMOSI = 24
        self.SPICS = 25

        # set up the SPI interface pins
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)


        # 10k trim pot connected to adc #0
        self.potentiometer_adc = 0;

        last_read = 0       # this keeps track of the last potentiometer value
        tolerance = 5       # to keep from being jittery we'll only change
        # volume when the pot has moved more than 5 'counts'
        print("Potentiometer created!")


    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it

        return adcout

    def get_data(self):
        return self.readadc(self.potentiometer_adc, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
