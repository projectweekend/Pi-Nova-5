from adafruit import TSL2561


def read_luminosity():
    tsl = TSL2561()
    luminosity = tsl.read_lux(gain=1)
    return luminosity
