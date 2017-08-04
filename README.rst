===================================================
PYGA: Python Google Analytics
===================================================
This is a fork of https://github.com/kra3/py-ga-mob

Pyga is an implementation of Google Analytics (ga.js) in Python that can be used
at server side. This project only helps you with Data Collection part of Google
Analytics. You can consider this as a replacement for ga.js at client side.

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

