from pyramid import testing
from webob.multidict import MultiDict
import unittest2


class DirectoryViewTests(unittest2.TestCase):
    def test_view(self):
        from rezoirclogs.views import directory
        ressource = object()
        request = None
        response = directory(ressource, request)
        self.assertEqual(ressource, response['dir'])


class ChanViewTests(unittest2.TestCase):
    def test_view(self):
        from rezoirclogs.views import chan
        ressource = object()
        request = None
        response = chan(ressource, request)
        self.assertEqual(ressource, response['chan'])


class LogFileTests(unittest2.TestCase):
    def _get_request(self):
        request = testing.DummyRequest()
        request.GET = MultiDict()
        return request

    def test_basic(self):
        from rezoirclogs.views import logfile
        context = DummyIterable([DummyObject() for i in range(3)])
        request = self._get_request()
        result = logfile(context, request)
        self.assertEqual(result['context'], context)
        self.assertListEqual(result['lines'], context.value)

    def test_anchor_link(self):
        from rezoirclogs.views import logfile
        line = DummyObject()
        line.time = 'outatime'
        context = DummyIterable([line])
        request = self._get_request()
        result = logfile(context, request)
        resulting_line = result['lines'][0]
        self.assertEqual(resulting_line.anchor, '0')
        self.assertEqual(resulting_line.anchorlink, 'http://example.com/?select=0#0')

    def test_range(self):
        from rezoirclogs.views import logfile
        context = DummyIterable([DummyObject() for i in range(10)])
        request = self._get_request()
        request.GET['range'] = '2-5'
        result = logfile(context, request)
        for i in xrange(2, 5):
            self.assertEqual(result['lines'][i].highlighted, True)

    def test_range_buggy_get(self):
        from rezoirclogs.views import logfile
        context = DummyIterable([DummyObject() for i in range(10)])
        request = self._get_request()
        request.GET.add('range', '10-15')
        request.GET.add('range', 'tagada')
        request.GET.add('range', '10-12-12')
        result = logfile(context, request)
        for obj in result['lines']:
            self.assertFalse(hasattr(obj, 'highlighted'))

    def test_select(self):
        from rezoirclogs.views import logfile
        context = DummyIterable([DummyObject() for i in range(10)])
        for d in context:
            d.time = 'notNone'
        request = self._get_request()
        request.GET.add('select', '2')
        result = logfile(context, request)
        self.assertEqual(result['lines'][5].anchorlink,
                         'http://example.com/?range=2-6#2')


class SearchTests(unittest2.TestCase):
    def test_search(self):
        from rezoirclogs.views import search
        obj = DummyObject()
        parent = DummyObject()
        parent.__name__ = ''
        obj.__parent__ = parent
        obj.__name__ = 'dummy'
        obj.date = ''
        obj.search = lambda x, y: [(obj, 42, DummyObject())]
        request = testing.DummyRequest()
        request.POST['query'] = 'lala'
        request.POST['search'] = True
        response = search(obj, request)
        self.assertEqual(len(response['results']), 1)
        self.assertEqual(response['results'][0].anchorlink,
                         'http://example.com/dummy/#42')
        self.assertEqual(response['query'], 'lala')

    def test_search_form_with_no_query(self):
        from rezoirclogs.views import search
        request = testing.DummyRequest()
        response = search(None, request)
        self.assertEqual(response['context'], None)
        self.assertIn('form', response)

    def test_search_form_with_invalid_query(self):
        from rezoirclogs.views import search
        request = testing.DummyRequest()
        request.POST['search'] = True
        response = search(None, request)
        self.assertEqual(response['context'], None)
        self.assertIn('form', response)


class DummyObject(object):
    type = ''
    time = None


class DummyIterable(object):
    __name__ = ''
    __parent__ = None

    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return iter(self.value)
