import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid>=1.3', 'pyramid_debugtoolbar', 'pyramid_jinja2',
            'deform', 'pyramid_beaker', 'unittest2', 'deform_bootstrap',
            'waitress']

setup(name='rezoirclogs',
      version='1.9',
      description='rezoirclogs',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Georges Dubus',
      author_email='georges.dubus@compiletoi.net',
      url='',
      keywords='web pyramid pylons irc logs',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite="rezoirclogs",
      entry_points = """\
      [paste.app_factory]
      main = rezoirclogs:main
      """,
      paster_plugins=['pyramid'],
      )

