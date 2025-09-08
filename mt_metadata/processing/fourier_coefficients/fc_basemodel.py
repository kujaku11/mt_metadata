# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata import NULL_VALUES
from mt_metadata.base import MetadataBase
from mt_metadata.common import ListDict, TimePeriod
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.processing.fourier_coefficients.decimation_basemodel import Decimation


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
            examples=["[1, 2, 3]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="ID given to the FC group",
            examples=["aurora_01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_estimated: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of channels estimated",
            examples=[["ex", "hy"]],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    starting_sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="Starting sample rate of the time series used to estimate FCs.",
            examples=[60],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    method: Annotated[
        MethodEnum,
        Field(
            default="fft",
            description="Fourier transform method",
            examples=["fft"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,  # type: ignore
            description="Time period of the FCs",
            examples=[TimePeriod(start="2020-01-01", end="2020-01-02")],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    levels: Annotated[
        ListDict,
        Field(
            default_factory=ListDict,  # type: ignore
            description="ListDict of decimation levels and their parameters",
            examples=[
                ListDict(
                    [
                        {
                            "id": "1",
                            "channels_estimated": '["ex", "ey", "hx", "hy"]',
                            "sample_rate_decimation_level": 30,
                            "sample_rate_window_step": 4,
                            "units": "millivolts",
                            "time_period": TimePeriod(
                                start="2020-01-01", end="2020-01-02"
                            ),
                        }
                    ]
                )
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
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
                dl = Decimation()
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

        :param decimation_level_obj: decimation_level object to add
        :type decimation_level_obj: :class:`mt_metadata.transfer_functions.processing.fourier_coefficients.decimation_level`

        """
        if not isinstance(fc_decimation, (Decimation)):
            msg = f"Input must be metadata.decimation_level not {type(fc_decimation)}"
            logger.error(msg)
            raise ValueError(msg)

        if self.has_decimation_level(fc_decimation.decimation.level):
            self.levels[fc_decimation.decimation.level].update(fc_decimation)
            logger.debug(
                f"ch {fc_decimation.decimation.level} already exists, updating metadata"
            )

        else:
            self.levels.append(fc_decimation)

        self.update_time_period()

    def remove_decimation_level(self, decimation_level_id):
        """
        remove a ch from the survey

        :param level: decimation_level level to look for
        :type level: string

        """

        if self.has_decimation_level(decimation_level_id):
            self.levels.remove(decimation_level_id)
        else:
            logger.warning(f"Could not find {decimation_level_id} to remove.")

        self.update_time_period()

    @property
    def n_decimation_levels(self):
        return self.__len__()

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
