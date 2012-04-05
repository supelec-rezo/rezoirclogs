from pyramid.paster import get_app
application = get_app('/var/lib/rezoirclogs/production.ini', 'main')
