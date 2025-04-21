import pytest
from mt_metadata.timeseries import DataQuality


def test_data_quality_default_values():
    """
    Test the default values of the DataQuality model.
    """
    data_quality = DataQuality()

    assert data_quality.warnings is None
    assert data_quality.good_from_period is None
    assert data_quality.good_to_period is None
    assert data_quality.flag is None
    assert data_quality.comments is None


def test_data_quality_custom_values():
    """
    Test the DataQuality model with custom values.
    """
    data_quality = DataQuality(
        warnings="periodic pipeline noise",
        good_from_period=0.01,
        good_to_period=1000,
        flag=1,
        comments="Data quality is acceptable.",
    )

    assert data_quality.warnings == "periodic pipeline noise"
    assert data_quality.good_from_period == 0.01
    assert data_quality.good_to_period == 1000
    assert data_quality.flag == 1
    assert data_quality.comments == "Data quality is acceptable."


def test_data_quality_partial_values():
    """
    Test the DataQuality model with partial values.
    """
    data_quality = DataQuality(
        good_from_period=0.1,
        comments="Only partial data available.",
    )

    assert data_quality.warnings is None
    assert data_quality.good_from_period == 0.1
    assert data_quality.good_to_period is None
    assert data_quality.flag is None
    assert data_quality.comments == "Only partial data available."


def test_data_quality_invalid_values():
    """
    Test the DataQuality model with invalid values.
    """
    with pytest.raises(ValueError):
        DataQuality(good_from_period="invalid")

    with pytest.raises(ValueError):
        DataQuality(good_to_period="invalid")

    with pytest.raises(ValueError):
        DataQuality(flag="invalid")


def test_data_quality_edge_cases():
    """
    Test the DataQuality model with edge case values.
    """
    data_quality = DataQuality(
        good_from_period=0.0,
        good_to_period=float("inf"),
        flag=0,
    )

    assert data_quality.good_from_period == 0.0
    assert data_quality.good_to_period == float("inf")
    assert data_quality.flag == 0
