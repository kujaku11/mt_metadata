# =====================================================
# Imports
# =====================================================

from collections import OrderedDict
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import AliasChoices, Field, field_validator, PrivateAttr, ValidationInfo

from mt_metadata import NULL_VALUES
from mt_metadata.base import helpers, MetadataBase
from mt_metadata.common import (
    BasicLocation,
    Comment,
    DataQuality,
    Fdsn,
    Instrument,
    TimePeriod,
)
from mt_metadata.common.units import get_unit_object, Unit
from mt_metadata.timeseries import AppliedFilter
from mt_metadata.timeseries.filters import ChannelResponse
from mt_metadata.utils.exceptions import MTSchemaError
from mt_metadata.utils.validators import validate_name


# =====================================================


# this is a channel base for channels that have multiple sensors and locations like an
# electric dipole.
class ChannelBase(MetadataBase):
    _channel_type: str = PrivateAttr("base")
    channel_number: Annotated[
        int,
        Field(
            default=0,
            description="Channel number on the data logger.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1"],
            },
        ),
    ]

    channel_id: Annotated[
        str | None,
        Field(
            default=None,
            description="channel id given by the user or data logger",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1001.11"],
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments about the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["ambient air temperature was chilly, ice on cables"],
            },
        ),
    ]

    component: Annotated[
        str,
        Field(
            default="",
            description="Name of the component measured, can be uppercase and/or lowercase.  For now electric channels should start with an 'e' and magnetic channels start with an 'h', followed by the component. If there are multiples of the same channel the name could include an integer.  {type}{component}{number} --> Ex01.",
            alias=None,
            pattern=r"\w+",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ex"],
            },
        ),
    ]

    measurement_azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="Horizontal azimuth of the channel in measurement coordinate system spcified in station.orientation.reference_frame.  Default reference frame is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            validation_alias=AliasChoices("measurement_azimuth", "azimuth"),
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": [0.0],
            },
        ),
    ]

    measurement_tilt: Annotated[
        float,
        Field(
            default=0.0,
            description="Vertical tilt of the channel in measurement coordinate system specified in station.orientation.reference_frame.  Default reference frame is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            validation_alias=AliasChoices("measurement_tilt", "dip"),
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": [0],
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate",
            validation_alias=AliasChoices("sample_rate", "sampling_rate"),
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [8.0],
            },
        ),
    ]

    translated_azimuth: Annotated[
        float | None,
        Field(
            default=None,
            description="Horizontal azimuth of the channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data in geomagnetic coordinates and then translated them to geographic coordinates you would set measurement_azimuth=0, translated_azimuth=-12.5 for a declination angle of N12.5E.",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
                "examples": [0.0],
            },
        ),
    ]

    translated_tilt: Annotated[
        float | None,
        Field(
            default=None,
            description="Tilt of channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data using a tripod you would set measurement_tilt=45, translated_tilt=0 for a vertical component.",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
                "examples": [0.0],
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="base",
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["temperature"],
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="",
            description="Units of the data, should be in SI units and represented as the full name of the unit all lowercase.  If a complex unit use 'per' and '-'.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["celsius"],
            },
        ),
    ]

    data_quality: Annotated[
        DataQuality,
        Field(
            default_factory=DataQuality,
            description="Data quality for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["DataQuality()"],
            },
        ),
    ]

    filters: Annotated[
        list[AppliedFilter],
        Field(
            default_factory=list,
            description="Filter data for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [
                    "AppliedFilter(name='filter_name', applied=True, stage=1)"
                ],
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,
            description="Time period for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["TimePeriod(start='2020-01-01', end='2020-12-31')"],
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,
            description="FDSN information for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Fdsn()"],
            },
        ),
    ]

    @field_validator("component", mode="before")
    @classmethod
    def validate_component(cls, value: str) -> str:
        """make sure the value is all lower case"""
        if not isinstance(value, str):
            raise TypeError(f"Component must be a string not {type(value)}")

        return value.lower()

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, (str, list)):
            return Comment(value=value)
        return value

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str, info: ValidationInfo) -> str:
        """
        validate units base on input string will return the long name

        Parameters
        ----------
        value : units string
            unit string separated by either '/' for division or ' ' for
            multiplication.  Or 'per' and ' ', respectively
        info : ValidationInfo
            _description_

        Returns
        -------
        str
            return the long descriptive name of the unit. For example 'kilometers'.
        """
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """
        Validate that the type channel
        """
        # Get the expected filter type based on the actual class
        # Make sure derived classes define their own _filter_type as class variable
        expected_type = getattr(cls, "_channel_type", "base").default

        if value != expected_type:
            logger.warning(
                f"Channel type is set to {value}, but should be "
                f"{expected_type} for {cls.__name__}."
            )
        return expected_type

    @field_validator("filters", mode="after")
    @classmethod
    def validate_filters(cls, v, info):
        """sort the filters by stage number and check for duplicates"""
        # Get the instance being validated
        instance = info.data if hasattr(info, "data") else None

        # Sort filters by stage number, treating None as 0
        v.sort(key=lambda f: f.stage if f.stage is not None else 0)

        # Check for duplicates
        seen = set()
        for f in v:
            if f.name in seen:
                raise ValueError(f"Duplicate filter found: {f.name}")
            seen.add(f.name)

        return v

    def add_filter(
        self,
        applied_filter: AppliedFilter | None = None,
        name: str | None = None,
        applied: bool = True,
        stage: int | None = None,
        comments: Comment | str | None = None,
    ) -> None:
        """
        Add a filter to the filter list.

        Parameters
        ----------
        name : str
            Name of the filter.
        applied : bool, optional
            Whether the filter has been applied, by default True.
        stage : int | None, optional
            Stage of the filter in the processing chain, by default None.
        """
        if applied_filter is not None:
            if not isinstance(applied_filter, AppliedFilter):
                raise TypeError("applied_filter must be an instance of AppliedFilter")
            if applied_filter.stage is None:
                applied_filter.stage = len(self.filters) + 1
            self.filters.append(applied_filter)
        else:
            if name is None:
                raise ValueError("name must be provided if applied_filter is None")
            if not isinstance(name, str):
                raise TypeError("name must be a string")
            if stage is None:
                stage = len(self.filters) + 1

            # Build kwargs for AppliedFilter, excluding None comments to use default
            filter_kwargs = {"name": name, "applied": applied, "stage": stage}
            if comments is not None:
                filter_kwargs["comments"] = comments

            self.filters.append(AppliedFilter(**filter_kwargs))

            # Sort filters and validate for duplicates
            self._sort_filters()
            self._validate_no_duplicates()

    def remove_filter(self, name: str, reset_stages: bool = True) -> None:
        """
        Remove a filter from the filter list.

        Parameters
        ----------
        name : str
            Name of the filter to remove.
        reset_stages : bool, optional
            Whether to reset the stages of the remaining filters, by default True.
        """

        new_list = []
        for f in self.filters:
            if f.name == name:
                continue
            if reset_stages:
                f.stage = len(new_list) + 1
            new_list.append(f)
        self.filters = new_list

    def _sort_filters(self) -> None:
        """
        Sort the list of filters applied to the channel by stage number.

        Returns
        -------
        None
        """
        # Sort filters by stage number, treating None as 0
        self.filters.sort(key=lambda f: f.stage if f.stage is not None else 0)

    def _validate_no_duplicates(self) -> None:
        """
        Check for duplicate filter names and raise an error if found.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If duplicate filter names are found.
        """
        seen = set()
        for f in self.filters:
            if f.name in seen:
                raise ValueError(f"Duplicate filter found: {f.name}")
            seen.add(f.name)

    def channel_response(self, filters_dict):
        """
        full channel response from a dictionary of filter objects
        """

        mt_filter_list = []
        for applied_filter in self.filters:
            try:
                mt_filter = filters_dict[applied_filter.name]
                mt_filter_list.append(mt_filter)
            except KeyError:
                msg = f"Could not find {applied_filter.name} in filters dictionary, skipping"
                logger.error(msg)
                continue
        # compute instrument sensitivity and units in/out
        return ChannelResponse(filters_list=mt_filter_list)

    @property
    def unit_object(self) -> Unit:
        """
        Some channels have a unit object that is used to convert between units.
        This is a property that returns the unit object for the channel.
        The unit object is created using the units attribute of the channel.
        The unit object is used to convert between units and to get the unit

        Returns
        -------
        Unit
            BaseModel object with unit attributes
        """
        return get_unit_object(self.units)

    def _validate_filtered_applied(
        self, applied: list | np.typing.NDArray | str | None
    ) -> list:
        applied_values = _applied_values_map(treat_null_values_as=False)
        # the returned type from a hdf5 dataset is a numpy array.
        if isinstance(applied, np.ndarray):
            return applied.tolist()

        # sets an empty list to one default value
        if isinstance(applied, list) and len(applied) == 0:
            return []

        # Handle string case
        if isinstance(applied, str):
            # Handle simple strings
            if applied in applied_values.keys():
                return [
                    applied_values[applied],
                ]

            # Handle string-lists (e.g. from json)
            if applied.find("[") >= 0:
                applied = applied.replace("[", "").replace("]", "")
            if applied.count(",") > 0:
                return [ss.strip().lower() for ss in applied.split(",")]
            else:
                return [ss.lower() for ss in applied.split()]
        elif isinstance(applied, list):
            return applied
        elif isinstance(applied, tuple):
            return list(applied)
        else:
            msg = f"Input applied cannot be of type {type(applied)}"
            logger.error(msg)
            raise MTSchemaError(msg)

    def _validate_filtered_name(
        self, names: list | np.typing.NDArray | str | None
    ) -> list:
        if names is None:
            return []

        if isinstance(names, str):
            return [ss.strip().lower() for ss in names.split(",")]
        elif isinstance(names, list):
            return [ss.strip().lower() for ss in names]
        elif isinstance(names, np.ndarray):
            names = names.astype(np.str_)
            return [ss.strip().lower() for ss in names]
        else:
            msg = "names must be a string or list of strings not {0}, type {1}"
            logger.error(msg.format(names, type(names)))
            raise MTSchemaError(msg.format(names, type(names)))

    def _find_filter_keys(self, meta_dict: dict) -> str | None:
        """
        Search for filter-related keys in the meta_dict.

        Parameters
        ----------
        meta_dict : dict
            Dictionary to search for filter keys.

        Returns
        -------
        str | None
            Returns 'filter' if any keys have 'filter' as base (before '.'),
            'filtered' if any keys have 'filtered' as base (before '.'),
            or None if no filter-related keys are found.
        """
        keys = list(meta_dict.keys())

        for key in keys:
            # Split by '.' and check the base key
            base_key = key.split(".")[0]

            # Check for 'filter' base (legacy format)
            if base_key == "filter":
                return "filter"

            # Check for 'filtered' base (old format)
            if base_key == "filtered":
                return "filtered"

        return None

    def from_dict(self, meta_dict: dict, skip_none: bool = False) -> None:
        """
        fill attributes from a dictionary but need to make it
        backwards compatible with accepting filtered.applied and
        filtered.name as lists.

        Parameters
        ----------
        meta_dict : dict
            dictionary of attributes to set.
        skip_none : bool, optional
            If True, skip attributes with None values, by default False.

        Raises
        -------
        MTSchemaError
            If the input dictionary is not valid.

        """
        if not isinstance(meta_dict, (dict, OrderedDict)):
            msg = f"Input must be a dictionary not {type(meta_dict)}"
            logger.error(msg)
            raise MTSchemaError(msg)
        keys = list(meta_dict.keys())
        if len(keys) == 1:
            if isinstance(meta_dict[keys[0]], (dict, OrderedDict)):
                class_name = keys[0]
                if class_name.lower() != validate_name(self.__class__.__name__):
                    msg = (
                        "name of input dictionary is not the same as class type "
                        f"input = {class_name}, class type = {self.__class__.__name__}"
                    )
                    logger.debug(msg, class_name, self.__class__.__name__)
                meta_dict = helpers.flatten_dict(meta_dict[class_name])
            else:
                meta_dict = helpers.flatten_dict(meta_dict)

        else:
            logger.debug(
                f"Assuming input dictionary is of type {self.__class__.__name__}",
            )
            meta_dict = helpers.flatten_dict(meta_dict)

        # Use helper method to detect filter format
        filter_format = self._find_filter_keys(meta_dict)

        # Handle different filter formats based on detection
        if filter_format == "filtered":
            # Handle old format filters using f-string formatting
            old_format_applied = meta_dict.pop(f"{filter_format}.applied", None)
            old_format_names = meta_dict.pop(f"{filter_format}.name", None)

            if old_format_applied is not None and old_format_names is not None:
                filter_applied = self._validate_filtered_applied(old_format_applied)
                filter_name = self._validate_filtered_name(old_format_names)
                if filter_applied and filter_name:
                    logger.warning(
                        f"{filter_format}.applied and {filter_format}.name are deprecated, use filters as a list of AppliedFilter objects instead"
                    )
                    if len(filter_applied) != len(filter_name):
                        msg = (
                            f"{filter_format}.applied and {filter_format}.name must be the same length, "
                            f"got {len(filter_applied)} and {len(filter_name)}"
                        )
                        logger.error(msg)
                        raise MTSchemaError(msg)
                    for name, applied in zip(filter_name, filter_applied):
                        self.add_filter(name=name, applied=applied)

        elif filter_format == "filter":
            # Handle legacy single 'filter' attribute - just remove and warn
            legacy_filter = meta_dict.pop(filter_format, None)
            if legacy_filter is not None:
                logger.warning(
                    f"The '{filter_format}' attribute is deprecated and will be ignored. Use 'filters' as a list of AppliedFilter objects instead."
                )

        # Handle new format filters separately to combine with old format
        new_format_filters = meta_dict.pop("filters", None)

        for name, value in meta_dict.items():
            if skip_none:
                if value in NULL_VALUES:
                    continue
            self.update_attribute(name, value)

        # Process new format filters after other attributes, adding to existing filters
        if new_format_filters is not None:
            for filter_dict in new_format_filters:
                if isinstance(filter_dict, dict):
                    # Create AppliedFilter from dict using from_dict method to handle nested attributes
                    applied_filter = AppliedFilter()
                    applied_filter.from_dict(filter_dict)
                    self.add_filter(applied_filter=applied_filter)
                elif isinstance(filter_dict, AppliedFilter):
                    self.add_filter(applied_filter=filter_dict)
                else:
                    logger.warning(f"Unknown filter format: {type(filter_dict)}")


