import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import (
    ChannelOrientationEnum,
    GeographicReferenceFrameEnum,
    OrientationMethodEnum,
)
from mt_metadata.common.orientation import Orientation


@pytest.fixture
def default_orientation():
    """Fixture to create a default Orientation object."""
    return Orientation()


@pytest.fixture
def custom_orientation():
    """Fixture to create a custom Orientation object."""
    return Orientation(
        method=OrientationMethodEnum.compass,
        reference_frame=GeographicReferenceFrameEnum.geographic,
        angle_to_geographic_north=15.0,
        value=ChannelOrientationEnum.orthogonal,
    )


def test_default_orientation(default_orientation, subtests):
    """Test the default values of the Orientation model."""
    with subtests.test("Default method"):
        assert default_orientation.method == OrientationMethodEnum.compass

    with subtests.test("Default reference frame"):
        assert (
            default_orientation.reference_frame
            == GeographicReferenceFrameEnum.geographic
        )

    with subtests.test("Default angle to geographic north"):
        assert default_orientation.angle_to_geographic_north is None

    with subtests.test("Default value"):
        assert default_orientation.value == ChannelOrientationEnum.orthogonal


def test_custom_orientation(custom_orientation, subtests):
    """Test a custom Orientation object."""
    with subtests.test("Custom method"):
        assert custom_orientation.method == OrientationMethodEnum.compass

    with subtests.test("Custom reference frame"):
        assert (
            custom_orientation.reference_frame
            == GeographicReferenceFrameEnum.geographic
        )

    with subtests.test("Custom angle to geographic north"):
        assert custom_orientation.angle_to_geographic_north == 15.0

    with subtests.test("Custom value"):
        assert custom_orientation.value == ChannelOrientationEnum.orthogonal


def test_invalid_orientation_method(subtests):
    """Test invalid method for Orientation."""
    with subtests.test("Invalid method"):
        with pytest.raises(ValidationError):
            Orientation(method="invalid_method")


def test_invalid_reference_frame(subtests):
    """Test invalid reference frame for Orientation."""
    with subtests.test("Invalid reference frame"):
        with pytest.raises(ValidationError):
            Orientation(reference_frame="invalid_frame")


def test_invalid_angle_to_geographic_north(subtests):
    """Test invalid angle to geographic north."""
    with subtests.test("Non-numeric angle"):
        with pytest.raises(ValidationError):
            Orientation(angle_to_geographic_north="not_a_number")

    with subtests.test("Negative angle"):
        orientation = Orientation(angle_to_geographic_north=-10.0)
        assert orientation.angle_to_geographic_north == -10.0


def test_invalid_channel_orientation(subtests):
    """Test invalid channel orientation."""
    with subtests.test("Invalid channel orientation"):
        with pytest.raises(ValidationError):
            Orientation(value="invalid_orientation")
