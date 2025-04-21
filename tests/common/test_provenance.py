import pytest
import numpy as np
import pandas as pd
from mt_metadata.common import Provenance, Person, Software
from mt_metadata.utils.mttime import MTime
from pydantic import ValidationError


def test_provenance_default_values():
    """
    Test the default values of the Provenance model.
    """
    provenance = Provenance()

    assert isinstance(provenance.creation_time, MTime)
    assert provenance.creation_time.isoformat() == "1980-01-01T00:00:00+00:00"
    assert provenance.comments.value is None
    assert provenance.log is None
    assert isinstance(provenance.creator, Person)
    assert isinstance(provenance.submitter, Person)
    assert isinstance(provenance.archive, Person)
    assert isinstance(provenance.software, Software)


def test_provenance_custom_values():
    """
    Test the Provenance model with custom values.
    """
    provenance = Provenance(
        creation_time="2023-05-01T12:00:00+00:00",
        comments="Data created for testing.",
        log="2023-05-02T14:00:00+00:00 updated metadata",
        creator=Person(name="J. Pedantic", email="jped@mt.com"),
        submitter=Person(name="Submitter Name", email="submitter@email.com"),
        archive=Person(name="Archive Name", url="https://archive.url"),
        software=Software(name="mt_metadata", version="0.1"),
    )

    assert provenance.creation_time.isoformat() == "2023-05-01T12:00:00+00:00"
    assert provenance.comments == "Data created for testing."
    assert provenance.log == "2023-05-02T14:00:00+00:00 updated metadata"
    assert provenance.creator.name == "J. Pedantic"
    assert provenance.creator.email == "jped@mt.com"
    assert provenance.submitter.name == "Submitter Name"
    assert provenance.submitter.email == "submitter@email.com"
    assert provenance.archive.name == "Archive Name"
    assert provenance.archive.url.unicode_string() == "https://archive.url/"
    assert provenance.software.name == "mt_metadata"
    assert provenance.software.version == "0.1"


def test_provenance_invalid_creation_time():
    """
    Test the Provenance model with an invalid creation_time value.
    """
    with pytest.raises(ValidationError):
        Provenance(creation_time="invalid-date")


def test_provenance_creation_time_with_epoch():
    """
    Test the Provenance model with creation_time as an epoch time.
    """
    provenance = Provenance(
        creation_time=1682942400.0
    )  # Epoch time for 2023-05-01T12:00:00+00:00

    assert provenance.creation_time.isoformat() == "2023-05-01T12:00:00+00:00"


def test_provenance_creation_time_with_np_datetime64():
    """
    Test the Provenance model with creation_time as a numpy datetime64.
    """
    provenance = Provenance(creation_time=np.datetime64("2023-05-01T12:00:00+00:00"))

    assert provenance.creation_time.isoformat() == "2023-05-01T12:00:00+00:00"


def test_provenance_creation_time_with_pd_timestamp():
    """
    Test the Provenance model with creation_time as a pandas Timestamp.
    """
    provenance = Provenance(creation_time=pd.Timestamp("2023-05-01T12:00:00+00:00"))

    assert provenance.creation_time.isoformat() == "2023-05-01T12:00:00+00:00"


def test_provenance_partial_values():
    """
    Test the Provenance model with partial values.
    """
    provenance = Provenance(
        comments="Partial data",
        creator=Person(name="J. Pedantic"),
    )

    assert provenance.comments.value == "Partial data"
    assert provenance.creator.name == "J. Pedantic"
    assert provenance.creator.email is None
    assert provenance.submitter.name == ""
    assert provenance.archive.name == ""
    assert provenance.software.name == ""


def test_provenance_invalid_creator_type():
    """
    Test the Provenance model with an invalid creator type.
    """
    with pytest.raises(ValidationError):
        Provenance(creator="invalid_creator")  # Creator must be a Person object


def test_provenance_invalid_software_type():
    """
    Test the Provenance model with an invalid software type.
    """
    with pytest.raises(ValidationError):
        Provenance(software="invalid_software")  # Software must be a Software object
