# -*- coding: utf-8 -*-

from sys import stderr
import utils
from entities import CustomVariable
from requests import EventRequest, ItemRequest, PageViewRequest, SocialInteractionRequest, TransactionRequest


__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"


class Config(object):
    '''
    Configurations for Google Analytics: Server Side

    Properties:
    error_severity -- How strict should errors get handled? After all,
        we do just do some tracking stuff here, and errors shouldn't
        break an application's functionality in production.
        RECOMMENDATION: Exceptions during deveopment, warnings in production.
    queue_requests --  Whether to just queue all requests on HttpRequest.fire()
        and actually send them on shutdown after all other tasks are done.
        This has two advantages:
        1) It effectively doesn't affect app performance
        2) It can e.g. handle custom variables that were set after scheduling a request
    fire_and_forget -- Whether to make asynchronous requests to GA without
        waiting for any response (speeds up doing requests).
    logging_callback -- Logging callback, registered via setLoggingCallback().
        Will be fired whenever a request gets sent out and receives the
        full HTTP request as the first and the full HTTP response
        (or null if the "fireAndForget" option or simulation mode are used) as the 2nd argument.
    request_timeout -- Seconds (float allowed) to wait until timeout when
        connecting to the Google analytics endpoint host.
    endpoint -- Google Analytics tracking request endpoint. Can be set to null to
        silently simulate (and log) requests without actually sending them.
    anonimize_ip_address -- Whether to anonymize IP addresses within Google Analytics
        by stripping the last IP address block, will be mapped to "aip" parameter.
    site_speed_sample_rate -- Defines a new sample set size (0-100) for
        Site Speed data collection. By default, a fixed 1% sampling of your site
        visitors make up the data pool from which the Site Speed metrics are derived.

    '''
    ERROR_SEVERITY_SILECE = 0
    ERROR_SEVERITY_PRINT = 1
    ERROR_SEVERITY_RAISE = 2

    def __init__(self):
        self.error_severity = Config.ERROR_SEVERITY_RAISE
        self.queue_requests = False
        self.fire_and_forget = False
        self.logging_callback = False
        self.request_timeout = 1
        self.endpoint = 'www.google-analytics.com/__utm.gif'
        self.anonimize_ip_address = False
        self.site_speed_sample_rate = 1

    def __setattr__(self, name, value):
        if name == 'site_speed_sample_rate':
            if value and (value < 0 or value >100):
                raise Exception('For consistency with ga.js, sample rates must be specified as a number between 0 and 100.')
        object.__setattr__(self, name, value)


