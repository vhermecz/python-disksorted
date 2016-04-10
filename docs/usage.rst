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

Time of operations relative to in-memory sort. Conf:
**simple,10k**: A list of 10k random integers.
**pload:32,10k**: A 10k list of namedtuples of random-integers plus a 32byte string payload.
**pload:0-2k,1m**: A 1 million item list, string payload is 0-2048 byte. 
