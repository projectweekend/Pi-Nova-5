import time

import sensors
import events
import lighting


DETECTION_TIMEOUT = 60
LUMINOSITY_THRESHOLD = 10
MAX_AUTH_FAILURES = 5


if __name__ == "__main__":

    # setup the HUE bridge
    try:
        hue_bridge = lighting.Bridge()

    # handle exceptions
    except lighting.BridgeNotFoundException:
        print("Red LED blink pattern: SOLID")

    except lighting.IPUtilityException:
        print("Red LED blink pattern: 01")

    except lighting.BridgeConfigurationException:
        print("Red LED blink pattern: 01")

    except lighting.BridgeAPIResponseException:
        print("Red LED blink pattern: 02")

    # we have the bridge...
    else:

        # main run loop
        while True:

            # start authorization process...
            AUTH_FAILURES = 0
            while not hue_bridge.authorized:
                # indicate that link button needs to be pressed
                if hue_bridge.press_link:
                    print("Blue LED blink pattern: 01")
                    # pause to give user time to press link button
                    time.sleep(10)
                # attempt authorization...
                try:
                    hue_bridge.authorize()
                except lighting.BridgeAPIResponseException:
                    print("Red LED blink pattern: 03")
                    AUTH_FAILURES += 1
                    if AUTH_FAILURES >= MAX_AUTH_FAILURES:
                        raise lighting.BridgeAuthAttemptsExceeded
                    time.sleep(5)
                else:
                    print("Green LED blink pattern: 01")

            # bridge is now authorized...
            while hue_bridge.authorized:
                # check for motion and log it
                if sensors.detect_motion():
                    print("MOTION DETECTED!")
                    events.log_motion_event()
                    # if it's dark enough then turn lights on
                    if sensors.read_luminosity() < LUMINOSITY_THRESHOLD:
                        # TODO: Make call to HUE API to turn on lights
                        print("LIGHTS ON!")
                    # Pause before checking for motion again
                    time.sleep(DETECTION_TIMEOUT)
