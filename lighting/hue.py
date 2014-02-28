import json
import requests
from hammock import Hammock
from custom_exceptions import *


IP_UTILITY_URL = 'http://www.meethue.com/api/nupnp'
HUE_AUTHORIZED_USER_CONFIG = {
    'devicetype': 'Nova5.local',
    'username': 'nova5dotlocal'
}


class Light(object):
    
    def __init__(self, api, username, light_id):
        self.id = light_id
        self.username = username
        self.api = api

    def on(self):
        self.api(self.username).lights(self.id).state.PUT(data=json.dumps({'on': True}))


class Bridge(object):

    def __init__(self, ip="", user_config=HUE_AUTHORIZED_USER_CONFIG):

        if ip:
            self.ip_address = ip
        else:
            self._find_ip_address()

        self.api = Hammock("http://{0}/api".format(self.ip_address))
        self.user_config = user_config
        self.authorized = False
        self.press_link = False
        self.lights = {}
        self._check_authorization()

    @staticmethod
    def _parse_error(self, response_data):
        return response_data[0].get('error', '')

    # Set the ip_address using HUE API web utility
    def _find_ip_address(self):

        utility_response = requests.get(IP_UTILITY_URL)
        if utility_response.status_code != 200:
            message = "IP utility was not available at: {0}".format(IP_UTILITY_URL)
            raise IPUtilityException(message)

        data = utility_response.json()
        if not data:
            message = "No bridge was located on this network"
            raise BridgeNotFoundException(message)

        self.ip_address = data[0]['internalipaddress']

    def _check_authorization(self):

        r = self.api(self.user_config['username']).GET()

        if r.status_code != 200:
            message = "The bridge did not respond properly on route '{0}'".format(r.url)
            raise BridgeAPIResponseException(message)

        data = r.json()

        # if authorized, the response is a dictionary of light data
        if isinstance(data, dict):
            self.authorized = True
            self._find_lights()
            return

        # if unauthorized, then response is a list with an error dictionary inside
        unauthorized_error = self._parse_error(data)
        if unauthorized_error and unauthorized_error['type'] == 1:
            self.authorized = False
        else:
            error_type = unauthorized_error['type']
            error_desc = unauthorized_error['description']
            message = "Received an unexpected error. TYPE: {0}. DESCRIPTION: {1}".format(error_type, error_desc)
            raise BridgeAPIResponseException(message)

    def _find_lights(self):

        r = self.api(self.user_config['username']).lights.GET()

        if r.status_code != 200:
            message = "The bridge did not respond properly on route '{0}'".format(r.url)
            raise BridgeAPIResponseException(message)

        data = r.json()
        for k in data.keys():
            self.lights[k] = Light(self.api, self.user_config['username'], k)

    def authorize(self):

        if not self.authorized:

            r = self.api.POST(data=json.dumps(HUE_AUTHORIZED_USER_CONFIG))

            if r.status_code != 200:
                message = "The bridge did not respond properly on route: '{0}'".format(r.url)
                raise BridgeAPIResponseException(message)

            data = r.json()
            unauthorized_error = self._parse_error(data)

            if not unauthorized_error:
                self.authorized = True
                self.press_link = False
                self._find_lights()
                return

            if unauthorized_error['type'] == 101:
                self.authorized = False
                self.press_link = True
            else:
                error_type = unauthorized_error['type']
                error_desc = unauthorized_error['description']
                message = "Received an unexpected error. TYPE: {0}. DESCRIPTION: {1}".format(error_type, error_desc)
                raise BridgeAPIResponseException(message)

    def lights_on(self):
        
        if self.authorized:

            for k, light in self.lights.items():
                light.on()
