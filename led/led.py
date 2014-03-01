import time

import webcolors
from arduino.usbdevice import ArduinoUsbDevice


class LED(object):

    def __init__(self):

        self._digispark = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
        self.off()

    def on(self, color_name):
        rgb_values = webcolors.name_to_rgb(color_name)
        self._digispark.write(ord("s"))
        for v in rgb_values:
            self._digispark.write(v)

    def off(self):
        rgb_values = [0, 0, 0]
        self._digispark.write(ord("s"))
        for v in rgb_values:
            self._digispark.write(v)

    def blink(self, color_name, blink_count):
        self.off()
        for _ in xrange(blink_count):
            self.on(color_name)
            time.sleep(.75)
            self.off()
            time.sleep(.75)