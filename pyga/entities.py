# -*- coding: utf-8 -*-

from datetime import datetime
from utils import get32bitRandom

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"

class Campaign(object):
    pass


class CustomVariable(object):
    pass


class Event(object):
    pass


class Item(object):
    pass


class Page(object):
    '''
    Contains all parameters needed for tracking a page

    Properties:
    path -- Page request URI, e.g. "/path/page.html", will be mapped to "utmp" parameter
    title -- Page title, will be mapped to "utmdt" parameter
    charset -- Charset encoding (e.g. "UTF-8"), will be mapped to "utmcs" parameter
    referrer -- Referer URL, e.g. "http://www.example.com/path/page.html",  will be mapped to "utmr" parameter
    load_time -- Page load time in milliseconds, will be encoded into "utme" parameter.

    '''
    REFERRER_INTERNAL = '0'

    def __init__(self, path):
        self.path = ''
        self.title = ''
        self.charset = ''
        self.referrer = ''
        self.load_time = ''

        if path_val:
            self.path= path

    def __setattr__(self, name, value):
        if name == 'path':
            if value and value != '':
                if value[0] != '/':
                    raise Exception('The page path should always start with a slash ("/").')
        elif name == 'load_time':
            if value and not isinstance(value, int):
                raise Exception('Page load time must be specified in integer milliseconds.')

        object.__setattr__(self, name, value)


class Session(object):
    '''
    You should serialize this object and store it in the user session to keep it
    persistent between requests (similar to the "__umtb" cookie of the GA Javascript client).

    Properties:
    session_id -- A unique per-session ID, will be mapped to "utmhid" parameter
    track_count -- The amount of pageviews that were tracked within this session so far,
                   will be part of the "__utmb" cookie parameter.
                   Will get incremented automatically upon each request
    start_time -- Timestamp of the start of this new session, will be part of the "__utmb" cookie parameter

    '''
    def __init__(self):
        self.session_id = get32bitRandom()
        self.track_count = 0
        self.start_time = datetime.now()

    @staticmethod
    def generate_session_id():
        return get32bitRandom()

    def extract_from_utmb(self, utmb):
        '''
        Will extract information for the "trackCount" and "startTime"
        properties from the given "__utmb" cookie value.
        '''
        parts = utmb.split('.')
        if len(parts) != 4:
            raise Exception('The given "__utmb" cookie value is invalid.')

        self.track_count = parts[1]
        self.start_time = datetime.fromtimestamp(parts[3])

        return self


class SocialInteraction(object):
    pass


class Tracker(object):
    pass


class Transaction(object):
    pass


class Visitor(object):
    pass


class Parameters(object):
    pass
