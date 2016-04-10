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
__all__ = ['disksorted', 'diskiterator', 'merge', 'SERIALIZER_PICKLE', 'SERIALIZER_JSON',
           'SERIALIZER_MARSHAL']


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
    '''
    Merge iterators together
    :param chunks: to be merged.
    :param key: specifies a function of one argument that is used to extract a comparison key from
        each list element.
    :param reverse: is a boolean value. If set to True, then the list elements are sorted as if
        each comparison were reversed.
    '''
    # NOTE: consider using heapq.merge
    key = key or (lambda x: x)
    if reverse:
        key = key_to_reverse_order(key)
    heap = [(((0, ), idx), MERGE_SENTINEL) for idx in range(len(chunks))]
    heapq.heapify(heap)
    while heap:
        (_, stream_idx), record = heapq.heappop(heap)
        if record != MERGE_SENTINEL:
            yield record
        try:
            record = next(chunks[stream_idx])
            heapq.heappush(heap, (((1, key(record)), stream_idx), record))
        except StopIteration:
            pass


def _json_dump(payload, fp):
    json.dump(payload, fp)
    fp.write("\n")


def _json_load(fp):
    return json.loads(next(fp))


SERIALIZER_PICKLE = (functools.partial(pickle.dump, protocol=-1), pickle.load, "w+b")
SERIALIZER_JSON = (_json_dump, _json_load, "w+t")
SERIALIZER_MARSHAL = (marshal.dump, marshal.load, "w+b")


def diskiterator(iterable, fp=None, serializer=SERIALIZER_PICKLE):
    '''
    Cache iterator to disk
    :param iterable: to be cached
    :param fp: is the file-object to be used. (tempfile to be used if omitted.)
    :param serializer: defines the methods to be used for transfering data between disk and memory.
    :type fp: file|NoneType
    :type serializer: (function, function)
    '''
    dump, load, filemode = serializer
    def chunk_writer(chunk, fp=None):
        fp = fp or tempfile.TemporaryFile(mode=filemode)
        for subchunk in chunks(chunk, 128):
            dump(list(subchunk), fp)
        dump(list(), fp)
        fp.seek(0)
        return fp
    def chunk_reader(fp):
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
    return chunk_reader(chunk_writer(iterable, fp=fp))


def disksorted(iterable, key=None, reverse=False, chunksize=sys.maxsize,
               serializer=SERIALIZER_PICKLE):
    '''
    Sorting function for collections not fitting into memory
    NOTE: Uses temporary files
    :param iterable: of items to be sorted
    :param key: specifies a function of one argument that is used to extract a comparison key from
        each list element.
    :param reverse: is a boolean value. If set to True, then the list elements are sorted as if
        each comparison were reversed.
    :param chunksize: specifies the largest number of items to be held in memory at once.
    :param serializer: defines the methods to be used for transfering data between disk and memory.
    :type key: function|NoneType
    :type reverse: bool
    :type chunksize: int|NoneType
    :type serializer: (function, function)
    '''
    if chunksize < 1:
        raise ValueError("chunksize to be positive integer")
    single = True
    pieces = []
    chunk = []
    for chunk in chunks(iterable, chunksize):
        chunk = sorted(chunk, key=key, reverse=reverse)
        if len(chunk) == chunksize:
            single = False
        if not single:
            pieces.append(diskiterator(chunk, serializer=serializer))
    if not single:
        chunk = merge(pieces, key, reverse)
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
