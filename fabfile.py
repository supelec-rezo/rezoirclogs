from fabric.api import *
from fabric.contrib.files import *

env.hosts = ['anakin.rez-gif.supelec.fr']


def reload():
    sudo('/etc/init.d/apache2 reload')


def deploy():
    with cd('/var/lib/rezoirclogs'):
        # put crashes for me
        # put('production.ini', '.')
        run('wget https://raw.github.com/supelec-rezo/rezoirclogs/master/production.ini -O production.ini')
        if not exists('venv'):
            run('virtualenv venv')
        run('venv/bin/pip install -e git://github.com/supelec-rezo/rezoirclogs.git@origin#egg=rezoirclogs')
        with cd('venv/'):
            run('wget https://raw.github.com/supelec-rezo/rezoirclogs/master/pyramid.wsgi -O pyramid.wsgi')
        # put('pyramid.wsgi', 'venv/')
    reload()
