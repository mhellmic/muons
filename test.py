##############################################################################
# A Raspberry Pi Muon Detector
#
# This file includes the necessary functions for tests.
#
# Here will be the license that we use.
# Martin Hellmich (mhellmic@gmail.com)
##############################################################################

import random
import sys
import time

import lib


def signal_handler(signal, frame):
    print 'Received Ctrl-C'
    exit_code = 0
    sys.exit(exit_code)


def read_fake_event_to_queue(channel, event_queue):
    no_events = 1000
    for i in range(no_events):
        print 'Created {0} events.'.format(i)
        e = lib.Event(strength=float(i))
        event_queue.put_nowait(e)
        time.sleep(random.random() + 0.5)
