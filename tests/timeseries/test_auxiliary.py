import pytest
from mt_metadata.timeseries import Auxiliary, Channel

# File: mt_metadata/timeseries/test_auxiliary_basemodel.py


@pytest.fixture
def auxiliary_instance():
    """Fixture to create an instance of Auxiliary."""
    return Auxiliary()


def test_auxiliary_initialization(auxiliary_instance):
    """Test that the Auxiliary class initializes correctly."""
    assert isinstance(auxiliary_instance, Auxiliary)


def test_auxiliary_inherits_channel(auxiliary_instance):
    """Test that Auxiliary class inherits from Channel."""
    assert isinstance(auxiliary_instance, Channel)


def test_auxiliary_default_fields(auxiliary_instance):
    """Test default fields of Auxiliary class."""
    # Assuming Auxiliary inherits fields from Channel, check for expected defaults
    # Replace 'field_name' with actual field names if applicable
    assert hasattr(auxiliary_instance, "component")  # Example placeholder
