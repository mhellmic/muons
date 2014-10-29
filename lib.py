##############################################################################
# A Raspberry Pi Muon Detector
#
# This script holds constants and data structures that are used in
# several places.
#
# Here will be the license that we use.
# Martin Hellmich (mhellmic@gmail.com)
##############################################################################

from collections import namedtuple
from datetime import datetime
import threading

# GPIO constants in GPIO.BOARD configuration
TRIGGER = 22
GPS_IN = 10
GPS_OUT = 8

Position = namedtuple('Position', 'lat lon alt')


class Event(object):
    date = datetime.now()
    strength = 0.0
    position = Position(0.0, 0.0, 0.0)  # lat, lon, alt
    angle = 0.0

    def __init__(self,
                 date=None,
                 strength=None,
                 position=None,
                 angle=None):
        self.strength = strength
        self.date = datetime.now()

    def __str__(self):
        return '{0};{1};{2},{3},{4};{5}'.format(
            self.date,
            self.strength,
            self.position.lat, self.position.lon, self.position.alt,
            self.angle
        )


class EventError(Exception):
    pass


class EventReadError(EventError):
    pass


def start_thread(f, *args):
    t = threading.Thread(target=f, args=(args))
    t.daemon = True
    t.start()
    return t
