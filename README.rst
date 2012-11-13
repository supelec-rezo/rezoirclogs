RezoIrcLogs
===========

``rezoirclogs`` is a small web app that displays irc logs in a beautiful way and provide search.

It's designed to read log files that look more or less like irssi log files, and that are organized in any hierarchy of subdirs. The log files have names that look like ``#chan_name.20101209.log``

It's based on pyramid, and can be used like any other pyramid app. Just change the root value in the config file to point to the root of your log files.

I developped it to scratch my own itch, so it may need some tweaking to suits your needs. The code is (hopefully) clean and well-tested, but if you need anything, fell free to contact me.

Installation
------------

* Clone the repository or extract the archive to the folder of your choice. (In the following let's assume it's ``$PATH_TO_RZEOIRCLOGS``)
* Create a virtualenv where you want with ``virtualenv --no-site-packages $PATH_TO_VENV`` (replace ``$PATH_TO_VENV`` with whatever you feel appropriate)
* Activate the virtualenv with ``source $PATH_TO_VENV/bin/activate``
* Install rezoirclogs with ``pip install -e $PATH_TO_RZEOIRCLOGS``
* Adjust the *root* parameter in *development.ini* and/or *production.ini* to match the path where your logs files are stored
* Execute ``pserve production.ini`` to start the builtin webserver, which by default listens on the port 6543. Check if everything is running fine.

Apache Configuration
--------------------

If the application is correctly installed (see above) it is then possible to let it run as a WSGI application through Apache.

First, edit ``$PATH_TO_REZOIRCLOGS/pyramid.wsgi`` and set the correct path to rezoirclogs application::

    application = get_app('$PATH_TO_REZOIRCLOGS/production.ini', 'main')

Then let Apache find your WSGI application. Hereafter is a configuration example for a VirtualHost (with HTTP Auth Basic password protection). Don't forget to replace ``$PATH_TO_REZOIRCLOGS`` and ``$PATH_TO_VENV`` with the actual values, and edit it to suit your needs.

::

    <VirtualHost *:80>
        ServerName irclogs.example.org
        
        DocumentRoot $PATH_TO_REZOIRCLOGS
        <Directory "$PATH_TO_REZOIRCLOGS">
            Order allow,deny
            Allow from all
            
            AuthName        "Logs IRC"
            AuthType        Basic
            AuthUserFile    auth.users
            Satisfy         All
            Require         valid-user
            
            AllowOverride AuthConfig FileInfo Limit
            
            Options -ExecCGI +FollowSymLinks -Includes -IncludesNOEXEC -Indexes
        </Directory>
        
        CustomLog /var/log/apache2/access_irclogs.log vhost_combined
        ErrorLog /var/log/apache2/error_irclogs.log
        
        <IfModule wsgi_module>
            WSGIProcessGroup pyramid
            WSGIApplicationGroup irclogs
            WSGIPassAuthorization On
            WSGIDaemonProcess pyramid user=www-data group=www-data processes=1 threads=4 \
                    python-path=$PATH_TO_VENV/lib/python2.6/site-packages
            WSGIScriptAlias / $PATH_TO_REZOIRCLOGS/pyramid.wsgi
        </IfModule>
    </VirtualHost>

The user under which will be executed the WSGI application must have read permissions on the directory where the irclogs lie (i.e. in the above configuration example, *www-data* must be able to read the directory set up in ``production.ini``.)

Further Tweaking
----------------

If the log files are not parsed correctly by rezoirclogs, modify the regular expressions in ``$PATH_TO_REZOIRCLOGS/rezoirclogs/utils.py`` to match the format of your log files (variable *_regex* in the LogLine class).

|travis|_

.. |travis| image:: https://secure.travis-ci.org/supelec-rezo/rezoirclogs.png?branch=master
.. _travis: http://travis-ci.org/supelec-rezo/rezoirclogs
