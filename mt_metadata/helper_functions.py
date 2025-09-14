"""
This module has some general helper functions that it isn't yet clear where they should live.

These may not be needed at all after the pydantic upgrade is fully integrated.
"""

from typing import Dict, List, Union

from mt_metadata.base import MetadataBase


"""
    Here are some rather abstract functions for generalizing setters of lists,
    whose elements are particular mt_metadata classes.
    Example usage is decimation_level.bands

"""


def validate_setter_input(
    value: Union[Dict, MetadataBase], expected_class: MetadataBase
) -> List:
    """
    Takes a setter's input and makes it a list if it not.
    Then asserts that every list element is of permissible type (dict or expected class)

    Parameters
    ----------
    value: Union[Dict, Base]
        The input to the setter.

    expected_class: Base
        Some mt_metadata class that we want the setter work with

    Returns
    -------
    value: list
        List of elements for the setter all of type expected_class or dict.
    """
    # Handle singleton cases
    if isinstance(value, (expected_class, dict)):
        value = [value]

    if not isinstance(value, list):
        raise TypeError(f"Not sure what to do with {type(value)}")

    return value


def cast_to_class_if_dict(
    obj: Union[Dict, MetadataBase], cls: MetadataBase
) -> MetadataBase:
    """

    Parameters
    ----------
    obj: Union[Dict, MetadataBase]
        Either an mt_metadata object or its dict representaiton
    cls: MetadataBase
        Some mt_metadata object that we want to get back

    Returns
    -------
    either the input or the input dict cast to an mt_metadata object.
    """
    if not isinstance(obj, (cls, dict)):
        raise TypeError(
            f"List entry must be a {cls().__class__} object not {type(obj)}"
        )
    if isinstance(obj, dict):
        mt_metadata_obj = cls()
        mt_metadata_obj.from_dict(obj)
    else:
        mt_metadata_obj = obj

    return mt_metadata_obj
