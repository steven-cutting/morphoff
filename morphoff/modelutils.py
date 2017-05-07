# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '05/04/2017'
__doc__ = """
Utils for working with various segmentation models.
"""

try:
    import cytoolz as tlz
    from cytoolz import curried as tlzc
except ImportError:
    import toolz as tlz
    from toolz import curried as tlzc

from h_topic_model import segment as mseg

from morphoff import fcatsegment as fseg


_LOADERDICT = {"morfessor2": mseg.load_morfessor_model,
               "flatcat": fseg.load_flatcat_model}


@tlz.curry
def load_seg_model(kind, filename, loaderdict=_LOADERDICT):
    """
    kind - Type of segmenter - morfessor2 or flatcat.
    model - the model that should be used to create the segmenter.

    loaderdict - {"kind1": loader1, "kind2": loader2}
    """
    return (kind, loaderdict[kind](filename))


def load_seg_models(models, loaderdict=_LOADERDICT):
    """
    models - [(kind1, filename1), (kind2, filename2), ...]
    """
    return tlz.pipe(models,
                    tlzc.map(lambda model: load_seg_model(model[0],
                                                          model[1],
                                                          loaderdict=loaderdict)),
                    tuple)
