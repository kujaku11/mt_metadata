# -*- coding: utf-8 -*-
"""
Tests for filter renaming functionality using pytest.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

from collections import OrderedDict

import numpy as np
import pytest

try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_01
from mt_metadata.timeseries.filters import PoleZeroFilter
from mt_metadata.timeseries.stationxml import XMLChannelMTChannel


@pytest.fixture(scope="module")
def inventory():
    """Create and return an inventory with cleared filter names."""
    inv = read_inventory(STATIONXML_01.as_posix())
    # Clear all stage names
    for ch in inv.networks[0].stations[0].channels:
        for stage in ch.response.response_stages:
            stage.name = ""
    return inv


@pytest.fixture(scope="module")
def converter():
    """Create an XMLChannelMTChannel converter."""
    return XMLChannelMTChannel()


@pytest.fixture(scope="module")
def sample_filter():
    """Create a sample PoleZeroFilter."""
    return PoleZeroFilter(
        **OrderedDict(
            [
                ("calibration_date", "1980-01-01"),
                ("comments", "butterworth filter"),
                ("gain", 1.0),
                ("name", "zpk_00"),
                ("normalization_factor", 1984.31439386406),
                (
                    "poles",
                    np.array(
                        [
                            -6.283185 + 10.882477j,
                            -6.283185 - 10.882477j,
                            -12.566371 + 0.0j,
                        ]
                    ),
                ),
                ("type", "zpk"),
                ("units_in", "nT"),
                ("units_out", "V"),
                ("zeros", np.array([], dtype="complex128")),
            ]
        )
    )


@pytest.fixture(scope="module")
def existing_filters(sample_filter):
    """Create a dictionary of existing filters."""
    return {sample_filter.name: sample_filter}


@pytest.fixture(scope="module")
def converted_channel(inventory, converter):
    """Convert the first channel and return both channel and filter dict."""
    return converter.xml_to_mt(inventory.networks[0].stations[0].channels[0])


def test_rename_filters(converted_channel, subtests):
    """Test that filters are renamed correctly when converting from XML to MT."""
    mt_ch, ch_filter_dict = converted_channel

    with subtests.test(msg="filter count"):
        assert len(ch_filter_dict) == 3

    with subtests.test(msg="filter names"):
        expected_names = sorted(["zpk_00", "coefficient_00", "time delay_00"])
        actual_names = sorted(ch_filter_dict.keys())
        assert actual_names == expected_names


def test_filter_exists(converter, existing_filters, sample_filter, subtests):
    """Test handling of an existing filter with the same name."""
    name, new = converter._add_filter_number(existing_filters, sample_filter)

    with subtests.test(msg="name unchanged"):
        assert name == sample_filter.name

    with subtests.test(msg="not marked as new"):
        assert new is False


def test_filter_new_name(converter, existing_filters, subtests):
    """Test adding a filter with a name collision that needs renaming."""
    # Create a new filter with same base name but different attributes
    new_filter = PoleZeroFilter(
        name="zpk_00",
        gain=2.0,  # Different gain than the sample filter
        units_in="V",
        units_out="count",
        poles=np.array([-5.0 + 8.0j, -5.0 - 8.0j]),
        zeros=np.array([]),
    )

    name, new = converter._add_filter_number(existing_filters, new_filter)

    with subtests.test(msg="name incremented"):
        assert name == "zpk_01"

    with subtests.test(msg="marked as new"):
        assert new is True


def test_multiple_filter_renaming(converter, subtests):
    """Test adding multiple filters with the same base name."""
    filters = {}

    # Create three similar filters
    base_params = {
        "gain": 1.0,
        "units_in": "nT",
        "units_out": "V",
        "poles": np.array([-1.0 + 2.0j, -1.0 - 2.0j]),
        "zeros": np.array([]),
    }

    filter_params = []
    for i in range(3):
        params = base_params.copy()
        params["name"] = "test_filter"
        params["gain"] = float((i + 1) * 10)  # Make each filter slightly different
        filter_params.append(params)

    expected_names = []

    for params in filter_params:
        filt = PoleZeroFilter(**params)
        name, _ = converter._add_filter_number(filters, filt)
        filters[name] = filt
        expected_names.append(name)

    with subtests.test(msg="first filter name"):
        assert expected_names[0] == "zpk_00"

    with subtests.test(msg="second filter name"):
        assert expected_names[1] == "zpk_01"

    with subtests.test(msg="third filter name"):
        assert expected_names[2] == "test_filter"

    with subtests.test(msg="filter count"):
        assert len(filters) == 3


def test_identical_filter_reuse(converter, subtests):
    """Test that identical filters are reused rather than duplicated."""
    filters = {}

    # Create two identical filters
    base_params = {
        "name": "identical_filter",
        "gain": 1.0,
        "units_in": "nT",
        "units_out": "V",
        "poles": np.array([-1.0 + 2.0j, -1.0 - 2.0j]),
        "zeros": np.array([]),
    }

    # First filter should get a new name
    filt1 = PoleZeroFilter(**base_params)
    name1, is_new1 = converter._add_filter_number(filters, filt1)
    filters[name1] = filt1

    # Second identical filter should reuse the name
    filt2 = PoleZeroFilter(**base_params)
    name2, is_new2 = converter._add_filter_number(filters, filt2)

    with subtests.test(msg="first filter renamed"):
        assert name1 == "zpk_00"

    with subtests.test(msg="first filter is new"):
        assert is_new1 is True

    with subtests.test(msg="second filter name matches first"):
        assert name2 == filt1.name

    with subtests.test(msg="second filter is not new"):
        assert is_new2 is False
