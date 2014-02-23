import time

import sensors

pir_pin = 18
io.setup(pir_pin, io.IN)


if __name__ == "__main__":
    while True:
        if sensors.detect_motion():
            print("MOTION DETECTED!")
        time.sleep(0.5)