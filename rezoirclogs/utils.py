from pyramid.decorator import reify
import re
from jinja2 import Markup

def convert_unknow_encoding(text):
    try:
        t = text.decode('utf-8')
    except UnicodeDecodeError:
        t = text.decode('latin-1')
    return t


class LogLine(unicode):
    """
    The log line informations are populated when the 'type' attribute is accessed.
    This way, LogLine is lazy and can be used as a normal string in other cases.
    """
    def __new__(cls, value):
        return unicode.__new__(cls, convert_unknow_encoding(value))

    _regex = [
        (re.compile(r"(\d\d:\d\d) <(\w*)> ?(.*)"), 'normal'),
        (re.compile(r"(\d\d:\d\d) *\* (\w*) ?(.*)"), 'me'),
        (re.compile(r"(\d\d:\d\d) -!- (\w*) ?(.*)"), 'status'),
        ]

    @reify
    def type(self):
        for r, type in LogLine._regex:
            m = r.match(self)
            if m:
                self.time, self.user, self.message = m.groups()
                return type
        return 'unrecognized'

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
