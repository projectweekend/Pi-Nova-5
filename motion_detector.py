import time
import RPi.GPIO as io


io.setmode(io.BCM)

pir_pin = 18
io.setup(pir_pin, io.IN)


if __name__ == "__main__":
    while True:
        if io.input(pir_pin):
            print("MOTION DETECTED!")
        time.sleep(0.5)