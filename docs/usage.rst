=====
Usage
=====

To use Python Disksorted in a project::

    from disksorted import disksorted
    data = disksorted(data, key=lambda x: -x[2].cost)

Timing
------

The filesystem (either using HDD or SSD) has a much slover throughput than memory. So it should
come as no surprise, that while disksorted solves one problem, produces another one. Sorting this
way is slower.

NOTE: This part of the module still requires some development, to achieve better performance.

.. include:: timing.rst
