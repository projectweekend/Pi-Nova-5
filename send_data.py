import time
import holly
from stash import Stash


def process_motion_data():
    motion_stash = Stash("motion_events")
    if motion_stash.data:
        data_created = holly.send_bulk_movement_log_data(motion_stash.data)
        if data_created:
            motion_stash.empty()
            return
    motion_stash.close()


def process_system_temperature_data():
    system_temperature_stash = Stash("system_temperature")
    if system_temperature_stash.data:
        data_created = holly.send_bulk_system_temperature_data(system_temperature_stash.data)
        if data_created:
            system_temperature_stash.empty()
            return
    system_temperature_stash.close()


def worker():

    number_of_attempts = 0

    while number_of_attempts <= 5:
        try:
            process_motion_data()
        except:
            number_of_attempts += 1
            time.sleep(10)
        else:
            break

    number_of_attempts = 0
    while number_of_attempts <= 5:
        try:
            process_system_temperature_data()
        except:
            number_of_attempts += 1
            time.sleep(10)
        else:
            break


if __name__ == "__main__":
    worker()
