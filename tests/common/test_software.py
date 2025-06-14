import pytest
import numpy as np
import pandas as pd
from mt_metadata.common import Software
from mt_metadata.utils.mttime import MTime


def test_software_default_values():
    """
    Test the default values of the Software model.
    """
    software = Software()

    assert software.author == ""
    assert software.version == ""
    assert software.name == ""
    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "1980-01-01T00:00:00+00:00"


def test_software_custom_values():
    """
    Test the Software model with custom values.
    """
    software = Software(
        author="Neo",
        version="12.01a",
        name="mtrules",
        last_updated="2023-05-01T12:00:00+00:00",
    )

    assert software.author == "Neo"
    assert software.version == "12.01a"
    assert software.name == "mtrules"
    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "2023-05-01T12:00:00+00:00"


def test_software_invalid_last_updated():
    """
    Test the Software model with an invalid last_updated value.
    """
    with pytest.raises(ValueError):
        Software(last_updated="invalid-date")


def test_software_last_updated_with_epoch():
    """
    Test the Software model with last_updated as an epoch time.
    """
    software = Software(
        last_updated=1682942400.0
    )  # Epoch time for 2023-05-01T12:00:00+00:00

    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "2023-05-01T12:00:00+00:00"


def test_software_last_updated_with_np_datetime64():
    """
    Test the Software model with last_updated as a numpy datetime64.
    """
    software = Software(last_updated=np.datetime64("2023-05-01T12:00:00+00:00"))

    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "2023-05-01T12:00:00+00:00"


def test_software_last_updated_with_pd_timestamp():
    """
    Test the Software model with last_updated as a pandas Timestamp.
    """
    software = Software(last_updated=pd.Timestamp("2023-05-01T12:00:00+00:00"))

    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "2023-05-01T12:00:00+00:00"


def test_software_partial_values():
    """
    Test the Software model with partial values.
    """
    software = Software(author="Trinity", name="mttools")

    assert software.author == "Trinity"
    assert software.version == ""
    assert software.name == "mttools"
    assert isinstance(software.last_updated, MTime)
    assert software.last_updated.isoformat() == "1980-01-01T00:00:00+00:00"
