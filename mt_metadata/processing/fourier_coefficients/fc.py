# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, model_validator, ValidationInfo

from mt_metadata import NULL_VALUES
from mt_metadata.base import MetadataBase
from mt_metadata.common import ListDict, TimePeriod
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.processing.fourier_coefficients.decimation import Decimation


# =====================================================
class MethodEnum(StrEnumerationBase):
    fft = "fft"
    wavelet = "wavelet"
    other = "other"


class FC(MetadataBase):
    decimation_levels: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of decimation levels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["[1, 2, 3]"],
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="ID given to the FC group",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["aurora_01"],
            },
        ),
    ]

    channels_estimated: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of channels estimated",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [["ex", "hy"]],
            },
        ),
    ]

    starting_sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="Starting sample rate of the time series used to estimate FCs.",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [60],
            },
        ),
    ]

    method: Annotated[
        MethodEnum,
        Field(
            default=MethodEnum.fft,
            description="Fourier transform method",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["fft"],
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,  # type: ignore
            description="Time period of the FCs",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [TimePeriod(start="2020-01-01", end="2020-01-02")],
            },
        ),
    ]

    levels: Annotated[
        ListDict,
        Field(
            default_factory=ListDict,  # type: ignore
            description="ListDict of decimation levels and their parameters",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ListDict containing Decimation objects"],
            },
        ),
    ]

    @field_validator("channels_estimated", "decimation_levels", mode="before")
    @classmethod
    def validate_channels_estimated(
        cls, value: list[str] | np.ndarray | str, info: ValidationInfo
    ) -> list[str]:
        if isinstance(value, np.ndarray):
            value = value.tolist()

        if value in NULL_VALUES:
            return []
        elif isinstance(value, (list, tuple)):
            return value

        elif isinstance(value, (str)):
            value = value.split(",")
            return value

        else:
            raise TypeError(
                "'channels_recorded' must be set with a list not " f"{type(value)}."
            )

    @field_validator("levels", mode="before")
    @classmethod
    def validate_levels(cls, value, info: ValidationInfo):
        # Handle None values first
        if value is None:
            return ListDict()

        # Handle string representations that might come from HDF5 storage
        if isinstance(value, str):
            # If it's a string representation, try to parse it or return empty ListDict
            if value in ["", "none", "None", "ListDict()", "{}"]:
                return ListDict()
            # For other string values, try to maintain backward compatibility
            logger.warning(f"Converting string representation of levels: {value}")
            return ListDict()

        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input dl_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            logger.error(msg)
            raise TypeError(msg)

        fails = []
        levels = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, decimation_level in enumerate(value_list):
            try:
                if isinstance(decimation_level, Decimation):
                    dl = decimation_level
                else:
                    dl = Decimation()  # type: ignore
                    if hasattr(decimation_level, "to_dict"):
                        decimation_level = decimation_level.to_dict()
                    dl.from_dict(decimation_level)
                levels.append(dl)
            except Exception as error:
                msg = "Could not create decimation_level from dictionary: %s"
                fails.append(msg % error)
                logger.error(msg, error)

        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        return levels

    @model_validator(mode="after")
    def synchronize_levels(self) -> "FC":
        """
        Ensure that decimation_levels and levels are synchronized.
        - Creates Decimation objects for any levels in decimation_levels that don't exist in levels
        - Adds level names to decimation_levels for any existing levels not in the list
        """
        # First, ensure all levels in decimation_levels have corresponding Decimation objects
        for level_name in self.decimation_levels:
            level_name_str = str(level_name)
            if level_name_str not in self.levels.keys():
                # Create a new Decimation object with the level name as id
                new_decimation = Decimation(id=level_name_str)  # type: ignore
                self.levels.append(new_decimation)

        # Second, ensure all existing levels in the ListDict are in decimation_levels
        for level_name in self.levels.keys():
            if level_name not in self.decimation_levels:
                self.decimation_levels.append(level_name)

        return self

    def has_decimation_level(self, level):
        """
        Check to see if the decimation_level already exists

        :param level: decimation_level level to look for
        :type level: string
        :return: True if found, False if not
        :rtype: boolean

        """

        if level in self.decimation_levels:
            return True
        return False

    def decimation_level_index(self, level):
        """
        get index of the decimation_level in the decimation_level list
        """
        if self.has_decimation_level(level):
            return self.levels.keys().index(str(level))
        return None

    def get_decimation_level(self, level):
        """
        Get a decimation_level

        :param level: decimation_level level to look for
        :type level: string
        :return: decimation_level object based on decimation_level type
        :rtype: :class:`mt_metadata.timeseries.decimation_level`

        """

        if self.has_decimation_level(level):
            return self.levels[str(level)]

    def add_decimation_level(self, fc_decimation):
        """
        Add a decimation_level to the list, check if one exists if it does overwrite it

        :param fc_decimation: decimation level object to add
        :type fc_decimation: :class:`mt_metadata.processing.fourier_coefficients.decimation_basemodel.Decimation`

        """
        if not isinstance(fc_decimation, (Decimation)):
            msg = f"Input must be metadata.decimation_level not {type(fc_decimation)}"
            logger.error(msg)
            raise ValueError(msg)

        level_id = fc_decimation.id
        if self.has_decimation_level(level_id):
            self.levels[level_id].update(fc_decimation)
            logger.debug(f"level {level_id} already exists, updating metadata")
        else:
            self.levels.append(fc_decimation)
            # Also add to decimation_levels list if not present
            if level_id not in self.decimation_levels:
                self.decimation_levels.append(level_id)

        self.update_time_period()

    def remove_decimation_level(self, decimation_level_id):
        """
        remove a ch from the survey

        :param level: decimation_level level to look for
        :type level: string

        """

        if self.has_decimation_level(decimation_level_id):
            self.levels.remove(decimation_level_id)
            # Also remove from decimation_levels list
            if decimation_level_id in self.decimation_levels:
                self.decimation_levels.remove(decimation_level_id)
        else:
            logger.warning(f"Could not find {decimation_level_id} to remove.")

        self.update_time_period()

    @property
    def n_decimation_levels(self):
        return len(self.levels)

    def update_time_period(self):
        """
        update time period from ch information
        """
        start = []
        end = []
        for dl in self.levels:
            if dl.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(dl.time_period.start)
            if dl.time_period.start != "1980-01-01T00:00:00+00:00":
                end.append(dl.time_period.end)
        if start:
            if self.time_period.start == "1980-01-01T00:00:00+00:00":
                self.time_period.start = min(start)
            else:
                if self.time_period.start > min(start):
                    self.time_period.start = min(start)
        if end:
            if self.time_period.end == "1980-01-01T00:00:00+00:00":
                self.time_period.end = max(end)
            else:
                if self.time_period.end < max(end):
                    self.time_period.end = max(end)
