import pytest
from pydantic import ValidationError

from mt_metadata.common import Fdsn


def test_fdsn_default_values():
    """
    Test the default values of the Fdsn model.
    """
    fdsn = Fdsn()

    assert fdsn.id is None
    assert fdsn.network is None
    assert fdsn.channel_code is None
    assert fdsn.new_epoch is None
    assert fdsn.alternate_code is None
    assert fdsn.alternate_network_code is None


def test_fdsn_custom_values():
    """
    Test the Fdsn model with custom values.
    """
    fdsn = Fdsn(
        id="MT001",
        network="EM",
        channel_code="LQN",
        new_epoch=True,
        alternate_code="_US-MT",
        alternate_network_code="_INT-NON_FDSN",
    )

    assert fdsn.id == "MT001"
    assert fdsn.network == "EM"
    assert fdsn.channel_code == "LQN"
    assert fdsn.new_epoch is True
    assert fdsn.alternate_code == "_US-MT"
    assert fdsn.alternate_network_code == "_INT-NON_FDSN"


def test_fdsn_invalid_id():
    """
    Test the Fdsn model with an invalid id.
    """
    with pytest.raises(ValidationError):
        Fdsn(id="MT@001")  # Invalid character in id


def test_fdsn_invalid_network():
    """
    Test the Fdsn model with an invalid network code.
    """
    with pytest.raises(ValidationError):
        Fdsn(network="EM1")  # Network code must be exactly 2 alphanumeric characters


def test_fdsn_invalid_channel_code():
    """
    Test the Fdsn model with an invalid channel code.
    """
    with pytest.raises(ValidationError):
        Fdsn(
            channel_code="LQ"
        )  # Channel code must be exactly 3 alphanumeric characters


def test_fdsn_partial_values():
    """
    Test the Fdsn model with partial values.
    """
    fdsn = Fdsn(
        id="MT002",
        network="US",
    )

    assert fdsn.id == "MT002"
    assert fdsn.network == "US"
    assert fdsn.channel_code is None
    assert fdsn.new_epoch is None
    assert fdsn.alternate_code is None
    assert fdsn.alternate_network_code is None


def test_fdsn_invalid_new_epoch():
    """
    Test the Fdsn model with an invalid new_epoch value.
    """
    with pytest.raises(ValidationError):
        Fdsn(new_epoch="invalid")  # new_epoch must be a boolean


def test_fdsn_invalid_alternate_code():
    """
    Test the Fdsn model with an invalid alternate_code.
    """
    with pytest.raises(ValidationError):
        Fdsn(alternate_code=[])  # alternate_code must be a string or None


def test_fdsn_invalid_alternate_network_code():
    """
    Test the Fdsn model with an invalid alternate_network_code.
    """
    with pytest.raises(ValidationError):
        Fdsn(
            alternate_network_code=[]
        )  # alternate_network_code must be a string or None
