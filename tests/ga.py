import unittest


class TestGA(unittest.TestCase):

    def test_request(self):
        from pyga.requests import Tracker, Visitor, Session, Page
        from mock import Mock
        import urllib2

        mocked = urllib2.urlopen = Mock()

        meta = dict(
            REMOTE_ADDR='134.321.0.1',
            HTTP_USER_AGENT='Test User Agent 1.0',
            HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.8,ru;q=0.6',
        )
        tracker = Tracker('UA-0000-0000', 'test.com')
        visitor = Visitor()
        visitor.extract_from_server_meta(meta)
        self.assertEqual(visitor.ip_address, '134.321.0.1')
        self.assertEqual(visitor.locale, 'en_US')
        self.assertEqual(visitor.user_agent, 'Test User Agent 1.0')
        session = Session()
        page = Page('/test_path')
        tracker.track_pageview(page, session, visitor)
        (request, ), _ = mocked.call_args_list.pop()
        self.assertEqual(request.headers.get('X-forwarded-for'), '134.321.0.1')
        self.assertEqual(request.headers.get('User-agent'), 'Test User Agent 1.0')
