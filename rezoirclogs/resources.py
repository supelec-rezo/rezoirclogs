from functools import wraps
import itertools
import os
import datetime
import logging
from beaker.cache import cache_region
from rezoirclogs.utils import LogLine

log = logging.getLogger(__name__)

class Base(object):
    """Base resource object, useful for debugging"""
    __name__ = ''
    __parent__ = None

    def __repr__(self):
        return u'<%s: %s>' % (self.__class__.__name__, self.__name__)


def jailed(f):
    @wraps(f)
    def jailed_f(self, path):
        if path.startswith(self.root_path):
            return f(self, path)
    return jailed_f


class Filesystem(object):
    """Jailed wrapper around os.path"""
    def __init__(self, root_path):
        self.root_path = os.path.abspath(os.path.normpath(root_path))

    join = staticmethod(os.path.join)

    @cache_region('short_term')
    @jailed
    def listdir(self, path):
        log.debug('listdir %s', path)
        return os.listdir(path)

    @cache_region('short_term')
    @jailed
    def isrealfile(self, path):
        log.debug('isrealfile %s', path)
        return os.path.isfile(path) and not os.path.islink(path)

    @cache_region('short_term')
    @jailed
    def isrealdir(self, path):
        log.debug('isrealdir %s', path)
        return os.path.isdir(path) and not os.path.islink(path)

    def open(self, path):
        log.debug('open %s', path)
        return open(path)

    def __str__(self):
        return '<Filesystem jailed in %s'% self.root_path


class LogFile(Base):
    def __init__(self, filesystem, path, date):
        self.fs = filesystem
        self.path = os.path.abspath(os.path.normpath(path))
        self.date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))

    def __iter__(self):
        for line in self.fs.open(self.path):
            yield LogLine(line)

    def neighbour(self, n):
        wanted = self.date + datetime.timedelta(days=n)
        wanted = wanted.strftime('%Y%m%d')
        try:
            return self.__parent__[wanted]
        except KeyError:
            return

    @property
    def previous(self):
        return self.neighbour(-1)

    @property
    def next(self):
        return self.neighbour(1)

    def search(self, query, after_date=None):
        if after_date and after_date > self.date:
            return
        for num, line in enumerate(self):
            if query in line:
                yield (self, num, line)


class Chan(Base):
    def __init__(self, filesystem, path, name):
        self.fs = filesystem
        self.path = os.path.abspath(os.path.normpath(path))
        self.name = name

    def _make_logfile(self, path, date):
        l = LogFile(self.fs, path, date)
        l.__name__ = date
        l.__parent__ = self
        return l

    def __getitem__(self, date):
        name = '%s.%s.log' % (self.name, date)
        nextpath = self.fs.join(self.path, name)
        if self.fs.isrealfile(nextpath):
            return self._make_logfile(nextpath, date)
        raise KeyError(date)

    def __iter__(self):
        for name in sorted(self.fs.listdir(self.path)):
            if name.startswith(self.name):
                path = self.fs.join(self.path, name)
                if self.fs.isrealfile(path):
                    date = name.rsplit('.', 2)[1]
                    yield self._make_logfile(path, date)

    def last(self, n):
        return list(self)[:-n-1:-1]

    def search(self, query, after_date=None):
        for logfile in self:
            for result in logfile.search(query, after_date):
                yield result


class Directory(Base):
    def __init__(self, filesystem, path):
        self.fs = filesystem
        self.path = os.path.abspath(os.path.normpath(path))

    def _make_dir(self, name):
        d = Directory(self.fs, self.fs.join(self.path, name))
        d.__name__ = name
        d.__parent__ = self
        return d

    def _make_chan(self, chan):
        c = Chan(self.fs, self.path, chan)
        c.__name__ = chan
        c.__parent__ = self
        return c

    def __getitem__(self, name):
        nextpath = self.fs.join(self.path, name)
        if self.fs.isrealdir(nextpath):
            return self._make_dir(name)
        elif any(file.startswith(name) and file.endswith('.log') and self.fs.isrealfile(self.fs.join(self.path, file)) for file in self.fs.listdir(self.path)):
            return self._make_chan(name)
        else:
            raise KeyError(name)

    @property
    def dirs(self):
        for name in sorted(self.fs.listdir(self.path)):
            path = self.fs.join(self.path, name)
            if self.fs.isrealdir(path):
                yield self._make_dir(name)

    @property
    def chans(self):
        files = (name for name in sorted(self.fs.listdir(self.path))
                 if self.fs.isrealfile(self.fs.join(self.path, name)) and name.endswith('.log'))

        for chan in set(name.rsplit('.', 2)[0] for name in files):
            yield self._make_chan(chan)

    def __iter__(self):
        return self.dirs

    def search(self, query, after_date=None):
        for sub in itertools.chain(self.dirs, self.chans):
            for result in sub.search(query, after_date):
                yield result