# this would be a normal channel that has a single sensor and location.
class Channel(ChannelBase):
    sensor: Annotated[
        Instrument,
        Field(
            default_factory=Instrument,
            description="Sensor for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Instrument()",
            },
        ),
    ]

    location: Annotated[
        BasicLocation,
        Field(
            default_factory=BasicLocation,
            description="Location information for the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [
                    "BasicLocation(latitude=0.0, longitude=0.0, elevation=0.0)"
                ],
            },
        ),
    ]


def _applied_values_map(treat_null_values_as: bool = True) -> dict:
    """
    helper function to simplify logic in applied setter.

    Notes:
    The logic in the setter was getting quite complicated handling many types.
    A reasonable solution seemed to be to map each of the allowed values to a bool
    via dict and then use this dict when setting applied values.

    :return: dict
    Mapping of all tolerated single-values for setting applied booleans
    """
    null_values = [None, "none", "None", "NONE", "null"]
    null_values_map = {x: treat_null_values_as for x in null_values}
    true_values = [True, 1, "1", "True", "true"]
    true_values_map = {x: True for x in true_values}
    false_values = [False, 0, "0", "False", "false"]
    false_values_map = {x: False for x in false_values}
    values_map = {**null_values_map, **true_values_map, **false_values_map}
    return values_map
