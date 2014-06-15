import time
import RPi.GPIO as gpio
from lighting import Bridge


DETECTION_TIMEOUT = 60
MOTION_PIN = 18

gpio.setmode(gpio.BCM)
gpio.setup(MOTION_PIN, gpio.IN, pull_up_down=gpio.PUD_DOWN)


if __name__ == "__main__":

    hue = Bridge()

    while True:
        gpio.wait_for_edge(MOTION_PIN, gpio.RISING)
        hue.lights_on()
        time.sleep(DETECTION_TIMEOUT)
