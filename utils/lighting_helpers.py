from datetime import datetime
from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'
LUMINOSITY_THRESHOLD_DEFAULT = 10


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

        if past_start_hour or (on_start_hour and past_start_minute):
            if before_end_hour or (on_end_hour and before_end_minute):
                return True
        return False
