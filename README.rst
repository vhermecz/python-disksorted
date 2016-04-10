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

Like the built-in sorted, just without the memory limitations.

Most data processing operations can be performed sequentially, keeping only a subset of the
whole dataset in memory. When this is not the case, sorting the dataset can make such a sequential
operation possible. However, sorting a large set of data, while it is not hard, goes beyond the
complexity that is convenient to be delt with, during solving a problem. Most of the times, you can
import data into python with the right sorting, and you should certainly do that. But sometimes,
this is not possible. For those cases, now you have this library.

Requirements
------------
* Make sure, the contents of your iterator are serializable
* pip install python-disksorted
* Change **sorted** to **disksorted** in your code
* Profit

Notes
--------

Compared to the built-in sorted, disksorted method returns a generator rather than a list. 
This lazy approach allows for writing code which will only be executed when the data in the iterator
is actually used. Other execution paths wont suffer from the long running sorting operation...


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
