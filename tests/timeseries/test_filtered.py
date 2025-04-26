import pytest
from mt_metadata.timeseries.filtered_basemodel import Filtered, AppliedFilter
from mt_metadata.common import Comment


def test_applied_filter_default_values():
    """
    Test the default values of the AppliedFilter model.
    """
    applied_filter = AppliedFilter()

    assert applied_filter.name is None
    assert applied_filter.applied is True
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

    assert filtered.filter_list == []
    assert filtered.comments.value is None


def test_filtered_with_applied_filters():
    """
    Test the Filtered model with a list of AppliedFilter objects.
    """
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    filtered = Filtered(filter_list=applied_filters)

    assert len(filtered.filter_list) == 2
    assert filtered.filter_list[0].name == "low pass"
    assert filtered.filter_list[1].name == "high pass"


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
    filtered = Filtered(filter_list=applied_filters, comments="Test comment")

    result = filtered.to_dict(single=True)
    assert result == {
        "filter_list": [
            {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
            {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
        ],
        "comments": filtered.comments.to_dict(),
    }


def test_filtered_from_dict():
    """
    Test the from_dict method of the Filtered model.
    """
    data = {
        "filtered": {
            "filter_list": [
                {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
                {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
            ],
            "comments": {"value": "Test comment"},
        }
    }
    filtered = Filtered()
    filtered.from_dict(data)

    assert len(filtered.filter_list) == 2
    assert filtered.filter_list[0].name == "low pass"
    assert filtered.filter_list[1].name == "high pass"
    assert isinstance(filtered.comments, Comment)
    assert filtered.comments.value == "Test comment"


def test_filtered_from_dict_without_stage():
    """
    Test the from_dict method when the stage is not provided.
    """
    data = {
        "filtered": {
            "filter_list": [
                {"applied_filter": {"name": "low pass", "applied": True}},
                {"applied_filter": {"name": "high pass", "applied": False}},
            ],
            "comments": {"value": "Test comment"},
        }
    }
    filtered = Filtered()
    filtered.from_dict(data)

    assert len(filtered.filter_list) == 2
    assert filtered.filter_list[0].name == "low pass"
    assert filtered.filter_list[1].name == "high pass"
    assert filtered.filter_list[0].stage is None
    assert filtered.filter_list[1].stage is None


def test_filtered_invalid_filter_list():
    """
    Test the Filtered model with an invalid filter_list type.
    """
    with pytest.raises(ValueError):
        Filtered(
            filter_list="invalid"
        )  # filter_list must be a list of AppliedFilter objects


def test_filtered_add_filter():
    """
    Test adding a filter to the Filtered model.
    """
    filtered = Filtered()
    applied_filter = AppliedFilter(name="low pass", applied=True, stage=1)
    filtered.add_filter(applied_filter)

    assert len(filtered.filter_list) == 1
    assert filtered.filter_list[0].name == "low pass"
    assert filtered.filter_list[0].applied is True
    assert filtered.filter_list[0].stage == 1


def test_filtered_add_filter_from_name_applied():
    """
    Test adding a filter to the Filtered model.
    """
    filtered = Filtered()
    filtered.add_filter(name="low pass", applied=True, stage=1)

    assert len(filtered.filter_list) == 1
    assert filtered.filter_list[0].name == "low pass"
    assert filtered.filter_list[0].applied is True
    assert filtered.filter_list[0].stage == 1


def test_filtered_remove_filter():
    """
    Test removing a filter from the Filtered model.
    """
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    filtered = Filtered(filter_list=applied_filters)

    filtered.remove_filter("low pass")
    assert len(filtered.filter_list) == 1
    assert filtered.filter_list[0].name == "high pass"
    assert filtered.filter_list[0].stage == 1


def test_filtered_remove_filter_no_reset():
    """
    Test removing a filter from the Filtered model.
    """
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    filtered = Filtered(filter_list=applied_filters)

    filtered.remove_filter("low pass", reset_stages=False)
    assert len(filtered.filter_list) == 1
    assert filtered.filter_list[0].name == "high pass"
    assert filtered.filter_list[0].stage == 2
