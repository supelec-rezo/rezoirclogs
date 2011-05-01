import os
from pyramid.config import Configurator
from pyramid_beaker import set_cache_regions_from_settings
from rezoirclogs.resources import Filesystem, Directory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    root = settings.pop('root', None)
    if root is None:
        raise ValueError('rezoirclogs requires a root')
    fs = Filesystem(os.path.abspath(os.path.normpath(root)))
    def get_root(environ):
        return Directory(fs, root)

    set_cache_regions_from_settings(settings)
    config = Configurator(root_factory=get_root, settings=settings)
    config.include('pyramid_jinja2')
    config.scan()
    config.add_static_view('static', 'rezoirclogs:static')
    config.add_static_view('static_form', 'deform:static')
    return config.make_wsgi_app()

