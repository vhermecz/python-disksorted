===============================
Python Disksorted
===============================

.. image:: https://img.shields.io/pypi/v/python-disksorted.svg
        :target: https://pypi.python.org/pypi/python-disksorted

.. image:: https://img.shields.io/travis/vhermecz/python-disksorted.svg
        :target: https://travis-ci.org/vhermecz/python-disksorted

.. image:: https://readthedocs.org/projects/python-disksorted/badge/?version=latest
        :target: https://readthedocs.org/projects/python-disksorted/?badge=latest
        :alt: Documentation Status


Sortin' gigz

* Free software: ISC license
* Documentation: https://python-disksorted.readthedocs.org.

TODO
--------
* Documentation
* Fix
* Add to PYPI
* WIN

Features
--------

* TODO

Notes
--------

The cmp parameter of sorted is not supported, as Python 3.0 removed that. Use the functools.cmp_to_key method if needed.

Compared to the built in sorted, disksorted method returns a generator rather than a list. This is a lazy approach, which allows for 


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
