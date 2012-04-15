# -*- coding: utf-8 -*-

from base import Config

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"


Class Q(object):
    REQ_ARRAY = []

    def add_wrapped_request(self, req_wrapper):
        self.REQ_ARRAY.append(req_wrapper)


class GIFRequest(object):
    '''

    Properties:
    type -- Indicates the type of request, will be mapped to "utmt" parameter
    config --
    x_forwarded_for --
    user_agent --

    '''
    def __init__(self, config):
        self.type = None
        self.config = None
        self.x_forwarded_for = None
        self.user_agent = None
        self.__Q = Q()
        if isinstance(config, Config):
            self.config = config

    def build_http_request(self):
        params = self.build_parameters()

    def build_parameters(self):
        return {}

    def __send(self):
        pass

    def fire(self):
        '''
        Simply delegates to send() if config option "queue_requests" is disabled
        else enqueues the request into Q object: you should call pyga.shutdowon
        as last statement, to actually send out all queued requests.
        '''
        if config.queue_requests:
            # Queuing results. You should call pyga.shutdown as last statement to send out requests.
            self.__Q.add_wrapped_request((lambda: self.__send()))
        else:
            self.__send()


class Request(GIFRequest):
    def __init__(self, config, tracker=None, visitor=None, session=None):
        super(self, Request).__init__(config)
        self.tracker = tracker
        self.visitor = visitor
        self.session = session


class ItemRequest(Request):
    pass


class PageViewRequest(Request):
    pass


class EventRequest(Request):
    pass


class SocialInteractionRequest(Request):
    pass


class TransactionRequest(Request):
    pass
