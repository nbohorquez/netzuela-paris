import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
	'pyramid',
	'SQLAlchemy',
	'transaction',
	'pyramid_tm',
	'pyramid_debugtoolbar',
	'zope.sqlalchemy',
	'waitress',
	'mysql-python',
	'py-bcrypt',
	'FormEncode',
	'pyDNS'
]

setup(name='paris',
      version='0.1',
      description='paris',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Zuliaworks C.A.',
      author_email='contacto@zuliaworks.com',
      url='www.zuliaworks.com',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='paris',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = paris:main
      [console_scripts]
      """,
      )

