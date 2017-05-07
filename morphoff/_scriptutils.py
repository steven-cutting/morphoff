# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '03/23/2017'
__doc__ = """
Misc. utils for the package's scripts.
"""

from collections import namedtuple
from os import path
# import logging

# from arrow import now
try:
    import cytoolz as tlz
    from cytoolz import curried as tlzc
except ImportError:
    import toolz as tlz
    from toolz import curried as tlzc

from h_topic_model._scriptutils import str_to_log_level_code, log_run_time

from morphoff.modelutils import _LOADERDICT

# LOG = logging.getLogger(__name__)

MODELTYPES = set(_LOADERDICT.keys())


# ------------------------------------------------------------------------------
# morphoff specific utils


SegMdlFile = namedtuple("SegMdlFile", ["name", "type", "filename"])


def tsegs_input_to_SegMdlFile(value):
    return SegMdlFile(*value)


def _validate_tsegs_filename(value):
    if not path.isfile(value.filename):
        raise ValueError("Not a file or does not exist {}".format(value.filename))
    else:
        return value


@tlz.curry
def _validate_tsegs_modeltype(value, modeltypes=MODELTYPES):
    if value.type not in modeltypes:
        raise KeyError("Can not work with '{wt}' model type. Available model types: {mt}".format(
            wt=value.type,
            mt=", ".join(modeltypes)))
    else:
        return value


@tlz.curry
def _validate_tsegs_input(value, modeltypes=MODELTYPES):
    return tlz.pipe(value,
                    _validate_tsegs_filename,
                    _validate_tsegs_modeltype(modeltypes=modeltypes))


@tlz.curry
def _proc_and_validate_tseg_input(value, modeltypes=MODELTYPES):
    return tlz.pipe(value,
                    tsegs_input_to_SegMdlFile,
                    _validate_tsegs_input(modeltypes=modeltypes))


def proc_tsegs_option_input(ctx, param, value, modeltypes=MODELTYPES):
    return tlz.pipe(value,
                    tlzc.map(_proc_and_validate_tseg_input(modeltypes=modeltypes)),
                    list)
