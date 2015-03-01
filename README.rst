========
PyTvName
========

.. _pytvname-synopsis:

PyTvName provides a python class to process names of tv shows into a
specific format given by the user.

.. contents::
    :local:

Usage
=============

Almost all functions are documented and the usage is very simple.::

    >>> from pytvname.process import prc
    >>> name = 'Banshee.S03E08.HDTV.x264-KILLERS[ettv]'
    >>> format = '{showName} S{seasonNum}E{episodeNum} {quality} {teamName}'
    >>> prc(name, format)


The best way to learn some ways to utilize this package is to look at the
examples at `pytvname_sample.py`_


.. _pytvname_sample.py: bin/pytvname_sample.py

.. _pytvname-unittests:

Executing unittests
===================

You need either setuptools or distribute in order to execute the tests. Chances are you already have one or another.::

    $ cd pytvname
    $ python setup.py test

Or simply execute one by one inside the tests directory::

    $ cd pytvname\tests
    $ python test_process.py

.. _pytvname-license:

License
=======

PyTvName is MIT licensed, so you are free to use it whatever you like, be it academic, commercial, creating forks or derivatives, as long as you copy the MIT statement if you redistribute it (see the LICENSE file for details).