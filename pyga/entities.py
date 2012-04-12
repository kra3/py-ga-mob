# -*- coding: utf-8 -*-

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

    Keyword Arguments:
    path -- Page request URI, e.g. "/path/page.html", will be mapped to "utmp" parameter
    title -- Page title, will be mapped to "utmdt" parameter
    charset -- Charset encoding (e.g. "UTF-8"), will be mapped to "utmcs" parameter
    referrer -- Referer URL, e.g. "http://www.example.com/path/page.html",  will be mapped to "utmr" parameter
    load_time -- Page load time in milliseconds, will be encoded into "utme" parameter.

    '''
    REFERRER_INTERNAL = '0'

    def __init__(self, path_val):
        self.path = ''
        self.title = ''
        self.charset = ''
        self.referrer = ''
        self.load_time = ''

        if path_val:
            self.path= path_val

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
    pass


class SocialInteraction(object):
    pass


class Tracker(object):
    pass


class Transaction(object):
    pass


class Visitor(object):
    pass
