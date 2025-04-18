# =====================================================
# Imports
# =====================================================
from typing import Annotated
from typing_extensions import Self
from pydantic import (
    Field,
    field_validator,
    ValidationInfo,
    ValidationError,
    model_validator,
)
from loguru import logger
import numpy as np
import pandas as pd

from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime


# =====================================================
class Comment(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="person who authored the comment",
            examples="J. Pedantic",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    time_stamp: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime,
        Field(
            default_factory=lambda: MTime(time_stamp="1980-01-01T00:00:00+00:00"),
            description="Date and time of in UTC of when comment was made.",
            examples="2020-02-01T09:23:45.453670+00:00",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    value: Annotated[
        str | None,
        Field(
            default=None,
            description="comment string",
            examples="failure at midnight.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    @field_validator("time_stamp", mode="before")
    @classmethod
    def validate_time(cls, value, info: ValidationInfo) -> MTime:
        """
        Validate that the value is a valid time.
        """
        return MTime(time_stamp=value)

    @model_validator(mode="after")
    def set_variables(self) -> Self:
        """
        Validate that the value is a valid string.
        """
        if self.value is not None:
            if "|" in self.value:
                parts = [ss.strip() for ss in self.value.split("|")]
                self.value = parts[-1]
                if len(parts) == 3:
                    self.time_stamp = parts[0]
                    self.author = parts[1]
                elif len(parts) == 2:
                    try:
                        self.time_stamp = parts[0]
                    except ValidationError:
                        self.author = parts[0]
        return self

    def to_dict(self, nested=False, single=False, required=True) -> str:
        """
        Returns the comment as "{time_stamp} | {author} | {comment}"

        TODO: in the future this should return an actual dictionary to
         comply with all other objects.

        Returns
        -------
        str
            formatted comment
        """
        if self.value is None:
            return None

        if self.time_stamp == "1980-01-01T00:00:00+00:00":
            if self.author in [None, ""]:
                return self.value
            return f" {self.author} | {self.value}"
        if self.author in [None, ""]:
            return f"{self.time_stamp} | {self.value}"
        return f"{self.time_stamp} | {self.author} | {self.value}"

    def from_dict(
        self,
        value: str | dict,
        skip_none=False,
    ) -> None:
        """
        Parse input comment assuming "{time_stamp} | {author} | {comment}"

        Parameters
        ----------
        value : str
            _description_
        skip_none : bool, optional
            _description_, by default False
        """
        if isinstance(value, str):
            self.value = value
        elif isinstance(value, dict):
            if len(value.keys()) > 1:
                for key in ["time_stamp", "author", "value"]:
                    try:
                        setattr(self, key, value[key])
                    except KeyError:
                        logger.warning(f"Could not find {key} in input dictionary.")
            else:
                key = list(value.keys())[0]
                self.value = value[key]

        else:
            raise TypeError(f"Cannot parse type {type(value)}")
