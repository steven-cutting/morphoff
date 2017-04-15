# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/13/2017'


import pytest

from morphoff import mktokens as mkt
from tests import t_utils as tu


@pytest.mark.parametrize("string,expected",
                         [(u"foobarbaz", ([u"foo", u"bar", u"baz"],
                                          [u"foo", u"bar", u"baz"])),
                          (u"foo", ([u"foo"], [u"foo"])),
                          (u"הוא צילם עליו כתבה", ([u"הוא צילם עליו כתבה"],
                                                  [u"הוא צילם עליו כתבה"],)),
                          ])
def test__mk_dual_segmenter(string, expected):
    mmodel = tu.MockMorfessorSegmentModel()
    fmodel = tu.MockFlatCatSegmentModel()
    segment = mkt.mk_dual_segmenter(mmodel, fmodel)
    assert(segment(string) == expected)


@pytest.mark.parametrize("string,expected",
                         [(u"foo bar baz", [([u"foo"], [u"foo"]),
                                            ([u"bar"], [u"bar"]),
                                            ([u"baz"], [u"baz"])]),
                          (u"foo", [([u"foo", ],
                                     [u"foo", ])]),
                          ])
def test__segment_text(string, expected):
    mmodel = tu.MockMorfessorSegmentModel()
    fmodel = tu.MockFlatCatSegmentModel()
    segment = mkt.mk_dual_segmenter(mmodel, fmodel)
    assert(mkt.segment_text(segment, string) == expected)


@pytest.mark.parametrize("strings,expected,flatten",
                         [([u"foo bar baz", u"foo", u"foobarbaz"],
                           [[([u"foo"], [u"foo"]),
                             ([u"bar"], [u"bar"]),
                             ([u"baz"], [u"baz"])],
                            [([u"foo"], [u"foo"])],
                            [([u"foo", u"bar", u"baz"], [u"foo", u"bar", u"baz"])]],
                           False),
                          ([u"foo bar baz", u"foo"],
                           [[u"foo"], [u"foo"], [u"bar"], [u"bar"],
                            [u"baz"], [u"baz"], [u"foo"], [u"foo"]],
                           True),
                          ])
def test__dual_segment_many(strings, expected, flatten):
    mmodel = tu.MockMorfessorSegmentModel()
    fmodel = tu.MockFlatCatSegmentModel()
    assert(list(mkt.dual_segment_many(mmodel, fmodel,
                                      strings,
                                      flatten=flatten)) ==
           expected)


@pytest.mark.parametrize("data,expected,separator",
                         [([[([u"foo"], [u"foo"]),
                             ([u"bar"], [u"bar"]),
                             ([u"baz"], [u"baz"])],
                            [([u"foo"], [u"foo"])],
                            [([u"foo", u"bar", u"baz"], [u"foo", u"bar", u"baz"])]],
                           [(u"foo", u"foo"),
                            (u"bar", u"bar"),
                            (u"baz", u"baz"),
                            (u"foo", u"foo"),
                            (u"foo + bar + baz", u"foo + bar + baz")],
                           " + "),
                          ([[([u"foo"], [u"foo"])],
                            [([u"foo", u"bar", u"baz"], [u"foo", u"bar", u"baz"])]],
                           [(u"foo", u"foo"),
                            (u"foo, bar, baz", u"foo, bar, baz")],
                           ", "),
                          ])
def test__to_string_pairs(data, expected, separator):
    assert(list(mkt.to_string_pairs(data, separator)) == expected)


@pytest.mark.parametrize("strings,expected",
                         [([u"foo bar baz", u"foo", u"foobarbaz"],
                           [(u"foo", u"foo"),
                            (u"bar", u"bar"),
                            (u"baz", u"baz"),
                            (u"foo", u"foo"),
                            (u"foo + bar + baz", u"foo + bar + baz")]),
                          ])
def test__dual_segment_many_and_to_string_pairs(strings, expected):
    mmodel = tu.MockMorfessorSegmentModel()
    fmodel = tu.MockFlatCatSegmentModel()
    data = mkt.dual_segment_many(mmodel, fmodel, strings)
    assert (list(mkt.to_string_pairs(data)) == expected)
