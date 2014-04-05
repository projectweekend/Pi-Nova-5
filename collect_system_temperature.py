import subprocess
import datetime

import utils
from stash import Stash


SHELL_COMMAND = ["/opt/vc/bin/vcgencmd", "measure_temp"]


def get_system_temp():
    system_result = subprocess.check_output(SHELL_COMMAND)
    celsius_temp = utils.parse_temp_value(system_result)
    fahrenheit_temp = utils.celsius_to_fahrenheit(celsius_temp)
    current_date = datetime.datetime.utcnow().isoformat()
    return {
        'date': current_date,
        'from': 'Starbug',
        'celsius':celsius_temp, 
        'fahrenheit': fahrenheit_temp
    }


def stash_system_temperature(temperature_value):
    system_temperature_stash = Stash("system_temperature")
    system_temperature_stash.add(temperature_value)


def worker():
    system_temperature = get_system_temp()
    stash_system_temperature(system_temperature)


if __name__ == "__main__":
    worker()
