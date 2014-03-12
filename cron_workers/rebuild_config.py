from configuration import ConfigurationManager


API_URL = 'http://holly.local/api/system/configuration'
SYSTEM_NAME = 'Nova5'


if __name__ == "__main__":
    manager = ConfigurationManager(API_URL, SYSTEM_NAME)
    manager.get_updates()
