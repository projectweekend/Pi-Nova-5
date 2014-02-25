import requests
from custom_exceptions import *


IP_UTILITY_URL = 'http://www.meethue.com/api/nupnp'
HUE_AUTHORIZED_USER_CONFIG = {
    'devicetype': 'Nova5.local',
    'username': 'nova5dotlocal'
}


class Light(object):
    pass


class Bridge(object):

    ip_address = ""
    username = ""
    authorized = False
    lights = {}

    def __init__(self, ip="", username=HUE_AUTHORIZED_USER_CONFIG['username']):

        if ip:
            self.ip_address = ip
        else:
            self._find_ip_address()

        self.username = username
        self._check_authorization()

    # Set the ip_address using HUE API web utility
    def _find_ip_address(self):

        utility_response = requests.get(IP_UTILITY_URL)
        if utility_response.status_code != 200:
            message = "IP utility was not available at: {0}".format(IP_UTILITY_URL)
            raise IPUtilityException(message)

        response_data = utility_response.json()
        if not response_data:
            message = "No bridge was located on this network"
            raise BridgeNotFoundException(message)

        self.ip_address = response_data[0]['internalipaddress']

    def _check_authorization(self):

        if not self.ip_address:
            message = "The 'ip_address' property is empty"
            raise BridgeConfigurationException(message)

        authorization_check_url = "{0}/api/{1}".format(self.ip_address, self.username)
        authorization_check_response = requests.get(authorization_check_url)

        if authorization_check_response.status_code != 200:
            message = "The bridge did not respond on route '{0}'".format(authorization_check_url)
            raise BridgeAPIResponseException(message)

        response_data = authorization_check_response.json()
        unauthorized_error = response_data[0].get('error', '')

        if not unauthorized_error:
            self.authorized = True

        if unauthorized_error['type'] == 1:
            self.authorized = False
        else:
            error_type = unauthorized_error['type']
            error_desc = unauthorized_error['description']
            message = "Received an unexpected error response. TYPE: {0}. DESCRIPTION: {1}".format(error_type, error_desc)
            raise BridgeAPIResponseException(message)

    def _authorize(self):

        if not self._check_authorization():
            pass


