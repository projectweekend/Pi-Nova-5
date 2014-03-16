import time

import sensors
import events
import lighting
import utils
import adafruit
from led import LED


DETECTION_TIMEOUT = 150
MAX_AUTH_FAILURES = 5


def connect_with_hue(led):
    try:
        hue_bridge = lighting.Bridge()
    except (lighting.BridgeNotFoundException,
            lighting.IPUtilityException,
            lighting.BridgeConfigurationException,
            lighting.BridgeAPIResponseException):
        led.on('red')
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
                led.blink('red', 3)
                AUTH_FAILURES += 1
                if AUTH_FAILURES >= MAX_AUTH_FAILURES:
                    led.blink('red', 10)
                    raise lighting.BridgeAuthAttemptsExceeded
                time.sleep(5)
            else:
                led.blink('green', 3)
                return hue_bridge


if __name__ == "__main__":

    led = LED()
    luminosity_sensor = adafruit.TSL2561()

    hue_bridge = connect_with_hue()

    while hue_bridge.authorized:
        # check for motion and log it
        if sensors.detect_motion():
            events.log_motion_event()
            lighting_config = utils.LightingConfig()
            # if it's dark enough then turn lights on
            current_luminosity = luminosity_sensor.read_lux(gain=1)
            if current_luminosity < lighting_config.luminosity_threshold():
                if not lighting_config.auto_lighting_disabled():
                    hue_bridge.lights_on(lighting_config.enabled_lights())
            # Pause before checking for motion again
            time.sleep(DETECTION_TIMEOUT)
