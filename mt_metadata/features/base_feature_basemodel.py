# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated
import numpy as np
import xarray as xr

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import Field, field_validator, ValidationInfo, PrivateAttr
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.features import SUPPORTED_FEATURE_DICT


# =====================================================
class DomainEnum(StrEnumerationBase):
    time = "time"
    frequency = "frequency"
    fc = "fc"
    ts = "ts"
    fourier = "fourier"


class Feature(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the feature.",
            examples=["simple coherence"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    description: Annotated[
        str,
        Field(
            default="",
            description="A full description of what the feature estimates.",
            examples=[
                "Simple coherence measures the coherence between measured electric and magnetic fields."
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    domain: Annotated[
        DomainEnum,
        Field(
            default="frequency",
            description="Temporal domain the feature is estimated in [ 'frequency' | 'time' ]",
            examples=["frequency"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),  # type: ignore
            description="Any comments about the feature",
            examples=["estimated using hilburt transform."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data: Annotated[
        xr.DataArray | xr.Dataset | np.ndarray | None,
        Field(
            default=None,
            description="The data associated with the feature.",
            examples=["path/to/datafile.nc"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    _supported_features: dict[str, type] = PrivateAttr(SUPPORTED_FEATURE_DICT)

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("data", mode="before")
    @classmethod
    def validate_data(
        cls, value, info: ValidationInfo
    ) -> xr.DataArray | xr.Dataset | np.ndarray | None:
        if value is None:
            return None
        elif not isinstance(value, (xr.DataArray, xr.Dataset, np.ndarray)):
            raise TypeError("Data must be a numpy array, xarray, or None.")
        return value

    @classmethod
    def from_feature_id(cls, meta_dict):
        """
        Factory: instantiate the correct feature class based on 'feature_id'.

        not sure this is needed anymore.
        """
        if "feature_id" not in meta_dict:
            raise KeyError("Feature metadata must include 'feature_id'.")
        feature_id = meta_dict["feature_id"]
        supported = SUPPORTED_FEATURE_DICT
        if feature_id not in supported:
            raise KeyError(
                f"Unknown feature_id '{feature_id}'. Supported: {list(supported.keys())}"
            )
        feature_cls = supported[feature_id]
        obj = feature_cls()
        obj.from_dict(meta_dict)
        return obj
