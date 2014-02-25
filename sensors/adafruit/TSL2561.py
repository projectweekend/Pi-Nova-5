import time

# Sourced from: https://github.com/seanbechhofer/raspberrypi/blob/master/python/TSL2561.py
# TODO: Strip out values into constants.
from sensors.adafruit.Adafruit_I2C import Adafruit_I2C


class TSL2561(object):
    
    i2c = None

    def __init__(self, address=0x39, debug=0, pause=0.8):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.pause = pause
        self.debug = debug
        self.gain = 0
        self.i2c.write8(0x80, 0x03)

    def set_gain(self, gain=1):
        """ Set the gain """
        if gain != self.gain:
            if gain==1:
                self.i2c.write8(0x81, 0x02)     # set gain = 1X and timing = 402 mSec
                if self.debug:
                    print "Setting low gain"
            else:
                self.i2c.write8(0x81, 0x12)     # set gain = 16X and timing = 402 mSec
                if self.debug:
                    print "Setting high gain"
            self.gain=gain                     # safe gain for calculation
            time.sleep(self.pause)              # pause for integration (self.pause must be bigger than integration time)

    def read_word(self, reg):
        """Reads a word from the I2C device"""
        try:
            wordval = self.i2c.readU16(reg)
            newval = self.i2c.reverseByteOrder(wordval)
            if self.debug:
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, wordval & 0xFFFF, reg))
            return newval
        except IOError:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def read_full(self, reg=0x8C):
        """Reads visible+IR diode from the I2C device"""
        return self.read_word(reg)

    def read_ir(self, reg=0x8E):
        """Reads IR only diode from the I2C device"""
        return self.read_word(reg)

    def read_lux(self, gain = 0):
        """Grabs a lux reading either with autoranging (gain=0) or with a specified gain (1, 16)"""
        if gain == 1 or gain == 16:
            self.set_gain(gain) # low/highGain
            ambient = self.read_full()
            ir = self.read_ir()
        elif gain == 0: # auto gain
            self.set_gain(16) # first try highGain
            ambient = self.read_full()
            if ambient < 65535:
                ir = self.read_ir()
            if ambient >= 65535 or ir >= 65535:
                self.set_gain(1)
                ambient = self.read_full()
                ir = self.read_ir()

        if self.gain==1:
            ambient *= 16    # scale 1x to 16x
            ir *= 16         # scale 1x to 16x
                        
        ratio = (ir / float(ambient)) # changed to make it run under python 2

        if self.debug:
            print "ir Result", ir
            print "Ambient Result", ambient

        if (ratio >= 0) & (ratio <= 0.52):
            lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
        elif ratio <= 0.65:
            lux = (0.0229 * ambient) - (0.0291 * ir)
        elif ratio <= 0.80:
            lux = (0.0157 * ambient) - (0.018 * ir)
        elif ratio <= 1.3:
            lux = (0.00338 * ambient) - (0.0026 * ir)
        elif ratio > 1.3:
            lux = 0

        return lux
