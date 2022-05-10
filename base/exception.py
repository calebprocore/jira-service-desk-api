import os
import sys
from datetime import datetime as dt

"""
Failure         - not an exception, but a programmer defined error, log and continue
FatalException  - is an exception, exit program
Error           - is an exception but continue, no exit
"""


class Failure(object):
    """
    Failure     = programmer discretion error, not an exception, log and do not exit
    """

    def __init__(self, msg):
        # todo: log all msgs somewhere
        print('Error: ', msg)


class FatalException(Exception):
    """
    Fast fail exception, exit program.

    FataException   = an exception, log and exit
    """

    def __init__(self, e, msg):
        print('\n\n---------------------------------------------------------------------')
        print('FatalException: Exiting...', e)
        print('Error: ', msg)

        # fail fast, exit
        sys.exit(-1)
        # os._exit(-1)
        # raise SystemExit('Exiting...')  # finally executed, no sys import
        # print("fatal error", file=sys.stderr)
        # sys.exit()  # will exit, finally in try/catch/finally will get run


class Error(Exception):
    """
    Error = an Exception, but do not exit
    """

    def __init__(self, e, msg):
        print('Error/Exception:', e)
        print('Error: ', msg)