class Parameters(object):
    '''
    This simple class is mainly meant to be a well-documented overview
    of all possible GA tracking parameters.

    http://code.google.com/apis/analytics/docs/tracking/gaTrackingTroubleshooting.html#gifParameters

    General Parameters:
    utmwv -- Google Analytics client version
    utmac -- Google Analytics account ID
    utmhn -- Host Name
    utmt -- Indicates the type of request, which is one of null (for page),
            "event", "tran", "item", "social", "var" (deprecated) or "error"
            (used by ga.js for internal client error logging).
    utms -- Contains the amount of requests done in this session. Added in ga.js v4.9.2.
    utmn -- Unique ID (random number) generated for each GIF request
    utmcc -- Contains all cookie values, see below
    utme -- Extensible Parameter, used for events and custom variables
    utmni -- Event "non-interaction" parameter. By default, the event hit will impact a visitor's bounce rate.
             By setting this parameter to 1, this event hit will not be used in bounce rate calculations.
    aip -- Whether to anonymize IP addresses within Google Analytics by stripping the last IP address block, either null or 1
    utmu --  Used for GA-internal statistical client function usage and error tracking,
             not implemented in php-ga as of now, but here for documentation completeness.
             http://glucik.blogspot.com/2011/02/utmu-google-analytics-request-parameter.html

    Page Parameters:
    utmp -- Page request URI
    utmdt -- Page title
    utmcs -- Charset encoding (default "-")
    utmr -- Referer URL (default "-" or "0" for internal purposes)

    Visitor Parameters:
    utmip -- IP Address of the end user, found in GA for Mobile examples, but sadly seems to be ignored in normal GA use
    utmul -- Visitor's locale string (all lower-case, country part optional)
    utmfl -- Visitor's Flash version (default "-")
    utmje -- Visitor's Java support, either 0 or 1 (default "-")
    utmsc -- Visitor's screen color depth
    utmsr -- Visitor's screen resolution
    _utma -- Visitor tracking cookie parameter.

    Session Parameters:
    utmhid -- Hit id for revenue per page tracking for AdSense, a random per-session ID
    _utmb -- Session timeout cookie parameter.
    _utmc -- Session tracking cookie parameter.
    utmipc -- Product Code. This is the sku code for a given product.
    utmipn -- Product Name
    utmipr -- Unit Price. Value is set to numbers only.
    utmiqt -- Unit Quantity.
    utmiva -- Variations on an item.
    utmtid -- Order ID.
    utmtst -- Affiliation
    utmtto -- Total Cost
    utmttx -- Tax Cost
    utmtsp -- Shipping Cost
    utmtci -- Billing City
    utmtrg -- Billing Region
    utmtco -- Billing Country

    Campaign Parameters:
    utmcn -- Starts a new campaign session. Either utmcn or utmcr is present on any given request,
             but never both at the same time. Changes the campaign tracking data;
             but does not start a new session. Either 1 or not set.
             Found in gaforflash but not in ga.js, so we do not use it,
             but it will stay here for documentation completeness.
    utmcr -- Indicates a repeat campaign visit. This is set when any subsequent clicks occur on the
             same link. Either utmcn or utmcr is present on any given request,
             but never both at the same time. Either 1 or not set.
             Found in gaforflash but not in ga.js, so we do not use it,
             but it will stay here for documentation completeness.
    utmcid -- Campaign ID, a.k.a. "utm_id" query parameter for ga.js
    utmcsr -- Source, a.k.a. "utm_source" query parameter for ga.js
    utmgclid -- Google AdWords Click ID, a.k.a. "gclid" query parameter for ga.js
    utmdclid -- Not known for sure, but expected to be a DoubleClick Ad Click ID.
    utmccn -- Name, a.k.a. "utm_campaign" query parameter for ga.js
    utmcmd -- Medium, a.k.a. "utm_medium" query parameter for ga.js
    utmctr -- Terms/Keywords, a.k.a. "utm_term" query parameter for ga.js
    utmcct -- Ad Content Description, a.k.a. "utm_content" query parameter for ga.js
    utmcvr -- Unknown so far. Found in ga.js.
    _utmz -- Campaign tracking cookie parameter.

    Social Tracking Parameters:
    utmsn -- The network on which the action occurs
    utmsa -- The type of action that happens
    utmsid -- The page URL from which the action occurred.

    Google Website Optimizer (GWO) parameters:
    _utmx -- Website Optimizer cookie parameter.

    Custom Variables parameters (deprecated):
    _utmv -- Deprecated custom variables cookie parameter.

    '''

    def __init__(self):
        # General Parameters
        self.utmwv = Tracker.VERSION
        self.utmac = None
        self.utmhn = None
        self.utmt = None
        self.utms = None
        self.utmn = None
        self.utmcc = None
        self.utme = None
        self.utmni = None
        self.aip = None
        self.utmu = None

        # Page Parameters
        self.utmp = None
        self.utmdt = None
        self.utmcs = '-'
        self.utmr = '-'

        # Visitor Parameters
        self.utmip = None
        self.utmul = None
        self.utmfl = '-'
        self.utmje = '-'
        self.utmsc = None
        self.utmsr = None
        '''
        Visitor tracking cookie __utma

         This cookie is typically written to the browser upon the first
         visit to your site from that web browser. If the cookie has been
         deleted by the browser operator, and the browser subsequently
         visits your site, a new __utma cookie is written with a different unique ID.

         This cookie is used to determine unique visitors to your site and
         it is updated with each page view. Additionally, this cookie is
         provided with a unique ID that Google Analytics uses to ensure both the
         validity and accessibility of the cookie as an extra security measure.

        Expiration: 2 years from set/update.
        Format: __utma=<domainHash>.<uniqueId>.<firstTime>.<lastTime>.<currentTime>.<sessionCount>
        '''
        self._utma = None

        # Session Parameters
        self.utmhid = None
        '''
        Session timeout cookie parameter __utmb

        Will never be sent with requests, but stays here for documentation completeness.

        This cookie is used to establish and continue a user session with your site.
        When a user views a page on your site, the Google Analytics code attempts to update this cookie.
        If it does not find the cookie, a new one is written and a new session is established.

        Each time a user visits a different page on your site, this cookie is updated to expire in 30 minutes,
        thus continuing a single session for as long as user activity continues within 30-minute intervals.

        This cookie expires when a user pauses on a page on your site for longer than 30 minutes.
        You can modify the default length of a user session with the setSessionTimeout() method.

        Expiration: 30 minutes from set/update.

        Format: __utmb=<domainHash>.<trackCount>.<token>.<lastTime>

        '''
        self._utmb = None
        '''
        Session tracking cookie parameter __utmc

        Will never be sent with requests, but stays here for documentation completeness.

        This cookie operates in conjunction with the __utmb cookie to
        determine whether or not to establish a new session for the user.
        In particular, this cookie is not provided with an expiration date,
        so it expires when the user exits the browser.

        Should a user visit your site, exit the browser and then return to your website within 30 minutes,
        the absence of the __utmc cookie indicates that a new session needs to be established,
        despite the fact that the __utmb cookie has not yet expired.

        Expiration: Not set.

        Format: __utmc=<domainHash>

        '''
        self._utmc = None
        self.utmipc = None
        self.utmipn = None
        self.utmipr = None
        self.utmiqt = None
        self.utmiva = None
        self.utmtid = None
        self.utmtst = None
        self.utmtto = None
        self.utmttx = None
        self.utmtsp = None
        self.utmtci = None
        self.utmtrg = None
        self.utmtco = None

        # Campaign Parameters
        self.utmcn = None
        self.utmcr = None
        self.utmcid = None
        self.utmcsr = None
        self.utmgclid = None
        self.utmdclid = None
        self.utmccn = None
        self.utmcmd = None
        self.utmctr = None
        self.utmcct = None
        self.utmcvr = None
        '''
        Campaign tracking cookie parameter.

        This cookie stores the type of referral used by the visitor to reach your site,
        whether via a direct method, a referring link, a website search, or a campaign such as an ad or an email link.

        It is used to calculate search engine traffic, ad campaigns and page navigation within your own site.
        The cookie is updated with each page view to your site.

        Expiration: 6 months from set/update.

        Format: __utmz=<domainHash>.<campaignCreation>.<campaignSessions>.<responseCount>.<campaignTracking>

        '''
        self._utmz = None

        # Social Tracking Parameters
        self.utmsn = None
        self.utmsa = None
        self.utmsid = None

        # Google Website Optimizer (GWO) parameters
        '''
        Website Optimizer cookie parameter.

        This cookie is used by Website Optimizer and only set when Website
        Optimizer is used in combination with GA.
        See the Google Website Optimizer Help Center for details.

        Expiration: 2 years from set/update.
        '''
        self._utmx = None

        # Custom Variables parameters (deprecated)
        '''
        Deprecated custom variables cookie parameter.

        This cookie parameter is no longer relevant as of migration from setVar() to
        setCustomVar() and hence not supported by this library,
        but will stay here for documentation completeness.

        The __utmv cookie passes the information provided via the setVar() method,
        which you use to create a custom user segment.

        Expiration: 2 years from set/update.

        Format: __utmv=<domainHash>.<value>

        '''
        self._utmv = None

    def get_parameters(self):
        '''
        Get all gif request parameters out of the class in a dict form.
        Attributes starting with _ are cookie names, so we dont need them.
        '''
        params = {}
        attribs = vars(self)
        for attr in attribs:
            if attr[0] != '_':
                params[attr] = getattr(self, attr)

        return params


