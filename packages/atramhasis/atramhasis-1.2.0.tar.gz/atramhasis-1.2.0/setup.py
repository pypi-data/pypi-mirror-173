import os
import subprocess

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()


def dojo_build():
    print('-' * 50)
    print('==> check npm dependencies')
    libs = str(subprocess.check_output(["npm", "list", "-g", "grunt-cli"]))
    if 'grunt-cli' in libs:
        gruntcli = True
        print('grunt-cli OK')
    else:
        gruntcli = False
        print('grunt-cli KO, use \'npm install -g grunt-cli\' to install')
    if gruntcli:
        print('==> running grunt build')
        subprocess.call(["grunt", "-v", "build"], cwd="atramhasis/static/admin")
    print('-' * 50)


class Prepare(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        dojo_build()


requires = [
    'pyramid',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'skosprovider',
    'skosprovider_sqlalchemy',
    'skosprovider_rdf',
    'skosprovider_getty',
    'pyramid_skosprovider',
    'pyramid_openapi3',
    'language_tags',
    'jinja2',
    'pyramid_jinja2',
    'alembic',
    'babel',
    'colander',
    'requests',
    'cachecontrol',
    'dogpile.cache',
    'pyramid_rewrite',
    'python-dateutil',
    'rdflib == 6.2.0',
    'bleach',
]

setup(name='atramhasis',
      version='1.2.0',
      description='A web based editor for thesauri adhering to the SKOS specification.',
      long_description=README + '\n\n' + CHANGES,
      long_description_content_type='text/x-rst',
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8"
      ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='http://atramhasis.readthedocs.org',
      keywords='web wsgi pyramid SKOS thesaurus vocabulary',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='atramhasis',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = atramhasis:main
      [console_scripts]
      initialize_atramhasis_db = atramhasis.scripts.initializedb:main
      import_file = atramhasis.scripts.import_file:main
      dump_rdf = atramhasis.scripts.dump_rdf:main
      generate_ldf_config = atramhasis.scripts.generate_ldf_config:main
      sitemap_generator = atramhasis.scripts.sitemap_generator:main
      delete_scheme = atramhasis.scripts.delete_scheme:main
      """,
      cmdclass={
          'prepare': Prepare
      }
      )
