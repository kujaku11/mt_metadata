# -*- coding: utf-8 -*-
"""
Test FAP (Frequency-Amplitude-Phase) tables using pytest.

These tests validate conversion between ObsPy StationXML and MT metadata formats
for frequency response table filters.
"""

import numpy as np
import pytest

try:
    from obspy.core import inventory

    from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_FAP
from mt_metadata.common.units import get_unit_object
from mt_metadata.timeseries.filters import FrequencyResponseTableFilter
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment

# --- Fixtures ---


@pytest.fixture(scope="module")
def base_inventory():
    """Load FAP test base_inventory from file."""
    return inventory.read_inventory(STATIONXML_FAP.as_posix())


@pytest.fixture(scope="module")
def fap_stage(base_inventory):
    """Extract FAP stage from base_inventory."""
    return (
        base_inventory.networks[0].stations[0].channels[0].response.response_stages[0]
    )


@pytest.fixture(scope="module")
def instrument_sensitivity(base_inventory):
    """Extract instrument sensitivity from base_inventory."""
    return (
        base_inventory.networks[0]
        .stations[0]
        .channels[0]
        .response.instrument_sensitivity
    )


@pytest.fixture(scope="module")
def fap_filter(fap_stage):
    """Create frequency response filter from FAP stage."""
    return create_filter_from_stage(fap_stage)


@pytest.fixture(scope="module")
def translator():
    """Create FAP translator instance."""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def experiment(translator, base_inventory):
    """Convert base_inventory to MT experiment."""
    return translator.xml_to_mt(base_inventory)


@pytest.fixture(scope="module")
def new_inventory(translator, experiment):
    """Convert MT experiment back to base_inventory."""
    return translator.mt_to_xml(experiment)


@pytest.fixture(scope="module")
def mt_fap(experiment):
    """Get FAP filter from experiment."""
    return experiment.surveys[0].filters["frequency response table_00"]


# --- Test Classes ---


class TestFAPFilter:
    """Test filter translation from ObsPy response stage to MT filter."""

    def test_is_fap_instance(self, fap_filter):
        """Test if the created filter is a FrequencyResponseTableFilter."""
        assert isinstance(fap_filter, FrequencyResponseTableFilter)

    def test_amplitudes(self, fap_stage, fap_filter):
        """Test if amplitudes are correctly transferred."""
        assert np.all(np.isclose(fap_stage.amplitudes, fap_filter.amplitudes))

    def test_phases(self, fap_stage, fap_filter):
        """Test if phases are correctly transferred with radian conversion."""
        assert np.all(np.isclose(np.deg2rad(fap_stage.phases), fap_filter.phases))

    def test_frequencies(self, fap_stage, fap_filter):
        """Test if frequencies are correctly transferred."""
        assert np.all(np.isclose(fap_stage.frequencies, fap_filter.frequencies))

    def test_units_in(self, fap_stage, fap_filter):
        """Test if input units are correctly transferred."""
        assert fap_stage.input_units == get_unit_object(fap_filter.units_in).symbol

    def test_units_out(self, fap_stage, fap_filter):
        """Test if output units are correctly transferred."""
        assert fap_stage.output_units == get_unit_object(fap_filter.units_out).symbol

    def test_comments(self, fap_stage, fap_filter):
        """Test if description is transferred to comments."""
        assert fap_stage.description == fap_filter.comments

    def test_gain(self, fap_stage, fap_filter):
        """Test if stage gain is correctly transferred."""
        assert fap_stage.stage_gain == fap_filter.gain


class TestFAPTranslation:
    """Test the translation of a FAP table from stationXML -> MTXML -> StationXML."""

    def test_has_surveys(self, base_inventory, experiment, subtests):
        """Test if surveys are correctly created."""
        with subtests.test("length equal"):
            assert len(base_inventory.networks) == len(experiment.surveys)

        with subtests.test("codes equal"):
            assert base_inventory.networks[0].code == experiment.surveys[0].fdsn.network

    def test_has_stations(self, base_inventory, experiment, subtests):
        """Test if stations are correctly created."""
        with subtests.test("length equal"):
            assert len(base_inventory.networks[0].stations) == len(
                experiment.surveys[0].stations
            )

        with subtests.test("codes equal"):
            assert (
                base_inventory.networks[0].stations[0].code
                == experiment.surveys[0].stations[0].fdsn.id
            )

    def test_has_channels(self, base_inventory, experiment):
        """Test if channels are correctly created."""
        assert len(base_inventory.networks[0].stations[0].channels) == len(
            experiment.surveys[0].stations[0].runs[0].channels
        )

    def test_has_filters(self, experiment):
        """Test if filters are correctly created."""
        filters = experiment.surveys[0].filters

        assert "frequency response table_00" in filters.keys()
        assert "v to counts (electric)" in filters.keys()

    def test_translation_fap_elements(self, base_inventory, new_inventory, subtests):
        """Test if FAP elements are preserved in round-trip conversion."""
        fap_0 = (
            base_inventory.networks[0]
            .stations[0]
            .channels[0]
            .response.response_stages[0]
        )
        fap_1 = (
            new_inventory.networks[0]
            .stations[0]
            .channels[0]
            .response.response_stages[0]
        )

        fap_elements_0 = fap_0.response_list_elements
        fap_elements_1 = fap_1.response_list_elements

        assert len(fap_elements_0) == len(fap_elements_1)

        # Extract arrays for efficient comparison
        frequencies_0 = np.array([elem.frequency for elem in fap_elements_0])
        frequencies_1 = np.array([elem.frequency for elem in fap_elements_1])
        amplitudes_0 = np.array([elem.amplitude for elem in fap_elements_0])
        amplitudes_1 = np.array([elem.amplitude for elem in fap_elements_1])
        phases_0 = np.array([np.deg2rad(elem.phase) for elem in fap_elements_0])
        phases_1 = np.array([elem.phase for elem in fap_elements_1])

        # Batch assertions for all elements at once
        with subtests.test("frequencies"):
            assert np.allclose(
                frequencies_0, frequencies_1
            ), "Frequency arrays do not match"

        with subtests.test("amplitudes"):
            assert np.allclose(
                amplitudes_0, amplitudes_1
            ), "Amplitude arrays do not match"

        with subtests.test("phases"):
            assert np.allclose(phases_0, phases_1), "Phase arrays do not match"

    def test_mt_translation_fap_elements(self, base_inventory, mt_fap, subtests):
        """Test if FAP elements are correctly translated to MT format."""
        fap = (
            base_inventory.networks[0]
            .stations[0]
            .channels[0]
            .response.response_stages[0]
        )
        fap_elements = fap.response_list_elements

        assert len(fap_elements) == mt_fap.frequencies.size

        for ii, element_1 in enumerate(fap_elements):
            with subtests.test("frequency"):
                assert element_1.frequency == mt_fap.frequencies[ii]

            with subtests.test("amplitude"):
                assert element_1.amplitude == mt_fap.amplitudes[ii]

            with subtests.test("phase"):
                assert np.deg2rad(element_1.phase) == mt_fap.phases[ii]
