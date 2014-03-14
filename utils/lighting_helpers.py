from datetime import datetime
from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'


def get_enabled_lights():
    manager = ConfigurationManager(API_URL, SYSTEM_NAME)
    list_of_lights = manager.read('lights_enabled')
    if not list_of_lights:
        return []
    return list_of_lights


def get_luminosity_threshold():
    manager = ConfigurationManager(API_URL, SYSTEM_NAME)
    luminosity_threshold = manager.read('luminosity_threshold')
    if not luminosity_threshold:
        # return a default
        return 10 
    return luminosity_threshold


def is_auto_lighting_enabled():
    manager = ConfigurationManager(API_URL, SYSTEM_NAME)
    disabled_start = manager.read('disabled_time_start')
    disabled_end = manager.read('disabled_time_end')

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
