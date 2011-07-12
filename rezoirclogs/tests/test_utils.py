# -*- coding: utf-8 -*-
import unittest2


class ConvertUnknowEncodingTests(unittest2.TestCase):
    def setUp(self):
        self.unicode = u'pâté'
        self.utf = 'p\xc3\xa2t\xc3\xa9'
        self.latin = 'p\xe2t\xe9'

    def test_utf8(self):
        from rezoirclogs.utils import convert_unknow_encoding
        self.assertEqual(self.unicode, convert_unknow_encoding(self.utf))

    def test_latin(self):
        from rezoirclogs.utils import convert_unknow_encoding
        self.assertEqual(self.unicode, convert_unknow_encoding(self.latin))


class ParseLogLineTests(unittest2.TestCase):
    def _get_FUT(self, *args, **kwargs):
        from rezoirclogs.utils import LogLine
        return LogLine(*args, **kwargs)

    def test_normal(self):
        line = "02:16 <ciblout> je suis secretaire, c'est moi qui decide"
        m = self._get_FUT(line)
        self.assertEqual(m.type, "normal")
        self.assertEqual(m.message, "je suis secretaire, c'est moi qui decide")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '02:16')
        self.assertEqual(str(m), line)

    def test_normal_empty(self):
        m = self._get_FUT("02:16 <ciblout>")
        self.assertEqual(m.type, "normal")
        self.assertEqual(m.message, "")

    def test_me(self):
        line = "02:16  * ciblout dit encore des conneries"
        m = self._get_FUT(line)
        self.assertEqual(m.type, "me")
        self.assertEqual(m.message, "dit encore des conneries")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '02:16')
        self.assertEqual(str(m), line)

    def test_me_empty(self):
        m = self._get_FUT("02:16  * ciblout")
        self.assertEqual(m.type, "me")
        self.assertEqual(m.message, "")

    def test_status(self):
        line = "01:56 -!- ciblout [cyprien@mauvaise.fois] has quit [Quit: Bon debaras.]"
        m = self._get_FUT(line)
        self.assertEqual(m.type, "status")
        self.assertEqual(m.message, "[cyprien@mauvaise.fois] has quit [Quit: Bon debaras.]")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '01:56')
        self.assertEqual(str(m), line)

    def test_status_empty(self):
        m = self._get_FUT("01:56 -!- ciblout ")
        self.assertEqual(m.type, "status")
        self.assertEqual(m.message, "")

    def test_unrecognized(self):
        m = self._get_FUT("Ceci n'est pas une ligne de log")
        self.assertEqual(m.type, "unrecognized")
        self.assertEqual(str(m), "Ceci n'est pas une ligne de log")


class ColorationTests(unittest2.TestCase):
    def test_colored(self):
        from jinja2 import Markup
        from rezoirclogs.utils import colored
        self.assertEqual(colored('madjar'), Markup(u'<span style="color:#3176B3">madjar</span>'))
