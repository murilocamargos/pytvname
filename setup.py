# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Command, find_packages
except ImportError:
    from distutils.core import setup, Command, find_packages

import sys, os, re

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        result = fp.read()
    return result

def get_version(package):
    """Return package version as listed in `__version__` in `__init__.py`."""
    init_py = read(os.path.join(package, '__init__.py'))
    version = re.search("__version__ = \'(.*)\'", init_py)
    return version.group(1) if version else ''

# Make sure I have the right Python version.
if sys.version_info[:2] < (2, 7):
    print("PyTvName requires Python 2.7 or newer. Python %d.%d detected" % sys.version_info[:2])
    sys.exit(-1)

setup(
    name='pytvname',
    version=get_version('pytvname'),
    author='Murilo Camargos',
    author_email='murilo.camargosf@gmail.com',
    url='https://github.com/murilocamargos/pytvname',
    #download_url='http://pypi.python.org/pypi/',
    packages=['pytvname','tests'],
    package_data={
        '': ['LICENSE'],
        'pytvname': ['resources/*.json'],
    },
    zip_safe=False,
    provides=[
        'pytvname'
    ],
    license='MIT',
    description='Python library for processing tv shows names.',
    long_description=read('README.rst'),
    scripts=['bin/pytvname_sample.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Tv Viewers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    test_suite='tests',
)