import logging
import time
import RPi.GPIO as gpio

import events
import lighting
import utils
import adafruit
from led import LED

DETECTION_TIMEOUT = 180
MAX_AUTH_FAILURES = 5
PIR_PIN = 18

gpio.setmode(gpio.BCM)
gpio.setup(PIR_PIN, gpio.IN)


def connect_with_hue(led):
    try:
        hue_bridge = lighting.Bridge()
    except (lighting.BridgeNotFoundException,
            lighting.IPUtilityException,
            lighting.BridgeConfigurationException,
            lighting.BridgeAPIResponseException):
        led.on('red')
        return None
    else:
        # bridge is authorized...
        if hue_bridge.authorized:
            led.blink('green', 3)
            return hue_bridge
        # bridge needs to authorize..
        AUTH_FAILURES = 0
        while not hue_bridge.authorized:
            # indicate that link button needs to be pressed
            if hue_bridge.press_link:
                led.blink('blue', 3)
                # pause to give user time to press link button
                time.sleep(5)
            # attempt authorization...
            try:
                hue_bridge.authorize()
            except lighting.BridgeAPIResponseException:
                led.blink('red', 2)
                AUTH_FAILURES += 1
                if AUTH_FAILURES >= MAX_AUTH_FAILURES:
                    led.blink('red', 10)
                    raise lighting.BridgeAuthAttemptsExceeded
                # wait 5 seconds before reattempting after a failure
                time.sleep(5)
            else:
                led.blink('green', 3)
                return hue_bridge


if __name__ == "__main__":

    led = LED()
    luminosity_sensor = adafruit.TSL2561()
    hue_bridge = connect_with_hue(led)

    while True:
        # this blocks execution until motion is detected
        lighting_config = utils.LightingConfig()
        gpio.wait_for_edge(PIR_PIN, gpio.RISING)
        # everything below is executed only when motion is detected
        events.log_motion_event()
        if hue_bridge and not lighting_config.auto_lighting_disabled():
            current_luminosity = luminosity_sensor.read_lux(gain=1)
            if current_luminosity < lighting_config.luminosity_threshold():
                hue_bridge.lights_on(lighting_config.enabled_lights())
        elif not hue_bridge:
            led.blink('red', 3)
        # Wait before returning to loop
        time.sleep(DETECTION_TIMEOUT)
