import logging
import time
import RPi.GPIO as gpio

import events
import utils
import adafruit
from led import LED

DETECTION_TIMEOUT = 180
PIR_PIN = 18

gpio.setmode(gpio.BCM)
gpio.setup(PIR_PIN, gpio.IN)


if __name__ == "__main__":

    led = LED()
    luminosity_sensor = adafruit.TSL2561()
    hue_bridge = utils.connect_with_hue(led)

    while True:
        
        # load config data before waiting for motion event
        lighting_config = utils.LightingConfig()
        lights_included_for_use = lighting_config.enabled_lights()
        luminosity_threshold = lighting_config.luminosity_threshold()

        # this blocks execution until motion is detected
        gpio.wait_for_edge(PIR_PIN, gpio.RISING)

        # everything below is executed only when motion is detected
        events.log_motion_event()
        if not lighting_config.auto_lighting_disabled():
            if hue_bridge:
                current_luminosity = luminosity_sensor.read_lux(gain=1)
                if current_luminosity < luminosity_threshold:
                    hue_bridge.lights_on(lights_included_for_use)
            else:
                led.blink('red', 3)
        # Wait before restarting loop
        time.sleep(DETECTION_TIMEOUT)
