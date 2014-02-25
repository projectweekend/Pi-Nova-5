import time

import sensors
import events


DETECTION_TIMEOUT = 60
LUMINOSITY_THRESHOLD = 10


if __name__ == "__main__":

    while True:

        if sensors.detect_motion():

            print("MOTION DETECTED!")
            events.log_motion_event()

            current_luminosity = sensors.read_luminosity()
            if current_luminosity < LUMINOSITY_THRESHOLD:
                # TODO: Make call to HUE API to turn on lights
                pass
            
            time.sleep(DETECTION_TIMEOUT)