from pyramid.view import view_config
from pyramid.url import resource_url

from rezoirclogs.resources import Directory, Chan, LogFile


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
        line.type # to force the computation
        if hasattr(line, 'time'):
            line.anchor = '%s' % i
            line.anchorlink = resource_url(context, request, anchor = line.anchor)

    for rang in request.GET.getall('range'):
        try:
            fro, to = map(int, rang.split('-'))
            for i in range(fro, to):
                lines[i].highlighted = True
        except ValueError:
            pass
        except IndexError:
            pass

    return {'lines': lines, 'context': context}


@view_config(name='search', renderer='search.jinja2')
def search(context, request):
    # TODO return to context if no query given
    query = request.GET['query']
    search_results = context.search(query)

    results = []
    for line in search_results:
        line[2].anchorlink = resource_url(line[0], request, anchor = str(line[1]))
        line[2].type
        line[2].date = line[0].date
        results.append(line[2])

    return dict(results=results,
                query=query)
