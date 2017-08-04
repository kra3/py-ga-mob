===================================================
PYGA: Python Google Analytics
===================================================
This is a fork of https://github.com/kra3/py-ga-mob

pyga is an iplementation of Google Analytics (ga.js) in Python;so that it can be used at server side.
This project only helps you with Data Collection part of Google Analytics.
ie., You can consider this as a replacement for ga.js at client side.

Google Provides Android SDK,iOS SDK + Flash SDK. 
And left everybody else with a single page documentation about GIF request parameters. 
Also with a basic sample of server side implementation in quite a few languages (perl, php, jsp).


Use Cases
--------------

1. You want to track data from server side
2. You're developing a mobile site and have to support devices w/o JS support


Supported Features    
----------------------

* Page View
* E-Commerce
* Social Interaction
* Custom Variables
* Events
* Campaigns

  not yet

* Ad-Words
* Search Engine



To know more about mobiletracking see:
https://developers.google.com/analytics/devguides/collection/other/mobileWebsites


Example
-------------------      
::

     from pyga.requests import Tracker, Page, Session, Visitor

     tracker = Tracker('MO-XXXXX-X', 'yourdomain.com')     
     visitor = Visitor()
     visitor.ip_address = '194.54.176.12'
     session = Session()
     page = Page('/path')
     tracker.track_pageview(page, session, visitor)
     
     
     


Thanks to: `Expicient Inc <http://www.expicient.com>`_

