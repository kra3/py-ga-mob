# -*- coding: utf-8 -*-

from math import floor
from base import Config, Parameters, Tracker, X10
from entities import Campaign, CustomVariable, Event, Item, Page, Session, SocialInteraction, Transaction, Visitor

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
    config -- base.Config object
    x_forwarded_for --
    user_agent -- User Agent String

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
    TYPE_PAGE = null
    TYPE_EVENT = 'event'
    TYPE_TRANSACTION = 'tran'
    TYPE_ITEM = 'item'
    TYPE_SOCIAL = 'social'

    '''
    This type of request is deprecated in favor of encoding custom variables
    within the "utme" parameter, but we include it here for completeness
    '''
    TYPE_CUSTOMVARIABLE = 'var'

    X10_CUSTOMVAR_NAME_PROJECT_ID = 8
    X10_CUSTOMVAR_VALUE_PROJCT_ID = 9
    X10_CUSTOMVAR_SCOPE_PROJECT_ID = 11


    def __init__(self, config, tracker, visitor, session):
        super(Request, self).__init__(config)
        self.tracker = tracker
        self.visitor = visitor
        self.session = session

    def build_http_request(self):
        self.x_forwarded_for = self.visitor.ip_address
        self.user_agent = self.visitor.user_agent


class ItemRequest(Request):
    def __init__(self, config, tracker, visitor, session, item):
        super(ItemRequest, self).__init__(config, tracker, visitor, session)
        self.item = item

    def get_type(self):
        ItemRequest.TYPE_ITEM

    def build_parameters(self):
        params = super(ItemRequest, self).build_parameters()
        params['utmtid'] = self.item.order_id
        params['utmipc'] = self.item.sku
        params['utmipn'] = self.item.name
        params['utmiva'] = self.item.variation
        params['utmipr'] = self.item.price
        params['utmiqt'] = self.item.quantity
        return params

    def build_visitor_parameters(self, parameters):
        '''
        The GA Javascript client doesn't send any visitor information for
        e-commerce requests, so we don't either.
        '''
        return parameters

    def build_custom_variable_parameters(self, parameters):
        '''
        The GA Javascript client doesn't send any custom variables for
        e-commerce requests, so we don't either.
        '''
        return parameters


class PageViewRequest(Request):
    X10_SITESPEED_PROJECT_ID = 14

    def __init__(self, config, tracker, visitor, session, page):
        super(PageViewRequest, self).__init__(config, tracker, visitor, session)
        self.page = page

    def get_type(self):
        PageViewRequest.TYPE_PAGEVIEW

    def build_parameters(self):
        params = super(PageViewRequest, self).build_parameters()
        params['utmp'] = self.page.path
        params['utmdt'] = self.page.title

        if self.page.charset:
            params['utmcs'] = self.page.charset

        if self.page.referrer:
            params['utmr'] = self.page.referrer

        if self.page.load_time:
            if params.get('utmn', 0) % 100 <  self.config.site_speed_sample_rate:
                x10 = X10()
                x10.clear_key(self.X10_SITESPEED_PROJECT_ID)
                x10.clear_value(self.X10_SITESPEED_PROJECT_ID)

                # from ga.js
                key = max(min(floor(self.page.load_time / 100), 5000), 0) * 100
                x10.set_key(self.X10_SITESPEED_PROJECT_ID, X10.OBJECT_KEY_NUM, key)
                x10.set_value(self.X10_SITESPEED_PROJECT_ID, X10.VALUE_VALUE_NUM, self.page.load_time)
                params['utme'] = '%s%s' % (params['utme'], x10.render_url_string())

        return params


class EventRequest(Request):
    X10_EVENT_PROJECT_ID = 5

    def __init__(self, config, tracker, visitor, session, event):
        super(EventRequest, self).__init__(config, tracker, visitor, session)
        self.event = event

    def get_type(self):
        EventRequest.TYPE_EVENT

    def build_parameters(self):
        params = super(EventRequest, self).build_parameters()
        x10 = X10()
        x10.clear_key(self.X10_EVENT_PROJECT_ID)
        x10.clear_value(self.X10_EVENT_PROJECT_ID)
        x10.set_key(self.X10_EVENT_PROJECT_ID, X10.OBJECT_KEY_NUM, self.event.category)
        x10.set_key(self.X10_EVENT_PROJECT_ID, X10.TYPE_KEY_NUM, self.event.action)

        if self.event.label:
            x10.set_key(self.X10_EVENT_PROJECT_ID, X10.LABEL_KEY_NUM, self.event.label)

        if self.event.value:
            x10.set_value(self.X10_EVENT_PROJECT_ID, X10.VALUE_VALUE_NUM, self.event.value)

        params['utme'] = "%s%s" % (params['utme'], x10.render_url_string())

        if self.event.noninteraction:
            params['utmni'] = 1

        return params


class SocialInteractionRequest(Request):
    def __init__(self, config, tracker, visitor, session, social_interaction, page):
        super(SocialInteractionRequest, self).__init__(config, tracker, visitor, session)
        self.social_interaction = social_interaction
        self.page = page

    def get_type(self):
        SocialInteractionRequest.TYPE_SOCIAL

    def build_parameters(self):
        params = super(SocialInteractionRequest, self).build_parameters()

        tmppagepath = self.social_interaction.target
        if tmppagepath == None:
            tmppagepath = self.page.path

        params['utmsn'] = self.social_interaction.network
        params['utmsa'] = self.social_interaction.action
        params['utmsid'] = tmppagepath
        return params


class TransactionRequest(Request):
    def __init__(self, config, tracker, visitor, session, transaction):
        super(TransactionRequest, self).__init__(config, tracker, visitor, session)
        self.transaction =  transaction

    def get_type(self):
        TransactionRequest.TYPE_TRANSACTION

    def build_parameters(self):
        params = super(TransactionRequest, self).build_parameters()
        params['utmtid'] = self.transaction.order_id
        params['utmtst'] = self.transaction.affiliation
        params['utmtto'] = self.transaction.total
        params['utmttx'] = self.transaction.tax
        params['utmtsp'] = self.transaction.shipping
        params['utmtci'] = self.transaction.city
        params['utmtrg'] = self.transaction.state
        params['utmtco'] = self.transaction.country
        return params

    def build_visitor_parameters(self, parameters):
        '''
        The GA Javascript client doesn't send any visitor information for
        e-commerce requests, so we don't either.
        '''
        return parameters

    def build_custom_variable_parameters(self, parameters):
        '''
        The GA Javascript client doesn't send any custom variables for
        e-commerce requests, so we don't either.
        '''
        return parameters
