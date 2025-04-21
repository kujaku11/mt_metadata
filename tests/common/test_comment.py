import pytest
from pydantic import ValidationError
from mt_metadata.common import Comment
from mt_metadata.utils.mttime import MTime


def test_comment_default_values():
    """
    Test the default values of the Comment model.
    """
    comment = Comment()

    assert comment.author is None
    assert comment.time_stamp.isoformat() == "1980-01-01T00:00:00+00:00"
    assert comment.value is None


def test_comment_custom_values():
    """
    Test the Comment model with custom values.
    """
    comment = Comment(
        author="J. Pedantic",
        time_stamp="2020-02-01T09:23:45.453670+00:00",
        value="failure at midnight.",
    )

    assert comment.author == "J. Pedantic"
    assert comment.time_stamp.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert comment.value == "failure at midnight."


def test_comment_invalid_time_stamp():
    """
    Test the Comment model with an invalid time_stamp value.
    """
    with pytest.raises(ValueError):
        Comment(
            author="J. Pedantic",
            time_stamp="invalid-time",
            value="failure at midnight.",
        )


def test_comment_to_dict():
    """
    Test the to_dict method of the Comment model.
    """
    comment = Comment(
        author="J. Pedantic",
        time_stamp="2020-02-01T09:23:45.453670+00:00",
        value="failure at midnight.",
    )

    result = comment.to_dict()
    assert (
        result
        == "2020-02-01T09:23:45.453670+00:00 | J. Pedantic | failure at midnight."
    )


def test_comment_from_dict_with_string():
    """
    Test the from_dict method with a string input.
    """
    comment = Comment()
    comment.from_dict(
        "2020-02-01T09:23:45.453670+00:00 | J. Pedantic | failure at midnight."
    )

    assert comment.author == "J. Pedantic"
    assert comment.time_stamp.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert comment.value == "failure at midnight."


def test_comment_from_dict_with_partial_string():
    """
    Test the from_dict method with a partial string input.
    """
    comment = Comment()
    comment.from_dict("2020-02-01T09:23:45.453670+00:00 | failure at midnight.")

    assert comment.author is None
    assert comment.time_stamp.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert comment.value == "failure at midnight."


def test_comment_from_dict_with_dict():
    """
    Test the from_dict method with a dictionary input.
    """
    comment = Comment()
    comment.from_dict(
        {
            "time_stamp": "2020-02-01T09:23:45.453670+00:00",
            "author": "J. Pedantic",
            "value": "failure at midnight.",
        }
    )

    assert comment.author == "J. Pedantic"
    assert comment.time_stamp.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert comment.value == "failure at midnight."


def test_comment_from_dict_with_invalid_type():
    """
    Test the from_dict method with an invalid input type.
    """
    comment = Comment()
    with pytest.raises(TypeError):
        comment.from_dict(12345)


def test_comment_partial_values():
    """
    Test the Comment model with partial values.
    """
    comment = Comment(author="J. Pedantic", value="failure at midnight.")

    assert comment.author == "J. Pedantic"
    assert comment.time_stamp.isoformat() == "1980-01-01T00:00:00+00:00"
    assert comment.value == "failure at midnight."


import pytest
from mt_metadata.common.comment_basemodel import Comment


def test_comment_to_dict_with_full_values():
    """
    Test the to_dict method with all fields set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == "2023-05-01T12:00:00+00:00 | J. Pedantic | This is a test comment."


def test_comment_to_dict_without_author():
    """
    Test the to_dict method when the author is not set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == "2023-05-01T12:00:00+00:00 |  | This is a test comment."


def test_comment_to_dict_without_time_stamp():
    """
    Test the to_dict method when the time_stamp is the default value.
    """
    comment = Comment(
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == " J. Pedantic | This is a test comment."


def test_comment_to_dict_without_author_and_time_stamp():
    """
    Test the to_dict method when both author and time_stamp are not set.
    """
    comment = Comment(value="This is a test comment.")

    result = comment.to_dict()
    assert result == "This is a test comment."


def test_comment_to_dict_with_none_value():
    """
    Test the to_dict method when the value is None.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value=None,
    )

    result = comment.to_dict()
    assert result is None


import pytest
from mt_metadata.common.comment_basemodel import Comment


def test_comment_to_dict_with_full_values():
    """
    Test the to_dict method with all fields set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == "2023-05-01T12:00:00+00:00 | J. Pedantic | This is a test comment."


def test_comment_to_dict_without_author():
    """
    Test the to_dict method when the author is not set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == "2023-05-01T12:00:00+00:00 | This is a test comment."


def test_comment_to_dict_without_time_stamp():
    """
    Test the to_dict method when the time_stamp is the default value.
    """
    comment = Comment(
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result == " J. Pedantic | This is a test comment."


def test_comment_to_dict_without_author_and_time_stamp():
    """
    Test the to_dict method when both author and time_stamp are not set.
    """
    comment = Comment(value="This is a test comment.")

    result = comment.to_dict()
    assert result == "This is a test comment."


def test_comment_to_dict_with_none_value():
    """
    Test the to_dict method when the value is None.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value=None,
    )

    result = comment.to_dict()
    assert result is None
