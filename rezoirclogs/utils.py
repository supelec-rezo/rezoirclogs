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
    '''
    The log line informations are populated when the 'type' attribute is accessed.
    This way, LogLine is lazy and can be used as a normal string in other cases.
    '''
    def __new__(cls, value):
        return unicode.__new__(cls, convert_unknow_encoding(value))

    @reify
    def type(self):
        # Shamefully stolen from the old code. It's ugly.
        s = self.split(None, 2)

        if s[1][0] == '<': #Message
            self.time = s[0]
            self.user = s[1][1:-1]
            if len(s) == 3:
                self.message = s[2]
            else: #No message, so no split
                self.message = ""
            return 'normal'
        elif s[1] == '*': #/me
            s = self.split(None, 3)
            self.time = s[0]
            self.user = s[2]
            try:
                self.message = s[3]
            except IndexError:
                self.message = ''
            return 'me'
        elif s[1] == '-!-':
            s = self.split(None, 3)
            self.time = s[0]
            self.user = s[2]
            try:
                self.message = s[3]
            except IndexError:
                self.message = ''
            return 'status'

        else: #autre
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
