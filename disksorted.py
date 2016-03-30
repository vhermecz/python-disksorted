# -*- coding: utf-8 -*-

"""
Simple helper for sorting when your ordinary memory wont cut it.
"""

import itertools
import sys
import tempfile
import operator
import json
import marshal
import functools
try:
    import cPickle as pickle
except:
    import pickle
import heapq

__author__ = 'Vajk Hermecz'
__email__ = 'vhermecz@gmail.com'
__version__ = '0.9'
__all__ = ['disksorted', 'merge', 'SERIALIZER_PICKLE', 'SERIALIZER_JSON', 'SERIALIZER_MARSHAL']


def chunks(iterable, size):
    """
    Spliter iterator t chunks of size items
    @see: http://stackoverflow.com/a/434314/1442987
    """
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, size))


def key_to_reverse_order(key_fn):
    # FIXME: applying twice should remove 
    """Convert keys to reverse order"""
    class K(object):
        __slots__ = ['obj']
        def __init__(self, obj, *args):
            self.obj = key_fn(obj)
        def __lt__(self, other):
            return operator.gt(self.obj, other.obj)
        def __gt__(self, other):
            return operator.lt(self.obj, other.obj)
        def __eq__(self, other):
            return operator.eq(self.obj, other.obj)
        def __le__(self, other):
            return operator.ge(self.obj, other.obj)
        def __ge__(self, other):
            return operator.le(self.obj, other.obj)
        def __ne__(self, other):
            return operator.ne(self.obj, other.obj)
        def __hash__(self):
            raise TypeError('hash not implemented')
    return K


MERGE_SENTINEL = object()


def merge(chunks, key=None, reverse=False):
    """
    Merge iterators together
    TODO: consider using heapq.merge
    """
    # TODO: test reverse
    key = key or (lambda x: x)
    if reverse:
        key = key_to_reverse_order(key)
    heap = [((None, idx), MERGE_SENTINEL) for idx in range(len(chunks))]
    heapq.heapify(heap)
    while heap:
        (_, stream_idx), record = heapq.heappop(heap)
        if record != MERGE_SENTINEL:
            yield record
        try:
            record = chunks[stream_idx].next()
            heapq.heappush(heap, (((1, key(record)), stream_idx), record))
        except StopIteration:
            pass


def _json_dump(payload, fp):
    json.dump(payload, fp)
    fp.write("\n")
    

def _json_load(fp):
    return json.loads(next(fp))


SERIALIZER_PICKLE = (functools.partial(pickle.dump, protocol=-1), pickle.load)
SERIALIZER_JSON = (_json_dump, _json_load)
SERIALIZER_MARSHAL = (marshal.dump, marshal.load)


def disksorted(iterable, key=None, reverse=False, chunksize=sys.maxint,
               serializer=SERIALIZER_PICKLE):
    """
    Sorting function for collections not fitting into memory
    NOTE: Uses temporary files
    NOTE: chunk_reader might do buffering
    """
    if chunksize < 1:
        raise ValueError("chunksize to be positive integer")
    dump, load = serializer
    def _chunk_writer(chunk, fp=None):
        fp = fp or tempfile.TemporaryFile()
        for subchunk in chunks(chunk, 128):
            dump(list(subchunk), fp)
        dump(list(), fp)
        fp.seek(0)
        return fp
    def _chunk_reader(fp):
        try:
            while True:
                sublist = load(fp)
                if not sublist:
                    break
                for item in sublist:
                    yield item
        finally:
            try:
                fp.close()
            except Exception:
                pass
    single = True
    pieces = []
    chunk = []
    for chunk in chunks(iterable, chunksize):
        chunk = sorted(chunk, key=key, reverse=reverse)
        if len(chunk) == chunksize:
            single = False
        if not single:
            pieces.append(_chunk_writer(chunk))
    if not single:
        chunk = merge([_chunk_reader(fp) for fp in pieces], key, reverse)
    for item in chunk:
        yield item


if sys.version_info[0] == 2:
    _disksorted = disksorted
    def disksorted(iterable, cmp=None, key=None, reverse=False, chunksize=sys.maxint,
                   serializer=SERIALIZER_PICKLE):
        if cmp:
            key = functools.cmp_to_key(cmp)
        return _disksorted(iterable, key=key, reverse=reverse, chunksize=chunksize,
                           serializer=serializer)
    disksorted.__doc__ = _disksorted.__doc__
