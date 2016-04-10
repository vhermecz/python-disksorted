# -*- coding: utf-8 -*-

"""Helper module for generating timing statistics for the disksorted utility"""
import random
import collections
from disksorted import disksorted
import gc
import contextlib
import timeit
import string
import tabulate

DataWithPayload = collections.namedtuple("DataWithPayload", "datum payload")

def some_simple_data(length=1000000):
    """Generate random array of integers"""
    data = list(range(length))
    random.shuffle(data)
    return data

def some_payload(size=32, var=0):
    """Generate a random string of length @size"""
    if var:
        size = random.randint(size-var, size+var)
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

def some_payloaded_data(length=1000000, size=32, var=0):
    """Generate random array with named tuples, containing random string as payload"""
    for datum in some_simple_data(length):
        yield DataWithPayload(datum, some_payload(size, var))

def mysorted(*args, **kwargs):
    """sorted that accepts the chunksize param"""
    _ = kwargs.pop("chunksize", None)
    return sorted(*args, **kwargs)

def pprint_timing(value):
    """Pretty-print timing data"""
    RANGES = [("h", 3600), ("m", 60), ("s", 1), ("ms", 0.001), ("μs", 1e-6), ("ns", 1e-9)]
    value += 1e-9  # CHEAT
    for postfix, limit in RANGES:
        if abs(value) >= limit:
            return "{:.2f}{}".format(float(value)/limit, postfix).replace(".00", "")

def pprint_size(value):
    """Pretty-print size (with rounding)"""
    for postfix, limit in [("G", 1e9), ("M", 1e6), ("K", 1e3), ("", 1)]:
        if value >= limit:
            return "{}{}".format(int(value/limit), postfix)

@contextlib.contextmanager
def timer():
    """Context enabled timer"""
    ts = timeit.default_timer()
    yield
    td = timeit.default_timer() - ts
    timer._data.append(td)

timer._data = []

def timer_read_data():
    """Reading collected timers"""
    tmp = timer._data
    timer._data = []
    if len(tmp) > 2:
        return sum(sorted(tmp)[1:-1])/(len(tmp)-2)
    elif len(tmp) == 0:
        return None
    else:
        return sum(tmp)/len(tmp)

timer.read = timer_read_data

KEYFN_D = lambda x: x.datum
DATACONF = [
    dict(fn=some_simple_data, args=dict(length=10000), keyfn=None, name="simple,10k"),
    dict(fn=some_simple_data, args=dict(length=1000000), keyfn=None, name="simple,1m"),
    dict(fn=some_payloaded_data, args=dict(length=10000, size=0, var=0), keyfn=KEYFN_D, name="pload:0,10k"),
    dict(fn=some_payloaded_data, args=dict(length=1000000, size=0, var=0), keyfn=KEYFN_D, name="pload:0,1m"),
    dict(fn=some_payloaded_data, args=dict(length=10000, size=32, var=0), keyfn=KEYFN_D, name="pload:32,10k"),
    dict(fn=some_payloaded_data, args=dict(length=1000000, size=32, var=0), keyfn=KEYFN_D, name="pload:0,1m"),
    dict(fn=some_payloaded_data, args=dict(length=10000, size=1024, var=1024), keyfn=KEYFN_D, name="pload:0-2k,10k"),
    dict(fn=some_payloaded_data, args=dict(length=1000000, size=1024, var=1024), keyfn=KEYFN_D, name="pload:0-2k,1m"),
]

CHUNKSIZE = [None, 1000, 10000, 100000, 1000000]

def main():
    """Generate timing table"""
    h1 = ["conf"]
    h2 = [""]
    for chunksize in CHUNKSIZE:
        if chunksize is None:
            h1.append("sorted")
            h2.append("")
        else:
            h1.append("disksorted")
            h2.append("chunksize={0}".format(pprint_size(chunksize)))
    timetable = [h1, h2]
    for dataconf in DATACONF:
        with timer():
            data = list(dataconf["fn"](**dataconf["args"]))
        print timer.read()
        times = []
        basetime = 0
        for chunksize in CHUNKSIZE:
            if chunksize is None or chunksize < dataconf["args"]["length"]:
                for _ in range(3):
                    _ = gc.collect()
                    with timer():
                        sort_fn = mysorted if chunksize is None else disksorted
                        _ = next(iter(sort_fn(data, key=dataconf["keyfn"], chunksize=chunksize)))
                timing = timer.read()
                if not times:
                    basetime = timing
                else:
                    timing = "{0}%".format(int(100 * timing / basetime))
            else:
                timing = "na"
            if not isinstance(timing, basestring):
                timing = pprint_timing(timing)
            times.append(timing)
        timetable.append([dataconf["name"]] + times)
    timetable = tabulate.tabulate(timetable, tablefmt='rst')
    with open("docs/timing.rst", "wt") as fp:
        fp.write(timetable)
    print timetable

if __name__ == "__main__":
    main()
