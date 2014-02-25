import time

import sensors
import events

HUE_SYSTEM_IS_READY = False
DETECTION_TIMEOUT = 60
LUMINOSITY_THRESHOLD = 10


if __name__ == "__main__":

    # main loop
    while True:

        if not HUE_SYSTEM_IS_READY:
            # Run initialization process here
            # This will have it's own loop and will not exit 
            # until completed successfully. Set HUE_SYSTEM_IS_READY = True
            pass
        
        if HUE_SYSTEM_IS_READY:
            
            if sensors.detect_motion():
                print("MOTION DETECTED!")
                events.log_motion_event()

                if sensors.read_luminosity() < LUMINOSITY_THRESHOLD:
                    # TODO: Make call to HUE API to turn on lights
                    print("LIGHTS ON!")

                time.sleep(DETECTION_TIMEOUT)
