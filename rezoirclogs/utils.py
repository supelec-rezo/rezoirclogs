import re
from jinja2 import Markup

def convert_unknow_encoding(text):
    try:
        t = text.decode('utf-8')
    except UnicodeDecodeError:
        t = text.decode('latin-1')
    return t


class Line(object):
    type = 'line'
    text = ''


class UnrecognizedLine(Line):
    type = 'unrecognized'


class Message(Line):
    type = 'message'
    message = ''
    user = ''
    time = ''


class NormalMessage(Message):
    type = 'normal'


class MeMessage(Message):
    type = 'me'


class StatusMessage(Message):
    type = 'status'


def parse_log_line(line):
    # Shamefully stolen from the old code. It's ugly.
    line = convert_unknow_encoding(line)
    s = line.split(None, 2)

    if s[1][0] == '<': #Message
        m = NormalMessage()
        m.time = s[0]
        m.user = s[1][1:-1]
        if len(s) == 3:
            m.message = s[2]
        else: #No message, so no split
            m.message = ""
    elif s[1] == '*': #/me
        m = MeMessage()
        s = line.split(None, 3)
        m.time = s[0]
        m.user = s[2]
        try:
            m.message = s[3]
        except IndexError:
            m.message = ''
    elif s[1] == '-!-':
        m = StatusMessage()
        s = line.split(None, 3)
        m.time = s[0]
        m.user = s[2]
        try:
            m.message = s[3]
        except IndexError:
            m.message = ''

    else: #autre
        m = UnrecognizedLine()
    m.text = line
    return m


class ColorPool(object):
    colors = [ "#E90C82", "#8E55E9", "#B30E0E", "#16B338", "#58B0B3", "#9D54B3", "#B39675", "#3176B3"]
    def __init__(self):
        self.nicks = {}

    def get_magic_number(self, nick):
        sum = 0
        for letter in nick:
            sum += ord(letter)
        return sum%len(self.colors)

    def get_color(self, nick):
        if not self.nicks.has_key(nick):
            self.nicks[nick] = self.colors[self.get_magic_number(nick)]
        return self.nicks[nick]

_colorPool = ColorPool()

def colored(nick):
    color = _colorPool.get_color(nick)
    return Markup('<span style="color:%s">%s</span>')%(color, nick)

_url_pattern = [
        (re.compile(r"(\b(http|https|ftp)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"),
         Markup(r'<a href="%(url)s">%(url)s</a>')),
        (re.compile(r"((^|\b)www\.([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"),
         Markup(r'<a href="http://%(url)s">%(url)s</a>'))
]
