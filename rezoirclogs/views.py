import datetime
from pyramid.view import view_config
from pyramid.url import resource_url
import colander
from deform import Form
from deform.exception import ValidationFailure
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
    get_args = request.GET.copy()
    try:
        select = int(get_args.pop('select'))
        lines[select].selected = True
    except (KeyError, ValueError):
        select = None

    for i, line in enumerate(lines):
        if line.time:
            query = get_args.copy()
            if select is None:
                query.add('select', i)
                line.anchor = '%s' % i
            else:
                fro, to = sorted((i, select))
                query.add('range', '%s-%s'%(fro, to + 1))
                line.anchor = '%s' % fro
            line.anchorlink = resource_url(context, request, anchor=line.anchor, query=query)

    for rang in request.GET.getall('range'):
        try:
            fro, to = map(int, rang.split('-'))
            for i in range(fro, to):
                lines[i].highlighted = True
        except (ValueError, IndexError):
            pass

    return {'lines': lines, 'context': context}


class Search(colander.MappingSchema):
    query = colander.SchemaNode(colander.String(), validator = colander.Length(min=3))
    after_date = colander.SchemaNode(colander.Date(), title='Search after the date',
                                     missing=None, default=(datetime.date.today() - datetime.timedelta(30)))


@view_config(name='search', renderer='search.jinja2')
def search(context, request):
    search_form = Form(Search(), action='search', buttons=('search',), css_class='well')
    if 'search' in request.POST:
        try:
            appstruct = search_form.validate(request.POST.items())
        except ValidationFailure, e:
            return {'context': context, 'form':e.render(), 'resources' : search_form.get_widget_resources()}

        search_results = context.search(appstruct['query'], appstruct['after_date'])

        results = []
        for line in search_results:
            line[2].anchorlink = resource_url(line[0], request, anchor = str(line[1]))
            line[2].date = line[0].date
            line[2].chan = line[0].__parent__.__name__
            results.append(line[2])

        return dict(context=context, results=results, query=appstruct['query'])
    else:
        return {'context': context, 'form': search_form.render(), 'resources' : search_form.get_widget_resources()}
