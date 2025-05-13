# -*- coding: utf-8 -*-
"""
Tests for the BaseTranslator class using pytest.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import pytest


try:
    from obspy.core.inventory import Comment

    from mt_metadata.timeseries.stationxml.utils import BaseTranslator
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)


@pytest.fixture(scope="module")
def translator():
    """Return a BaseTranslator instance."""
    return BaseTranslator()


@pytest.fixture(scope="module")
def test_comments():
    """Return test comment objects."""
    return {
        "run_comment": Comment(
            "author: John Doe, comments: X array a 0 and 90 degrees.",
            subject="mt.run:b.metadata_by",
        ),
        "null_comment": Comment(None, subject="mt.survey.survey_id"),
        "long_comment": Comment("a: b, c: d, efg", subject="mt.run.a:comment"),
        "odd_comment": Comment("a: b: action, d: efg", subject="mt.run.odd"),
        "normal_comment": Comment("normal", subject="mt.run.comment"),
    }


@pytest.fixture(scope="module")
def test_doi():
    """Return a test DOI."""
    return [r"DOI:10.1234.mt/test"]


def test_null_comment(test_comments, subtests):
    """Test parsing a null comment."""
    k, v = BaseTranslator.read_xml_comment(test_comments["null_comment"])

    with subtests.test(msg="key equal"):
        assert k == "mt.survey.survey_id"

    with subtests.test(msg="value equal"):
        assert v == "None"


def test_run_comment(test_comments, subtests):
    """Test parsing a run comment."""
    k, v = BaseTranslator.read_xml_comment(test_comments["run_comment"])

    with subtests.test(msg="key equal"):
        assert k == "mt.run:b.metadata_by"

    with subtests.test(msg="is dict"):
        assert isinstance(v, dict)

    with subtests.test(msg="value equal"):
        assert v == {
            "author": "John Doe",
            "comments": "X array a 0 and 90 degrees.",
        }


def test_long_comment(test_comments, subtests):
    """Test parsing a long comment."""
    k, v = BaseTranslator.read_xml_comment(test_comments["long_comment"])

    with subtests.test(msg="key equal"):
        assert k == "mt.run.a:comment"

    with subtests.test(msg="is dict"):
        assert isinstance(v, dict)

    with subtests.test(msg="value equal"):
        assert v == {"a": "b", "c": "d, efg"}


def test_odd_comment(test_comments, translator, subtests):
    """Test parsing an odd comment."""
    k, v = translator.read_xml_comment(test_comments["odd_comment"])

    with subtests.test(msg="key equal"):
        assert k == "mt.run.odd"

    with subtests.test(msg="is dict"):
        assert isinstance(v, dict)

    with subtests.test(msg="value equal"):
        assert v == {"a": "b-- action", "d": "efg"}


def test_normal_comment(test_comments, translator, subtests):
    """Test parsing a normal comment."""
    k, v = translator.read_xml_comment(test_comments["normal_comment"])

    with subtests.test(msg="key equal"):
        assert k == "mt.run.comment"

    with subtests.test(msg="value equal"):
        assert v == "normal"


def test_flip_dict(translator):
    """Test flipping a dictionary."""
    original = {"a": "b", "c": "d", "e": None, "f": "special"}
    flipped = translator.flip_dict(original)
    assert flipped == {"b": "a", "d": "c"}


def test_read_identifier(translator, test_doi):
    """Test reading an identifier."""
    read_doi = translator.read_xml_identifier(test_doi)
    assert read_doi == "https://doi.org/10.1234.mt/test"
