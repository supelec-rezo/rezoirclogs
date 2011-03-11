from pyramid.view import view_config
from pyramid.url import resource_url

from rezoirclogs.resources import Directory, Chan, LogFile
from rezoirclogs.utils import Message


@view_config(context=Directory, renderer='directory.jinja2')
def directory(context, request):
    return {'dir': context}


@view_config(context=Chan, renderer='chan.jinja2')
def chan(context, request):
    return {'chan': context}


@view_config(context=LogFile, renderer='logfile.jinja2')
def logfile(context, request):
    lines = list(context)
    for i, line in enumerate(lines):
        if hasattr(line, 'time'):
            line.anchor = '%s.%s'%(i, line.time)
            line.anchorlink = resource_url(context, request, anchor = line.anchor)
    return {'lines': lines, 'context': context}