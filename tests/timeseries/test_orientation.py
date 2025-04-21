import pytest
from pydantic import ValidationError
from mt_metadata.timeseries.orientation_basemodel import (
    Orientation,
    MethodEnum,
    ReferenceFrameEnum,
    ValueEnum,
)


def test_orientation_default_values():
    """
    Test the default values of the Orientation model.
    """
    orientation = Orientation()

    assert orientation.method == MethodEnum.compass
    assert orientation.reference_frame == ReferenceFrameEnum.geographic
    assert orientation.angle_to_geographic_north is None
    assert orientation.value is None


def test_orientation_custom_values():
    """
    Test the Orientation model with custom values.
    """
    orientation = Orientation(
        method=MethodEnum.GPS,
        reference_frame=ReferenceFrameEnum.geomagnetic,
        angle_to_geographic_north=15.5,
        value=ValueEnum.orthogonal,
    )

    assert orientation.method == MethodEnum.GPS
    assert orientation.reference_frame == ReferenceFrameEnum.geomagnetic
    assert orientation.angle_to_geographic_north == 15.5
    assert orientation.value == ValueEnum.orthogonal


def test_orientation_partial_values():
    """
    Test the Orientation model with partial values.
    """
    orientation = Orientation(
        method=MethodEnum.theodolite,
        angle_to_geographic_north=0.0,
    )

    assert orientation.method == MethodEnum.theodolite
    assert orientation.reference_frame == ReferenceFrameEnum.geographic
    assert orientation.angle_to_geographic_north == 0.0
    assert orientation.value is None


def test_orientation_invalid_method():
    """
    Test the Orientation model with an invalid method value.
    """
    with pytest.raises(ValidationError):
        Orientation(method="invalid_method")  # Must be a valid MethodEnum value


def test_orientation_invalid_reference_frame():
    """
    Test the Orientation model with an invalid reference_frame value.
    """
    with pytest.raises(ValidationError):
        Orientation(
            reference_frame="invalid_frame"
        )  # Must be a valid ReferenceFrameEnum value


def test_orientation_invalid_angle_to_geographic_north():
    """
    Test the Orientation model with an invalid angle_to_geographic_north value.
    """
    with pytest.raises(ValidationError):
        Orientation(
            angle_to_geographic_north="invalid_angle"
        )  # Must be a float or None


def test_orientation_invalid_value():
    """
    Test the Orientation model with an invalid value.
    """
    with pytest.raises(ValidationError):
        Orientation(value="invalid_value")  # Must be a valid ValueEnum value
