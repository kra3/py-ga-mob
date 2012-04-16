# -*- coding: utf-8 -*-

import calendar
from math import floor
from base import Config, Parameters, Tracker, X10
from entities import Campaign, CustomVariable, Event, Item, Page, Session, SocialInteraction, Transaction, Visitor
import urllib
import urllib2
import utils

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
        query_string = urllib.urlencode(params.get_parameters())
        query_string = query_string.replace('+', '%20')

        # Mimic Javascript's encodeURIComponent() encoding for the query
        # string just to be sure we are 100% consistent with GA's Javascript client
        query_string = utils.convert_to_uri_component_encoding(query_string)

        # Recent versions of ga.js use HTTP POST requests if the query string is too long
        use_post = len(query_string) > 2036

        if not use_post:
            url = '%s?%s' % (self.config.endpoint, query_string)
            post = None
        else:
            url = self.config.endpoint
            post = query_string

        headers = []
        headers['Host'] = self.config.endpoint.split('/')[0]
        headers['User-Agent'] = self.user_agent
        headers['X-Forwarded-For'] = self.x_forwarded_for

        if use_post:
            # Don't ask me why "text/plain", but ga.js says so :)
            headers['Content-Type'] = 'text/plain'
            headers['Content-Length'] = len(query_string)

        headers['Connection'] = 'close'
        return urllib2.Request(url, post, headers)

    def build_parameters(self):
        '''Marker implementation'''
        return Parameters()

    def __send(self):
        request =  self.build_http_request()
        response = None

        #  Do not actually send the request if endpoint host is set to null
        if self.config.endpoint:
            response = urllib2.urlopen(request, timeout=self.config.request_timeout)

        return response

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

    def get_type(self):
        return ''

    def build_http_request(self):
        self.x_forwarded_for = self.visitor.ip_address
        self.user_agent = self.visitor.user_agent

        # Increment session track counter for each request
        self.session.track_count = self.session.track_count + 1

        #http://code.google.com/intl/de-DE/apis/analytics/docs/tracking/eventTrackerGuide.html#implementationConsiderations
        if self.session.track_count > 500:
            raise Exception('Google Analytics does not guarantee to process more than 500 requests per session.')

        if self.tracker.campaign:
            self.tracker.campaign.response_count = self.tracker.campaign.response_count + 1

        return super(Request, self).build_http_request()

    def build_parameters(self):
        params = Parameters()
        params.utmac = self.tracker.account_id
        params.utmhn = self.tracker.domain_name
        params.utmt = self.get_type()
        params.utmn = utils.get_32bit_random_num()
        '''
        The "utmip" parameter is only relevant if a mobile analytics ID
        (MO-XXXXXX-X) was given
        '''
        params.utmip = self.visitor.ip_address
        params.aip = self.tracker.config.anonimize_ip_address and 1 or None
        if params.aip:
            # If anonimization of ip enabled? then!
            params.utmip = utils.anonymize_ip(params.utmip)

        params.utmhid = self.session.session_id
        params.utms = self.self.session.track_count
        params = self.build_visitor_parameters(params)
        params = self.build_custom_variable_parameters(params)
        params = self.build_campaign_parameters(params)
        params = self.build_cookie_parameters(params)
        return params

    def build_visitor_parameters(self, params):
        params.utml = self.visitor.locale.replace('_', '-').lower()

        if self.visitor.flash_version:
            params.utmfl = self.visitor.flash_version

        if self.visitor.java_enabled:
            params.utje = self.visitor.java_enabled

        if self.visitor.screen_colour_depth:
            params.utmsc = '%s-bit' % (self.visitor.screen_colour_depth)

        if self.visitor.screen_resolution:
            params.utmsr = self.visitor.screen_resolution

        return params

    def build_custom_variable_parameters(self, params):
        custom_vars = self.tracker.custom_variables

        if custom_vars:
            if len(custom_vars) > 5:
                raise Exception('The sum of all custom variables cannot exceed 5 in any given request.')

            x10 = X10()
            x10.clear_key(self.X10_CUSTOMVAR_NAME_PROJECT_ID)
            x10.clear_key(self.X10_CUSTOMVAR_VALUE_PROJCT_ID)
            x10.clear_key(self.X10_CUSTOMVAR_SCOPE_PROJECT_ID)

            for cvar in custom_vars.itervalues():
                name = utils.encode_uri_components(cvar.name)
                value = utils.encode_uri_components(cvar.value)
                x10.set_key(self.X10_CUSTOMVAR_NAME_PROJECT_ID, cvar.index, name)
                x10.set_key(self.X10_CUSTOMVAR_VALUE_PROJCT_ID, cvar.index, value)

                if cvar.scope and cvar.scope != CustomVariable.SCOPE_PAGE:
                    x10.set_key(self.X10_CUSTOMVAR_SCOPE_PROJECT_ID, cvar.index, cvar.scope)

            params.utme = '%s%s' % (params.utme, x10.render_url_string())

        return params

    def build_campaign_parameters(self, params):
        campaign = self.tracker.campaign
        if campaign:
            params._utmz = '%s.%s.%s.%s.' % (
                    self._generate_domain_hash(),
                    calendar.timegm(campaign.creation_time.utctimetuple()),
                    self.visitor.visit_count,
                    campaign.response_count,
                )

            param_map = {
                'utmcid': campaign.id,
                'utmcsr': campaign.source,
                'utmgclid': campaign.g_click_id,
                'utmdclid': campaign.d_click_id,
                'utmccn': campaign.name,
                'utmcmd': campaign.medium,
                'utmctr': campaign.term,
                'utmcct': campaign.content,
            }

            for k, v in param_map:
                if v:
                    # Only spaces and pluses get escaped in gaforflash and ga.js, so we do the same
                    params._utmz = '%s%s=%s%s' % (params._utmz, k,
                            v.replace('+', '%20').replace(' ', '%20'),
                            Campaign.CAMPAIGN_DELIMITER
                        )

            params._utmz = params._utmz.rstrip(Campaign.CAMPAIGN_DELIMITER)

        return params

    def build_cookie_parameters(self, params):
        domain_hash = self._generate_domain_hash()
        params._utma = "%s.%s.%s.%s.%s.%s" % (
                domain_hash,
                self.visitor.unique_id,
                calendar.timegm(self.visitor.first_visit_time.utctimetuple()),
                calendar.timegm(self.visitor.previous_visit_time.utctimetuple()),
                calendar.timegm(self.visitor.current_visit_time.utctimetuple()),
                self.visitor.visit_count
            )
        params._utmb = '%s.%s.10.%s' % (
                domain_hash,
                self.session.track_count,
                calendar.timegm(self.session.start_time.utctimetuple()),
            )
        params._utmc = domain_hash
        cookies = []
        cookies.append('__utma=%s;' % params._utma)
        if params._utmz:
            cookies.append('__utmz=%s;' % params._utmz)
        if params._utmv:
            cookies.append('__utmv=%s;' % params._utmv)

        params.utmcc = '+'.join(cookies)
        return params

    def _generate_domain_hash(self):
        hash_val = 1
        if self.tracker.allow_hash:
            hash_val = utils.generate_hash(self.tracker.domain_name)

        return hash_val


