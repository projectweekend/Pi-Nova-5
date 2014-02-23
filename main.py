import time

import sensors


if __name__ == "__main__":
    while True:
        if sensors.detect_motion():
            print("MOTION DETECTED!")
        time.sleep(0.5)