class Tracker(object):
    '''
    Act like a Manager of all files

    Properties:
    account_id -- Google Analytics account ID, will be mapped to "utmac" parameter
    domain_name -- Host Name, will be mapped to "utmhn" parameter
    allow_hash --  Whether to generate a unique domain hash,
                   default is true to be consistent with the GA Javascript Client
    custom_variables -- CustomVariable instances
    campaign -- Campaign instance
    '''

    '''
    Google Analytics client version on which this library is built upon,
    will be mapped to "utmwv" parameter.

    This doesn't necessarily mean that all features of the corresponding
    ga.js version are implemented but rather that the requests comply
    with these of ga.js.

    http://code.google.com/apis/analytics/docs/gaJS/changelog.html
    '''
    VERSION = '5.2.5' # As of 25.02.2012
    config = Config()

    def __init__(self, account_id='', domain_name='', conf=None):
        self.account_id = account_id
        self.domain_name = domain_name
        self.allow_hash = True
        self.custom_variables = {}
        self.campaign = None
        if isinstance(conf, Config):
            Tracker.config = conf

    def __setattr__(self, name, value):
        if name == 'account_id':
            if value and not utils.is_valid_google_account(value):
                raise Exception('Given Google Analytics account ID is not valid')

        elif name == 'campaign':
            if isinstance(value, Campaign):
                value.validate()
            else:
                value = None

        object.__setattr__(self, name, value)

    def add_custom_variable(self, custom_var):
        '''
        Equivalent of _setCustomVar() in GA Javascript client
        http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html
        '''
        if not isinstance(custom_var, CustomVariable):
            return

        custom_var.validate()
        index = custom_var.index
        self.custom_variables[index] = custom_var

    def remove_custom_variable(self, index):
        '''Equivalent of _deleteCustomVar() in GA Javascript client.'''
        if self.custom_variables.has_key(index):
            del self.custom_variables[index]

    def track_pageview(self, page, session, visitor):
        '''Equivalent of _trackPageview() in GA Javascript client.'''
        params = {
            'config': self.config,
            'tracker': self,
            'visitor': visitor,
            'session': session,
            'page': page,
        }
        request = PageViewRequest(**params)
        request.fire()

    def track_event(self, event, session, visitor):
        '''Equivalent of _trackEvent() in GA Javascript client.'''
        event.validate()

        params = {
            'config': self.config,
            'tracker': self,
            'visitor': visitor,
            'session': session,
            'event': event,
        }
        request = EventRequest(**params)
        request.fire()

    def track_transaction(self, transaction, session, visitor):
        '''Combines _addTrans(), _addItem() (indirectly) and _trackTrans() of GA Javascript client.'''
        transaction.validate()

        params = {
            'config': self.config,
            'tracker': self,
            'visitor': visitor,
            'session': session,
            'transaction': transaction,
        }
        request = TransactionRequest(**params)
        request.fire()

        for item in transaction.items:
            item.validate()

            params = {
                'config': self.config,
                'tracker': self,
                'visitor': visitor,
                'session': session,
                'item': item,
            }
            request = ItemRequest(**params)
            request.fire()


    def track_social(self, social_interaction, page, session, visitor):
        '''Equivalent of _trackSocial() in GA Javascript client.'''
        params = {
            'config': self.config,
            'tracker': self,
            'visitor': visitor,
            'session': session,
            'social_interaction': social_interaction,
            'page': page,
        }
        request = SocialInteractionRequest(**params)
        request.fire()


    def _raise_error(self, message):
        error_severity = self.config.error_severity
        if error_severity ==  Tracker.ERROR_SEVERITY_SILECE:
            # TODO: Log
        if error_severity == Tracker.ERROR_SEVERITY_LOG:
            # TODO: Log
            stderr.write(message)
            stderr.flush()
        elif error_severity == Tracker.ERROR_SEVERITY_RAISE:
            # TODO: Log
            raise Exception(message)
        else:
            # TODO: Log
            pass


