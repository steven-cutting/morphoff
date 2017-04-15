# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/08/2017'
__doc__ = """
Module uses Flatcat to train a morpheme segmentation model.
"""

import arrow
import logging
import random

import flatcat

LOG = logging.getLogger(__name__)


def fit_flatcat_model(datafile, corpusweight=1.0, randomState=None):
    random.seed(randomState)
    io = flatcat.FlatcatIO()

    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight=corpusweight)

    model.add_corpus_data(io.read_segmentation_file(datafile))
    model.initialize_hmm()

    # from https://github.com/aalto-speech/flatcat/blob/master/flatcat/cmd.py#L755
    ts = arrow.now()
    model.train_batch(
        # Stop training if cost reduction between iterations is below this limit * #boundaries.
        min_iteration_cost_gain=0.0025,
        # Stop training if cost reduction between epochs is below this limit * #boundaries.
        # In semi-supervised training the cost is not monotonous between epochs, so this
        # limit is meaningless.
        min_epoch_cost_gain=None,
        # The number of training epochs.
        max_epochs=4,
        # Maximum number of iterations of each operation in the first epoch.
        max_iterations_first=1,
        # Maximum number of iterations of each operation in the subsequent epochs.
        max_iterations=1,
        # Maximum number of iterations of resegmentation in all epochs.
        max_resegment_iterations=2,
        # Maximum number of iterations of resegmentation in all epochs.
        max_shift_distance=2,
        # Minimum number of letters remaining in the shorter morph after a shift operation.
        min_shift_remainder=2)
    LOG.info('Final cost: {}'.format(model.get_cost()))
    te = arrow.now()
    LOG.info('Training time: {}'.format(te - ts))

    return model


def save_flatcat_model(filename, model):
    io = flatcat.FlatcatIO()
    io.write_tarball_model_file(filename, model)
