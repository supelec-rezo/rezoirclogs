
def convert_unknow_encoding(text):
    try:
        t = text.decode('utf-8')
    except UnicodeDecodeError:
        t = text.decode('latin-1')
    return t


class Line(object):
    text = ''


class UnrecognizedLine(Line):
    pass


class Message(Line):
    message = ''
    user = ''
    time = ''


class NormalMessage(Message):
    pass


class MeMessage(Message):
    pass


class StatusMessage(Message):
    pass


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