class X10(object):
    __KEY = 'k'
    __VALUE = 'v'
    __DELIM_BEGIN = '('
    __DELIM_END = ')'
    __DELIM_SET = '*'
    __DELIM_NUM_VALUE = '!'
    __ESCAPE_CHAR_MAP = {
        "'": "'0",
        ')': "'1",
        '*': "'2",
        '!': "'3",
    }
    __MINIMUM = 1

    OBJECT_KEY_NUM = 1
    TYPE_KEY_NUM = 2
    LABEL_KEY_NUM = 3
    VALUE_VALUE_NUM = 1

    def __init__(self):
        self.project_data = {}

    def has_project(self, project_id):
        return project_data.has_key(project_id)

    def set_key(self, project_id, num, value):
        self.__set_internal(project_id, X10.__KEY, num, vaue)

    def get_key(self, project_id, num):
        return self.__get_internal(project_id, X10.__KEY, num)

    def clear_key(self, project_id):
        self.__clear_internal(project_id, X10.__KEY)

    def set_value(self, project_id, num, value):
        self.__set_internal(project_id, X10.__VALUE, num, vaue)

    def get_value(self, project_id, num):
        return self.__get_internal(project_id, X10.__VALUE, num)

    def clear_value(self, project_id):
        self.__clear_internal(project_id, X10.__VALUE)

    def __set_internal(self, project_id, _type, num, value):
        '''Shared internal implementation for setting an X10 data type.'''
        if not self.project_data.has_key(project_id):
            self.project_data[project_id] = {}

        if not self.project_data[project_id].has_key(_type):
            self.project_data[project_id][_type] = {}

        self.project_data[project_id][_type][num] = value

    def __get_internal(self, project_id, _type, num):
        ''' Shared internal implementation for getting an X10 data type.'''
        if self.project_data.get(project_id, {}).get(_type, {}).has_key(num):
            return self.project_data[project_id][_type][num]
        return None

    def __clear_internal(self, project_id, _type):
        '''
        Shared internal implementation for clearing all X10 data
        of a type from a certain project.
        '''
        if self.project_data.has_key(project_id) and self.project_data[project_id].has_key(_type):
            del self.project_data[project_id][_type]

    def __escape_extensible_value(self, value):
        '''Escape X10 string values to remove ambiguity for special characters.'''
        def _translate(char):
            try:
                return e[char]
            except KeyError:
                return char

        return ''.join(map(_translate, str(value))

    def __render_data_type(self, data):
        '''Given a data array for a certain type, render its string encoding.'''
        result = []
        last_indx = 0

        for indx, entry in sorted(data.items()):
            if entry:
                tmpstr = ''

                # Check if we need to append the number. If the last number was
                # outputted, or if this is the assumed minimum, then we don't.
                if indx != X10.__MINIMUM and indx-1 != last_indx:
                    tmpstr = '%s%s%s' % (tmpstr, indx, X10.__DELIM_NUM_VALUE)

                tmpstr = '%s%s' % (tmpstr, self.__escape_extensible_value(entry))
                result.append(tmpstr)

            last_indx = indx

        return "%s%s%s" % (X10.__DELIM_BEGIN, X10.__DELIM_SET.join(result) ,X10.__DELIM_END)

    def __render_project(self, project):
        '''Given a project array, render its string encoding.'''
        result = ''
        need_type_qualifier =  False

        for val in X10.__KEY, X10.__VALUE:
            if project.has_key(val):
                data = project[val]
                if need_type_qualifier:
                    result = '%s%s' % (result, val)

                result = '%s%s'  % (result, self.__render_data_type(data))
                need_type_qualifier = False
            else:
                need_type_qualifier = True

        return result

    def render_url_string(self):
        result = ''
        for project_id, project in self.project_data:
            result = '%s%s%s' % (result, project_id, self.__render_project(project))

        return result
