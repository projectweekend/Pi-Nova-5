import time

from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'


if __name__ == "__main__":

    refresh_attempts = 0
    refresh_complete = False

    manager = ConfigurationManager(API_URL, SYSTEM_NAME)

    while refresh_complete == False and refresh_attempts < 6:
        try:
            manager.get_updates()
        except:
            refresh_attempts += 1
            time.sleep(5)
        else:
            refresh_complete = True

    if refresh_complete == False:
        # TODO log failure with a message to Holly
        pass
