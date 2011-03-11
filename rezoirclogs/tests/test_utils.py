# -*- coding: utf-8 -*-
from rezoirclogs.tests.import_unittest import unittest


class ConvertUnknowEncodingTests(unittest.TestCase):
    def setUp(self):
        self.utf = 'p\xc3\xa2t\xc3\xa9'
        self.latin = 'p\xe2t\xe9'

    def test_utf8(self):
        from rezoirclogs.utils import convert_unknow_encoding
        self.assertEqual(self.utf, convert_unknow_encoding(self.utf))

    def test_latin(self):
        from rezoirclogs.utils import convert_unknow_encoding
        self.assertEqual(self.utf, convert_unknow_encoding(self.latin))


class ParseLogLineTests(unittest.TestCase):
    def test_normal(self):
        from rezoirclogs.utils import parse_log_line, NormalMessage
        line = "02:16 <ciblout> je suis secretaire, c'est moi qui décide"
        m = parse_log_line(line)
        self.assertIsInstance(m, NormalMessage)
        self.assertEqual(m.message, "je suis secretaire, c'est moi qui décide")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '02:16')
        self.assertEqual(m.text, line)

    def test_normal_empty(self):
        from rezoirclogs.utils import parse_log_line, NormalMessage
        m = parse_log_line("02:16 <ciblout>")
        self.assertIsInstance(m, NormalMessage)
        self.assertEqual(m.message, "")

    def test_me(self):
        from rezoirclogs.utils import parse_log_line, MeMessage
        line = "02:16  * ciblout dit encore des conneries"
        m = parse_log_line(line)
        self.assertIsInstance(m, MeMessage)
        self.assertEqual(m.message, "dit encore des conneries")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '02:16')
        self.assertEqual(m.text, line)

    def test_me_empty(self):
        from rezoirclogs.utils import parse_log_line, MeMessage
        m = parse_log_line("02:16  * ciblout")
        self.assertIsInstance(m, MeMessage)
        self.assertEqual(m.message, "")

    def test_status(self):
        from rezoirclogs.utils import parse_log_line, StatusMessage
        line = "01:56 -!- ciblout [cyprien@mauvaise.fois] has quit [Quit: Bon débaras.]"
        m = parse_log_line(line)
        self.assertIsInstance(m, StatusMessage)
        self.assertEqual(m.message, "[cyprien@mauvaise.fois] has quit [Quit: Bon débaras.]")
        self.assertEqual(m.user, 'ciblout')
        self.assertEqual(m.time, '01:56')
        self.assertEqual(m.text, line)

    def test_status_empty(self):
        from rezoirclogs.utils import parse_log_line, StatusMessage
        m = parse_log_line("01:56 -!- ciblout ")
        self.assertIsInstance(m, StatusMessage)
        self.assertEqual(m.message, "")

    def test_unrecognized(self):
        from rezoirclogs.utils import parse_log_line, UnrecognizedLine
        m = parse_log_line("Ceci n'est pas une ligne de log")
        self.assertIsInstance(m, UnrecognizedLine)
        self.assertEqual(m.text, "Ceci n'est pas une ligne de log")