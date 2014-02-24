import time

import sensors
import events


DETECTION_TIMEOUT = 60


if __name__ == "__main__":

    while True:

        if sensors.detect_motion():
            print("MOTION DETECTED!")
            events.log_motion_event()
            time.sleep(DETECTION_TIMEOUT)