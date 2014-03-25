import time
from datetime import datetime

import lighting
from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'
LUMINOSITY_THRESHOLD_DEFAULT = 10
MAX_AUTH_FAILURES = 5


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
        else:
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


class LightingConfig(object):

    def __init__(self):
        
        self._manager = ConfigurationManager(API_URL, SYSTEM_NAME)

    def enabled_lights(self):
        list_of_lights = self._manager.read('lights_enabled')
        if not list_of_lights:
            return []
        return list_of_lights

    def luminosity_threshold(self):
        luminosity_threshold = self._manager.read('luminosity_threshold')
        if not luminosity_threshold:
            return LUMINOSITY_THRESHOLD_DEFAULT
        return luminosity_threshold

    def auto_lighting_disabled(self):

        if self._manager.read('manually_disabled'):
            return True

        disabled_start = self._manager.read('disabled_time_start')
        disabled_end = self._manager.read('disabled_time_end')

        now = datetime.now()

        on_start_hour = now.hour == disabled_start['hour']
        past_start_hour = now.hour > disabled_start['hour']
        past_start_minute = now.minute >= disabled_start['minute']

        on_end_hour = now.hour == disabled_end['hour']
        before_end_hour = now.hour < disabled_end['hour']
        before_end_minute = now.hour <= disabled_end['minute']

        has_started = past_start_hour or (on_start_hour and past_start_minute)
        has_not_ended = before_end_hour or (on_end_hour and before_end_minute)

        if has_started or has_not_ended:
                return True
        return False
