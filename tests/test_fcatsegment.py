# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/13/2017'


import pytest

from morphoff import fcatsegment as fseg
from tests import t_utils as tu


@pytest.mark.parametrize("string,expected",
                         [(u"foobarbaz", [u"foo", u"bar", u"baz"]),
                          (u"foo", [u"foo"]),
                          (u"הוא צילם עליו כתבה", [u"הוא צילם עליו כתבה"]),
                          ])
def test__mk_segmenter(string, expected):
    model = tu.MockFlatCatSegmentModel()
    segment = fseg.mk_segmenter(model)
    # print segment
    # print segment(string)
    # print (string, ) if type(string) in (unicode, str) else string
    assert(segment(string) == expected)


@pytest.mark.parametrize("string,expected",
                         [(u"foo bar baz", [u"foo", u"bar", u"baz"]),
                          (u"foo", [u"foo"]),
                          (u"הוא צילם עליו כתבה",
                           # Hebrew unicode code points.
                           [u'\u05d4\u05d5\u05d0',
                            u'\u05e6\u05d9\u05dc\u05dd',
                            u'\u05e2\u05dc\u05d9\u05d5',
                            u'\u05db\u05ea\u05d1\u05d4']),
                          ])
def test__segment_text(string, expected):
    model = tu.MockFlatCatSegmentModel()
    assert(fseg.segment_text(model, string) == expected)


@pytest.mark.parametrize("strings,expected,flatten",
                         [([u"foo bar baz", u"foo", u"הוא צילם עליו כתבה"],
                           [[[u"foo"], [u"bar"], [u"baz"]],
                            [[u"foo"], ],
                            # Hebrew unicode code points.
                            [[u'\u05d4\u05d5\u05d0'],
                             [u'\u05e6\u05d9\u05dc\u05dd'],
                             [u'\u05e2\u05dc\u05d9\u05d5'],
                             [u'\u05db\u05ea\u05d1\u05d4']]],
                           False),
                          ([u"foo bar baz", u"foo"],
                           [u"foo", u"bar", u"baz",
                            u"foo"],
                           True),
                          ])
def test__segment_many(strings, expected, flatten):
    model = tu.MockFlatCatSegmentModel()
    assert(list(fseg.segment_many(model, strings, flatten=flatten)) == expected)
