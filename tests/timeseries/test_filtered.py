import pytest
from mt_metadata.timeseries.filtered_basemodel import Filtered, AppliedFilter
from mt_metadata.common.comment_basemodel import Comment


def test_applied_filter_default_values():
    """
    Test the default values of the AppliedFilter model.
    """
    applied_filter = AppliedFilter()

    assert applied_filter.name is None
    assert applied_filter.applied is False
    assert applied_filter.stage is None


def test_applied_filter_custom_values():
    """
    Test the AppliedFilter model with custom values.
    """
    applied_filter = AppliedFilter(name="low pass", applied=True, stage=1)

    assert applied_filter.name == "low pass"
    assert applied_filter.applied is True
    assert applied_filter.stage == 1


def test_applied_filter_invalid_name():
    """
    Test the AppliedFilter model with an invalid name type.
    """
    with pytest.raises(ValueError):
        AppliedFilter(name=True)  # Name must be a string


def test_filtered_default_values():
    """
    Test the default values of the Filtered model.
    """
    filtered = Filtered()

    assert filtered.applied_list == []
    assert filtered.comments is None
    assert filtered.applied == []
    assert filtered.name == []
    assert filtered.stage == []


def test_filtered_with_applied_filters():
    """
    Test the Filtered model with a list of AppliedFilter objects.
    """
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    filtered = Filtered(applied_list=applied_filters)

    assert len(filtered.applied_list) == 2
    assert filtered.applied == [True, False]
    assert filtered.name == ["low pass", "high pass"]
    assert filtered.stage == [1, 2]


def test_filtered_with_comments():
    """
    Test the Filtered model with comments.
    """
    filtered = Filtered(comments="low pass filter applied")

    assert isinstance(filtered.comments, Comment)
    assert filtered.comments.value == "low pass filter applied"


def test_filtered_to_dict():
    """
    Test the to_dict method of the Filtered model.
    """
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    filtered = Filtered(applied_list=applied_filters, comments="Test comment")

    result = filtered.to_dict(include_stage=True)
    assert result == {
        "applied": [True, False],
        "name": ["low pass", "high pass"],
        "stage": [1, 2],
        "comments": filtered.comments,
    }


def test_filtered_from_dict():
    """
    Test the from_dict method of the Filtered model.
    """
    data = {
        "applied": [True, False],
        "name": ["low pass", "high pass"],
        "stage": [1, 2],
    }
    filtered = Filtered()
    filtered.from_dict(data)

    assert len(filtered.applied_list) == 2
    assert filtered.applied == [True, False]
    assert filtered.name == ["low pass", "high pass"]
    assert filtered.stage == [1, 2]


def test_filtered_from_dict_without_stage():
    """
    Test the from_dict method when the stage is not provided.
    """
    data = {
        "applied": [True, False],
        "name": ["low pass", "high pass"],
    }
    filtered = Filtered()
    filtered.from_dict(data)

    assert len(filtered.applied_list) == 2
    assert filtered.applied == [True, False]
    assert filtered.name == ["low pass", "high pass"]
    assert filtered.stage == [0, 1]  # Default to index if stage is not provided


def test_filtered_invalid_applied_list():
    """
    Test the Filtered model with an invalid applied_list type.
    """
    with pytest.raises(ValueError):
        Filtered(
            applied_list="invalid"
        )  # applied_list must be a list of AppliedFilter objects