class ItemRequest(Request):
    def __init__(self, config, tracker, visitor, session, item):
        super(ItemRequest, self).__init__(config, tracker, visitor, session)
        self.item = item

    def get_type(self):
        ItemRequest.TYPE_ITEM

    def build_parameters(self):
        params = super(ItemRequest, self).build_parameters()
        params.utmtid = self.item.order_id
        params.utmipc = self.item.sku
        params.utmipn = self.item.name
        params.utmiva = self.item.variation
        params.utmipr = self.item.price
        params.utmiqt = self.item.quantity
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
        params.utmp = self.page.path
        params.utmdt = self.page.title

        if self.page.charset:
            params.utmcs = self.page.charset

        if self.page.referrer:
            params.utmr = self.page.referrer

        if self.page.load_time:
            if params.utmn % 100 <  self.config.site_speed_sample_rate:
                x10 = X10()
                x10.clear_key(self.X10_SITESPEED_PROJECT_ID)
                x10.clear_value(self.X10_SITESPEED_PROJECT_ID)

                # from ga.js
                key = max(min(floor(self.page.load_time / 100), 5000), 0) * 100
                x10.set_key(self.X10_SITESPEED_PROJECT_ID, X10.OBJECT_KEY_NUM, key)
                x10.set_value(self.X10_SITESPEED_PROJECT_ID, X10.VALUE_VALUE_NUM, self.page.load_time)
                params.utme = '%s%s' % (params.utme, x10.render_url_string())

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

        params.utme = "%s%s" % (params.utme, x10.render_url_string())

        if self.event.noninteraction:
            params.utmni = 1

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

        params.utmsn = self.social_interaction.network
        params.utmsa = self.social_interaction.action
        params.utmsid = tmppagepath
        return params


class TransactionRequest(Request):
    def __init__(self, config, tracker, visitor, session, transaction):
        super(TransactionRequest, self).__init__(config, tracker, visitor, session)
        self.transaction =  transaction

    def get_type(self):
        TransactionRequest.TYPE_TRANSACTION

    def build_parameters(self):
        params = super(TransactionRequest, self).build_parameters()
        params.utmtid = self.transaction.order_id
        params.utmtst = self.transaction.affiliation
        params.utmtto = self.transaction.total
        params.utmttx = self.transaction.tax
        params.utmtsp = self.transaction.shipping
        params.utmtci = self.transaction.city
        params.utmtrg = self.transaction.state
        params.utmtco = self.transaction.country
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
