# -*- coding: utf-8 -*-

__title__ = 'morphoff'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '04/13/2017'

from os import path

import pytest
import toolz as tlz

from h_topic_model import utils as u

from morphoff import _scriptutils as su
# from tests import t_utils as tu
import tests


k_error = pytest.mark.xfail(raises=KeyError,
                            reason="Test to ensure it does raise error on proper value.")
v_error = pytest.mark.xfail(raises=ValueError,
                            reason="Test to ensure it does raise error on proper value.")


def get_tests_dir():
    return path.dirname(tests.__file__)


def exmpl_file():
    return u.full_pkg_file_path(u"data/utf8.txt", get_tests_dir)


def test__SegMdlFile():
    args = (u"foo", u"bar", u"baz.txt")
    exmpl = su.SegMdlFile(*args)

    assert(exmpl.name == args[0])
    assert(exmpl.type == args[1])
    assert(exmpl.filename == args[2])


@pytest.mark.parametrize("value",
                         [("foo", "bar", "baz.txt"),
                          ])
def test__tsegs_input_to_SegMdlFile(value):
    exmpl = su.tsegs_input_to_SegMdlFile(value)

    assert(exmpl.name == value[0])
    assert(exmpl.type == value[1])
    assert(exmpl.filename == value[2])


@pytest.mark.parametrize("value",
                         [(u"foo", u"bar", exmpl_file()),
                          v_error((u"foo", u"bar", u"fake_file.txt")),
                          ])
def test___validate_tsegs_filename(value):
    assert(tlz.pipe(value,
                    su.tsegs_input_to_SegMdlFile,
                    su._validate_tsegs_filename))


@pytest.mark.parametrize("value,modeltypes",
                         [((u"foo", u"bar", u"baz.txt"),
                           {u"bar", u"bar2"}),
                          k_error(((u"foo", u"bar", u"baz.txt"),
                                   {u"bar1", u"bar2"})),
                          ])
def test___validate_tsegs_modeltype(value, modeltypes):
    assert(tlz.pipe(value,
                    su.tsegs_input_to_SegMdlFile,
                    su._validate_tsegs_modeltype(modeltypes=modeltypes)))


@pytest.mark.parametrize("value,modeltypes",
                         [((u"foo", u"bar", exmpl_file()),
                           {u"bar", u"bar2"}),
                          k_error(((u"foo", u"bar", exmpl_file()),
                                   {u"bar1", u"bar2"})),
                          v_error(((u"foo", u"bar", u"baz.txt"),
                                   {u"bar", u"bar2"})),
                          ])
def test___validate_tsegs_input(value, modeltypes):
    assert(tlz.pipe(value,
                    su.tsegs_input_to_SegMdlFile,
                    su._validate_tsegs_input(modeltypes=modeltypes)))


@pytest.mark.parametrize("value,modeltypes",
                         [((u"foo", u"bar", exmpl_file()),
                           {u"bar", u"bar2"}),
                          k_error(((u"foo", u"bar", exmpl_file()),
                                   {u"bar1", u"bar2"})),
                          v_error(((u"foo", u"bar", u"baz.txt"),
                                   {u"bar", u"bar2"})),
                          ])
def test___proc_and_validate_tsegs_input(value, modeltypes):
    exmpl = su._proc_and_validate_tseg_input(value, modeltypes=modeltypes)

    assert(exmpl.name == value[0])
    assert(exmpl.type == value[1])
    assert(exmpl.filename == value[2])


@pytest.mark.parametrize("values,modeltypes",
                         [([(u"foo", u"bar", exmpl_file()),
                            (u"foo", u"bar", exmpl_file()),
                            (u"foo", u"bar", exmpl_file()),
                            ],
                           {u"bar", u"baz2"}),
                          ])
def test__proc_tsegs_option_input(values, modeltypes):
    assert(su.proc_tsegs_option_input(None, None, values, modeltypes=modeltypes))
