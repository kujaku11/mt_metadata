import pytest
from mt_metadata.common.declination import Declination, ModelEnum
from mt_metadata.common import Comment


def test_declination_default_values():
    """
    Test the default values of the Declination model.
    """
    declination = Declination()

    assert declination.comments == Comment()
    assert declination.model == ModelEnum.IGRF
    assert declination.epoch is None
    assert declination.value == 0.0


def test_declination_custom_values():
    """
    Test the Declination model with custom values.
    """
    declination = Declination(
        comments="estimated from WMM 2020",
        model=ModelEnum.WMM,
        epoch="2020",
        value=12.3,
    )

    assert declination.comments.value == "estimated from WMM 2020"
    assert declination.model == ModelEnum.WMM
    assert declination.epoch == "2020"
    assert declination.value == 12.3


def test_declination_invalid_model():
    """
    Test the Declination model with an invalid model value.
    """
    with pytest.raises(ValueError):
        Declination(model="INVALID_MODEL")


def test_declination_invalid_value():
    """
    Test the Declination model with an invalid value type.
    """
    with pytest.raises(ValueError):
        Declination(value="invalid")


def test_declination_validate_comments_with_string():
    """
    Test the validate_comments method with a string input.
    """
    declination = Declination(comments="This is a test comment.")
    assert isinstance(declination.comments, Comment)
    assert declination.comments.value == "This is a test comment."


def test_declination_validate_comments_with_comment_object():
    """
    Test the validate_comments method with a Comment object.
    """
    comment = Comment(value="This is a test comment.")
    declination = Declination(comments=comment)
    assert declination.comments == comment


def test_declination_partial_values():
    """
    Test the Declination model with partial values.
    """
    declination = Declination(model=ModelEnum.EMM, value=5.5)

    assert declination.comments == Comment()
    assert declination.model == ModelEnum.EMM
    assert declination.epoch is None
    assert declination.value == 5.5
