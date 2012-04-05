RezoIrcLogs
===========

``rezoirclogs`` is a small web app that displays irc logs in a beautiful way and provide search.

It's designed to read log files that look more or less like irssi log files, and that are organized in any hierarchy of subdirs. The log files have names that look like ``#chan_name.20101209.log``

It's based on pyramid, and can be used like any other pyramid app. Just chan the root value in the config file to point to the root of your log files.

I developped it to scratch my own itch, so it may need some tweaking to suits your needs. The code is (hopefully) clean and well-tested, but if you need anything, fell free to contact me.