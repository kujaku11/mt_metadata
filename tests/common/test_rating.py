import pytest
from pydantic import ValidationError
from mt_metadata.common.rating_basemodel import Rating


def test_rating_default_values():
    """
    Test the default values of the Rating model.
    """
    rating = Rating()

    assert rating.author is None
    assert rating.method is None
    assert rating.value is None


def test_rating_custom_values():
    """
    Test the Rating model with custom values.
    """
    rating = Rating(
        author="gradstudent ace",
        method="standard deviation",
        value=4,
    )

    assert rating.author == "gradstudent ace"
    assert rating.method == "standard deviation"
    assert rating.value == 4


def test_rating_invalid_value_below_range():
    """
    Test the Rating model with a value below the valid range.
    """
    with pytest.raises(ValidationError):
        Rating(value=-1)  # Value must be between 0 and 5


def test_rating_invalid_value_above_range():
    """
    Test the Rating model with a value above the valid range.
    """
    with pytest.raises(ValidationError):
        Rating(value=6)  # Value must be between 0 and 5


def test_rating_partial_values():
    """
    Test the Rating model with partial values.
    """
    rating = Rating(value=3)

    assert rating.author is None
    assert rating.method is None
    assert rating.value == 3


def test_rating_invalid_author_type():
    """
    Test the Rating model with an invalid author type.
    """
    with pytest.raises(ValidationError):
        Rating(author=True)  # Author must be a string or None


def test_rating_invalid_method_type():
    """
    Test the Rating model with an invalid method type.
    """
    with pytest.raises(ValidationError):
        Rating(method=True)  # Method must be a string or None
