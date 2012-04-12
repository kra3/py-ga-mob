# -*- coding: utf-8 -*-

from entities import Tracker

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"


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
