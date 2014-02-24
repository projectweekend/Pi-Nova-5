import RPi.GPIO as io
from sensors.settings import PIR_PIN


io.setmode(io.BCM)
io.setup(PIR_PIN, io.IN)


def detect_motion():
    if io.input(PIR_PIN):
        return True
    return False
