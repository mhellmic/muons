##############################################################################
# A Raspberry Pi Muon Detector
#
# This script starts a daemon that listens to a
# muon detector, reads in events, and send them to a
# central server.
#
# Here will be the license that we use.
# Martin Hellmich (mhellmic@gmail.com)
##############################################################################

# system imports
import argparse
from functools import partial
import Queue
import signal
import sys
import test

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('Error importing RPi.GPIO!'
          ' This is probably because you need superuser privileges.'
          ' You can achieve this by using \'sudo\' to run your script')
    sys.exit(1)
except ImportError:
    print('Be sure to run this on a Raspberry Pi B+ ;)')
    print('Continuing anyway ...')

# local imports
import gpio
import lib


def register_event_handler(event_handler_func):
    GPIO.add_event_detect(lib.TRIGGER,
                          GPIO.RISING,
                          callback=event_handler_func,
                          bouncetime=20)


def read_event_to_queue(channel):
    # read event data
    try:
        e = gpio.read_full_event()
    except lib.EventError as e:
        print e
    else:
        # write event object to queue
        event_queue.put_nowait(e)


def store_event(store_event_handler_list):
    while True:
        e = event_queue.get()
        for handler_func in store_event_handler_list:
            # TODO: parallelize this?
            handler_func(e)


def print_event(event):
    print 'Event = {0}'.format(event)


def log_event(event, path):
    try:
        efile = open(path, 'a')
    except IOError as e:
        print e
    else:
        with efile:
            efile.write('{0}\n'.format(str(event)))


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lib.TRIGGER, GPIO.IN)
    GPIO.setup(lib.GPS_IN, GPIO.IN)
    GPIO.setup(lib.GPS_OUT, GPIO.OUT)


def cleanup_gpio():
    GPIO.cleanup()


def signal_handler(signal, frame):
    print 'Received Ctrl-C'
    exit_code = 0
    cleanup_gpio()
    sys.exit(exit_code)


parser = argparse.ArgumentParser(description='muon detector daemon.',
                                 prog='muon_detect_server')
parser.add_argument('-d', '--daemon', action='store_true',
                    help='run this script as daemon in the background')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 0.1',
                    help='print the program version')
parser.add_argument('-t', '--test', action='store_true',
                    help='test the procesing chain with fake event data')
parser.add_argument('-e', '--event-logfile',
                    help='the event log for recovery')

args = parser.parse_args()

if args.event_logfile is not None:
    try:
        f = open(args.event_logfile, 'a')
    except IOError as e:
        print 'Failed to open the specified log file: {0}\n{1}'.format(
            args.event_logfile, e)
        sys.exit(1)
    else:
        f.close()

# create an infinitely large queue for events
event_queue = Queue.Queue(maxsize=0)

if args.test:
    print 'Starting test mode ... Generating events.'
    lib.start_thread(test.read_fake_event_to_queue, None, event_queue)
    signal.signal(signal.SIGINT, test.signal_handler)
else:  # the normal case
    print 'Starting work mode ... Reading from GPIO.'
    init_gpio()
    register_event_handler(read_event_to_queue)
    signal.signal(signal.SIGINT, signal_handler)

#start event writer
lib.start_thread(store_event, [print_event,
                               partial(log_event, path=args.event_logfile)
                               ])

# wait for the end ...
signal.pause()
