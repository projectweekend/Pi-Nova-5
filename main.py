import time

import sensors
import events
import lighting

HUE_SYSTEM_IS_READY = False
DETECTION_TIMEOUT = 60
LUMINOSITY_THRESHOLD = 10
MAX_AUTH_ATTEMPTS = 5


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
        print("Red LED blink pattern: 02")

    except lighting.BridgeAPIResponseException:
        print("Red LED blink pattern: 03")

    # we have the bridge...
    else:
        # main run loop
        while True:
            # start authorization...
            AUTH_ATTEMPTS = 0
            while not hue_bridge.authorized:
                AUTH_ATTEMPTS += 1
                # indicate that link button needs to be pressed
                if hue_bridge.press_link:
                    print("Blue LED blink pattern: 01")
                    # pause to give user time to press link button
                    time.sleep(5)
                # attempt authorization...
                try:
                    hue_bridge.authorize()
                    print("Green LED blink pattern: 01")
                except lighting.BridgeAPIResponseException:
                    print("Red LED blink pattern: 04")
                    time.sleep(5)
                if AUTH_ATTEMPTS >= MAX_AUTH_ATTEMPTS:
                    raise lighting.BridgeAuthAttemptsExceeded

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
