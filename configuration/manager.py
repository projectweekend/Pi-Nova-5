from hammock import Hammock
from stash import Stash
# TODO: make a messaging module that can be imported


BASE_API_URL = 'http://holly.local/api/'
STASH_FILE_NAME = 'nova5_config_options'


class ConfigurationManager(object):

    config_data = {}


    def __init__(self, api_url, system_name):
        self._api = Hammock(api_url)
        self._system_name = system_name
        self._get_stash()

    def load(self):
        if self._stash.data:            
            self.config_data = self._stash.data.pop()
            self._stash.empty()

    def save(self):
        self._stash.add(self.config_data)

    def pull(self):
        url_params = {'system_name': self._system_name}
        response = self.api.GET(params=url_params)
        if response.status_code != 200:
            message_body = "Unable to pull new config data from {0}"
            self._send_failure_message(message_body.format())
            return False
        self._load_config_data(response.json())

    def build(self):
        pass

    def _get_stash(self):
        stash_file_name = "{0}_configuration_data".format(self._system_name.lower())
        self._stash = Stash(stash_file_name)

    def _load_config_data(self, json_data):
        if json_data:
            self.config_data = json_data[0]['system_options']

    def _send_failure_message(self, message_body):
        # TODO: use messaging module to report this back to Holly
        # Take the custom message body passed in here and use it in messaging module call
        pass
