import pytest

from mt_metadata.common import Comment, Rating
from mt_metadata.common.data_quality import DataQuality


def test_data_quality_default_values():
    """
    Test the default values of the DataQuality model.
    """
    data_quality = DataQuality()

    assert data_quality.warnings is None
    assert data_quality.good_from_period is None
    assert data_quality.good_to_period is None
    assert data_quality.flag is None
    assert isinstance(data_quality.comments, Comment)
    assert data_quality.comments.value == None
    assert isinstance(data_quality.rating, Rating)


def test_data_quality_custom_values():
    """
    Test the DataQuality model with custom values.
    """
    data_quality = DataQuality(
        warnings="periodic pipeline noise",
        good_from_period=0.01,
        good_to_period=1000.0,
        flag=1,
        comments="Data quality is acceptable.",
        rating=Rating(value=4),
    )

    assert data_quality.warnings == "periodic pipeline noise"
    assert data_quality.good_from_period == 0.01
    assert data_quality.good_to_period == 1000.0
    assert data_quality.flag == 1
    assert isinstance(data_quality.comments, Comment)
    assert data_quality.comments.value == "Data quality is acceptable."
    assert isinstance(data_quality.rating, Rating)
    assert data_quality.rating.value == 4


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
    assert isinstance(data_quality.comments, Comment)
    assert data_quality.comments.value == "Only partial data available."
    assert isinstance(data_quality.rating, Rating)


def test_data_quality_invalid_good_from_period():
    """
    Test the DataQuality model with an invalid good_from_period value.
    """
    with pytest.raises(ValueError):
        DataQuality(good_from_period="invalid")  # Must be a float or None


def test_data_quality_invalid_good_to_period():
    """
    Test the DataQuality model with an invalid good_to_period value.
    """
    with pytest.raises(ValueError):
        DataQuality(good_to_period="invalid")  # Must be a float or None


def test_data_quality_invalid_flag():
    """
    Test the DataQuality model with an invalid flag value.
    """
    with pytest.raises(ValueError):
        DataQuality(flag="invalid")  # Must be an integer or None


def test_data_quality_validate_comments_with_string():
    """
    Test the validate_comments method with a string input.
    """
    data_quality = DataQuality(comments="This is a test comment.")

    assert isinstance(data_quality.comments, Comment)
    assert data_quality.comments.value == "This is a test comment."


def test_data_quality_validate_comments_with_comment_object():
    """
    Test the validate_comments method with a Comment object.
    """
    comment = Comment(value="This is a test comment.")
    data_quality = DataQuality(comments=comment)

    assert data_quality.comments == comment


def test_data_quality_invalid_comments():
    """
    Test the DataQuality model with an invalid comments value.
    """
    with pytest.raises(ValueError):
        DataQuality(comments=[])  # Must be a string or a Comment object


def test_data_quality_rating_with_custom_value():
    """
    Test the DataQuality model with a custom rating value.
    """
    rating = Rating(value=5)
    data_quality = DataQuality(rating=rating)

    assert isinstance(data_quality.rating, Rating)
    assert data_quality.rating.value == 5
