# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/08/2017'
__doc__ = """
Module uses Flatcat to segment words.
"""

import flatcat
try:
    import cytoolz as tlz
    from cytoolz import curried as tlzc
except ImportError:
    import toolz as tlz
    from toolz import curried as tlzc

from h_topic_model import segment as mseg
from h_topic_model import textproc_utils as tpu


def load_flatcat_model(filename):
    """
    Loads and initializes Flatcat model from tarball archive.
    """
    io = flatcat.FlatcatIO()
    model = io.read_tarball_model_file(filename)
    model.initialize_hmm()
    return model


def mk_segmenter(model):
    """
    Returns function that segments text using the provided Flatcat models
    viterbi_segment method.
    """
    def segment(token):
        return tlz.pipe(token,
                        model.viterbi_segment,
                        mseg.unpack_viterbi_segment)

    return segment


@tlz.curry
def segment_text(model, txt, flatten=True):
    """
    Splits the text into tokens and then segments the tokens.

    Uses a Flatcat model.

    Curried.
    """
    return tlz.pipe(txt,
                    tpu.split_and_clean,
                    tlzc.map(mk_segmenter(model)),
                    mseg.should_flatten(flatten),
                    list)


def segment_many(model, txts, flatten=True):
    """
    Uses a Flatcat model.
    """
    return tlz.pipe(txts,
                    tlzc.map(segment_text(model, flatten=flatten)),
                    mseg.should_flatten(flatten))
