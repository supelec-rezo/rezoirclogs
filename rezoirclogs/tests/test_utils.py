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
        lines = [("02:16 <ciblout> je suis secretaire, c'est moi qui decide", "normal", "je suis secretaire, c'est moi qui decide", 'ciblout', '02:16'),
                 ("02:16:45 <ciblout> je suis secretaire, c'est moi qui decide", "normal", "je suis secretaire, c'est moi qui decide", 'ciblout', '02:16:45')]
        for line, expected_type, expected_message, expected_nick, expected_time in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, expected_type)
            self.assertEqual(m.message, expected_message)
            self.assertEqual(m.user, expected_nick)
            self.assertEqual(m.time, expected_time)
            self.assertEqual(str(m), line)

    def test_normal_empty(self):
        lines = ["02:16 <ciblout>",
                 "02:16:45 <ciblout>"]
        for line in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, "normal")
            self.assertEqual(m.message, "")

    def test_me(self):
        lines = [("02:16  * ciblout dit encore des conneries", "me", "dit encore des conneries", 'ciblout', '02:16'),
                 ("02:16:45  * ciblout dit encore des conneries", "me", "dit encore des conneries", 'ciblout', '02:16:45')]
        for line, expected_type, expected_message, expected_nick, expected_time in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, expected_type)
            self.assertEqual(m.message, expected_message)
            self.assertEqual(m.user, expected_nick)
            self.assertEqual(m.time, expected_time)
            self.assertEqual(str(m), line)

    def test_me_empty(self):
        lines = ["02:16  * ciblout",
                 "02:16:45  * ciblout"]
        for line in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, "me")
            self.assertEqual(m.message, "")

    def test_status(self):
        lines = [("01:56 -!- ciblout [cyprien@mauvaise.foi] has quit [Quit: Bon debaras.]", "status", "[cyprien@mauvaise.foi] has quit [Quit: Bon debaras.]", 'ciblout', '01:56'),
                 ("01:56:09 -!- ciblout [cyprien@mauvaise.foi] has quit [Quit: Bon debaras.]", "status", "[cyprien@mauvaise.foi] has quit [Quit: Bon debaras.]", 'ciblout', '01:56:09')]
        for line, expected_type, expected_message, expected_nick, expected_time in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, expected_type)
            self.assertEqual(m.message, expected_message)
            self.assertEqual(m.user, expected_nick)
            self.assertEqual(m.time, expected_time)
            self.assertEqual(str(m), line)

    def test_status_empty(self):
        lines = ["02:16 -!- ciblout",
                 "02:16:45 -!- ciblout"]
        for line in lines:
            m = self._get_FUT(line)
            self.assertEqual(m.type, "status")
            self.assertEqual(m.message, "")

    def test_unrecognized(self):
        m = self._get_FUT("Ceci n'est pas une ligne de log")
        self.assertEqual(m.type, "unrecognized")
        self.assertEqual(str(m), "Ceci n'est pas une ligne de log")

    def test_exotic_nicknames(self):
        lines = [("20:26 <K-Yo> madjar, \o/", "K-Yo"),
            ("22:14 <+K-Yo> putain, j'ai la même!", "K-Yo"),
            ("22:14 <@DaLynX> merci remram", "DaLynX"),
            ("04:54 <@Zertr1> derns!", "Zertr1"),
            ("04:54:00 <@Zertr1> derns!", "Zertr1"),
            ("01:59 < kage> c'est moche les GUI en java", "kage"),
            ("11:59 <~kage> c'est moche les GUI en java", "kage"),
            ("01:59 <&kage> c'est moche les GUI en java", "kage")]

        for line, nick in lines:
            self.assertEqual(self._get_FUT(line).user, nick, line)


class ColorationTests(unittest2.TestCase):
    def test_colored(self):
        from jinja2 import Markup
        from rezoirclogs.utils import colored
        self.assertEqual(colored('madjar'), Markup(u'<span style="color:#3176B3">madjar</span>'))
