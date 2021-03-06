# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/13/2017'
__doc__ = """
Create tokens.
"""

import csv
import itertools as itls

try:
    import cytoolz as tlz
    from cytoolz import curried as tlzc
except ImportError:
    import toolz as tlz
    from toolz import curried as tlzc


from h_topic_model import textproc_utils as tpu
from h_topic_model import segment as mseg
from morphoff import fcatsegment as fseg


concat_to_list = tlz.compose(list, tlz.concat)


_MKSEGS_DICT = {"morfessor2": mseg.mk_segmenter,
                "flatcat": fseg.mk_segmenter}


def mk_segmenter(modeltype, model, mksegsdict=_MKSEGS_DICT):
    """
    modeltype - Type of segmenter - morfessor2 or flatcat.
    model - the model that should be used to create the segmenter.

    mksegsdict - {"modeltype1": mk_modeltype1_segmenter,
                  "modeltype2": mk_modeltype2_segmenter}
    """
    return mksegsdict[modeltype](model)


def mk_dual_segmenter(morfessorModel, flatcatModel):
    """
    Allows for comparison of Morfessor 2.0 and Flatcat segmentation results.

    Accepts a Morfessor 2.0 segmentation model and a Flatcat segmentation model.

    Returns the segmentation resutls of both side by side in a tuple.
      (morfessor2.0, flatcat)
    """
    # msegmenter = tlz.compose(tuple, mseg.mk_segmenter(morfessorModel))
    msegmenter = mseg.mk_segmenter(morfessorModel)
    fsegmenter = fseg.mk_segmenter(flatcatModel)

    return lambda token: ([token], msegmenter(token), fsegmenter(token))


def into_list(item):
    """
    return [item, ]
    """
    return [item, ]


def mk_segmenters(models, mksegsdict=_MKSEGS_DICT):
    """
    Provide n models in tuples with the model type ('morfessor2' or 'flatcat')
    and the model in form:
        (modeltype, model)
    """
    segmenters = tlz.pipe(models,
                          tlzc.map(lambda model: mk_segmenter(model[0],
                                                              model[1],
                                                              mksegsdict=mksegsdict)),
                          lambda segs: itls.chain([into_list], segs),
                          list)
    return lambda token: tuple(map(lambda f: f(token), segmenters))


@tlz.curry
def segment_text(segmentfunc, txt, flatten=False):
    """
    Splits the text into tokens and then segments the tokens.

    using segmentfunc

    Curried.
    """
    return tlz.pipe(txt,
                    tpu.split_and_clean,
                    tlzc.map(segmentfunc),
                    mseg.should_flatten(flatten),
                    list)


@tlz.curry
def dual_segment_many(morfessorModel, flatcatModel, txts, flatten=False):
    return tlz.pipe(txts,
                    tlzc.map(segment_text(mk_dual_segmenter(morfessorModel,
                                                            flatcatModel),
                                          flatten=flatten)),
                    mseg.should_flatten(flatten))


@tlz.curry
def segment_many(segmenter, txts, flatten=False):
    return tlz.pipe(txts,
                    tlzc.map(segment_text(segmenter,
                                          flatten=flatten)),
                    mseg.should_flatten(flatten))


@tlz.curry
def to_string_pairs(segmentsbytxt, separator=" + "):
    """
    segmentsbytxt - Output from dual_segment_many.

    >>> exdata = [[([u"foo"], [u"foo"])], [([u"foo", u"bar", u"baz"], [u"foo", u"bar", u"baz"])]]

    >>> to_string_pairs(exdata)
    [(u"foo", u"foo"), (u"foo + bar + baz", u"foo + bar + baz")],

    >>> to_string_pairs(exdata, separator=", ")
    [(u"foo", u"foo"), (u"foo, bar, baz", u"foo, bar, baz")],
    """
    return tlz.pipe(segmentsbytxt,
                    tlz.concat,
                    tlzc.map(tlz.compose(tuple, tlzc.map(separator.join))))


def unique(seq):
    return tlz.pipe(seq,
                    set,
                    list)


@tlz.curry
def encode_row(encoding, row):
    """
    Encode all of the text in the tuple row, using encoding.
    """
    return tlz.pipe(row,
                    tlzc.map(lambda string: string.encode(encoding)),
                    tuple)


def segments_to_cvs(filename, seq, headers=(u"original", u"morfessor2.0", u"flatcat"),
                    delimiter='\t', sort_f=tlz.identity, encoding="utf-8"):
    """
    Does not include a header.
    The tuples in 'seq' should have this format:
        (count, token)

    Delimiter defaults to tabs.
    sort_f - A function that is applied to seq before writting it to the file.
             Default is the identity function.
    """
    csv.register_dialect('custom-sep', delimiter=delimiter)
    with open(filename, 'wb') as out:
        csv_out = csv.writer(out, 'custom-sep')
        csv_out.writerow(encode_row(encoding, headers))
        for row in sort_f(seq):
            tlz.pipe(row,
                     encode_row(encoding),
                     csv_out.writerow)
