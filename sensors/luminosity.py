from adafruit import TSL2561


def read_luminosity():
    tsl = TSL2561()
    return tsl.read_lux(gain=1)