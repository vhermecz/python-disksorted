#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests
----------------------------------

Tests for `python-disksorted` module.
"""

import unittest

from disksorted import disksorted, SERIALIZER_JSON, SERIALIZER_MARSHAL
import random
import collections
import sys

IS_PY3 = sys.version_info[0] == 3

class TestClass(object):
    def __init__(self, value):
        self.value = value


lrange = lambda x:list(range(x))


TestNamedTuple = collections.namedtuple("TestNamedTuple", "value")


class TestPythonDisksorted(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        initial = [1, 10, 2, 9, 3, 8, 4, 7, 5, 6]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(list(disksorted(initial, chunksize=4)), expected)
        self.assertEqual(list(disksorted(initial, chunksize=4, reverse=True)), expected[::-1])
        self.assertEqual(list(disksorted(initial, chunksize=4, key=lambda x: -x)), expected[::-1])
        self.assertEqual(list(disksorted(initial, chunksize=4, key=lambda x: -x, reverse=True)), expected)

    def test_cornercases(self):
        self.assertEqual(list(disksorted([])), [])
        with self.assertRaises(ValueError):
            _ = list(disksorted([], chunksize=0))

    if not IS_PY3:
        def test_empty_values(self):
            initial = [tuple(), True, False, 0, 0.0, -1, 1, "", None, [], {}]
            self.assertEqual(list(disksorted(initial, chunksize=5)), sorted(initial))

    def test_medium(self):
        initial = lrange(10000)
        random.shuffle(initial)
        self.assertEqual(list(disksorted(initial, chunksize=1000)), lrange(10000))

    def test_objects(self):
        initial = [TestClass(i) for i in lrange(1000)]
        random.shuffle(initial)
        result = [i.value for i in disksorted(initial, chunksize=500, key=lambda x: x.value)]
        self.assertEqual(result, lrange(1000))

    def test_namedtuple(self):
        initial = [TestNamedTuple(i) for i in lrange(1000)]
        random.shuffle(initial)
        result = [i.value for i in disksorted(initial, chunksize=500, key=lambda x: x.value)]
        self.assertEqual(result, lrange(1000))
    
    def test_serialize_json(self):
        self.assertEqual(list(disksorted(lrange(10), chunksize=4, serializer=SERIALIZER_JSON)), lrange(10))
        self.assertEqual(list(disksorted(self.get_some_unicode_array(), chunksize=1, serializer=SERIALIZER_JSON)), self.get_some_unicode_array())

    def test_serialize_marshal(self):
        self.assertEqual(list(disksorted(lrange(10), chunksize=4, serializer=SERIALIZER_MARSHAL)), lrange(10))
        self.assertEqual(list(disksorted(self.get_some_unicode_array(), chunksize=1, serializer=SERIALIZER_MARSHAL)), self.get_some_unicode_array())

    def get_some_unicode_array(self):
        return ['apple', u'\xe1\xe9\xfa\u0171\u0151']


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
