from adafruit import TSL2561


def read_luminosity():
    tsl = TSL2561()
    try:
        luminosity = tsl.read_lux(gain=16)
    except ZeroDivisionError:
        luminosity = 0
    return luminosity
