##############################################################################
# A Raspberry Pi Muon Detector
#
# This file includes functions to read in a full event.
# The event consists of multiple reads from the Raspi GPIO and parsing
# the results into a lib.Event() object. Reads will have to be protected
# against concurrent access.
#
# Here will be the license that we use.
# Martin Hellmich (mhellmic@gmail.com)
##############################################################################

from threading import Lock

import lib


read_event_mutex = Lock()


def read_full_event():
    e = lib.Event()
    read_event_mutex.acquire()
    try:
        # read event
        # read gps
        pass
    finally:
        read_event_mutex.release()
    if False:
        raise lib.EventReadError()
    return e
