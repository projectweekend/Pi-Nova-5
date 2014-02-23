import time

import sensors


DETECTION_TIMEOUT = 60


if __name__ == "__main__":
    while True:
        if sensors.detect_motion():
            print("MOTION DETECTED!")
            time.sleep(DETECTION_TIMEOUT)