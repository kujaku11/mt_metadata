import pytest

from mt_metadata.common import Comment


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
    expected = {
        "comment": {
            "author": "J. Pedantic",
            "time_stamp": "2020-02-01T09:23:45.453670+00:00",
            "value": "failure at midnight.",
        }
    }
    assert result["comment"]["author"] == expected["comment"]["author"]
    assert result["comment"]["time_stamp"] == expected["comment"]["time_stamp"]
    assert result["comment"]["value"] == expected["comment"]["value"]


def test_comment_as_string():
    """
    Test the as_string method of the Comment model.
    """
    comment = Comment(
        author="J. Pedantic",
        time_stamp="2020-02-01T09:23:45.453670+00:00",
        value="failure at midnight.",
    )

    result = comment.as_string()
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


def test_comment_as_string_with_full_values():
    """
    Test the as_string method with all fields set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.as_string()
    assert result == "2023-05-01T12:00:00+00:00 | J. Pedantic | This is a test comment."


def test_comment_as_string_without_author():
    """
    Test the as_string method when the author is not set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        value="This is a test comment.",
    )

    result = comment.as_string()
    assert result == "2023-05-01T12:00:00+00:00 | This is a test comment."


def test_comment_as_string_without_time_stamp():
    """
    Test the as_string method when the time_stamp is the default value.
    """
    comment = Comment(
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.as_string()
    assert result == " J. Pedantic | This is a test comment."


def test_comment_as_string_without_author_and_time_stamp():
    """
    Test the as_string method when both author and time_stamp are not set.
    """
    comment = Comment(value="This is a test comment.")

    result = comment.as_string()
    assert result == "This is a test comment."


def test_comment_as_string_with_none_value():
    """
    Test the as_string method when the value is None.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value=None,
    )

    result = comment.as_string()
    assert result == ""


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
    assert result["comment"]["author"] == "J. Pedantic"
    assert result["comment"]["time_stamp"] == "2023-05-01T12:00:00+00:00"
    assert result["comment"]["value"] == "This is a test comment."


def test_comment_to_dict_without_author():
    """
    Test the to_dict method when the author is not set.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    # Author should not be in the dict when it's None (required=True by default)
    assert result["comment"]["time_stamp"] == "2023-05-01T12:00:00+00:00"
    assert result["comment"]["value"] == "This is a test comment."


def test_comment_to_dict_without_time_stamp():
    """
    Test the to_dict method when the time_stamp is the default value.
    """
    comment = Comment(
        author="J. Pedantic",
        value="This is a test comment.",
    )

    result = comment.to_dict()
    assert result["comment"]["author"] == "J. Pedantic"
    # Default timestamp should not be included when required=True (default)
    assert result["comment"]["value"] == "This is a test comment."


def test_comment_to_dict_without_author_and_time_stamp():
    """
    Test the to_dict method when both author and time_stamp are not set.
    """
    comment = Comment(value="This is a test comment.")

    result = comment.to_dict()
    assert result["comment"]["value"] == "This is a test comment."


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
    assert result["comment"]["author"] == "J. Pedantic"
    assert result["comment"]["time_stamp"] == "2023-05-01T12:00:00+00:00"
    # None values might be excluded from to_dict


def test_comment_eq_with_identical_objects():
    """
    Test __eq__ with two identical Comment objects.
    """
    comment1 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )
    comment2 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )

    assert comment1 == comment2


def test_comment_eq_with_different_objects():
    """
    Test __eq__ with two different Comment objects.
    """
    comment1 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )
    comment2 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a different comment.",
    )

    assert comment1 != comment2


def test_comment_eq_with_string():
    """
    Test __eq__ with a Comment object and a string.
    """
    comment = Comment(
        value="This is a test comment.",
    )
    string = "This is a test comment."

    assert comment == string


def test_comment_eq_with_non_comment_object():
    """
    Test __eq__ with a Comment object and a non-Comment object.
    """
    comment = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )
    non_comment = {"time_stamp": "2023-05-01T12:00:00+00:00", "author": "J. Pedantic"}

    assert comment != non_comment


def test_comment_eq_with_partial_values():
    """
    Test __eq__ with Comment objects having partial values.
    """
    comment1 = Comment(value="This is a test comment.")
    comment2 = Comment(value="This is a test comment.")

    assert comment1 == comment2


def test_comment_eq_with_different_time_stamps():
    """
    Test __eq__ with Comment objects having different time stamps.
    """
    comment1 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )
    comment2 = Comment(
        time_stamp="2023-05-02T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )

    assert comment1 != comment2


def test_comment_eq_with_different_authors():
    """
    Test __eq__ with Comment objects having different authors.
    """
    comment1 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="J. Pedantic",
        value="This is a test comment.",
    )
    comment2 = Comment(
        time_stamp="2023-05-01T12:00:00+00:00",
        author="A. Different",
        value="This is a test comment.",
    )

    assert comment1 != comment2
