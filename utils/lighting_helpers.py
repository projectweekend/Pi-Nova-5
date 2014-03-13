from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'


def get_enabled_lights():
    manager = ConfigurationManager(API_URL, SYSTEM_NAME)
    list_of_lights = manager.read('lights_enabled')
    if not list_of_lights:
        return []
    return list_of_lights
