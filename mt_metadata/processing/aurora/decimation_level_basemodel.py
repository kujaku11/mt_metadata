# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.processing.aurora.band_basemodel import Band
from mt_metadata.processing.time_series_decimation_basemodel import (
    TimeSeriesDecimation as Decimation,
)


# =====================================================
class SaveFcsTypeEnum(str, Enum):
    h5 = "h5"
    csv = "csv"


class DecimationLevel(MetadataBase):
    bands: Annotated[
        list[Band],
        Field(
            default_factory=list,
            description="List of bands",
            examples=["[]"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channel_weight_specs: Annotated[
        list,
        Field(
            default_factory=list,
            description="List of weighting schemes to use for TF processing for each output channel",
            examples=["[]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input_channels: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of input channels (sources)",
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of output channels (responses)",
            examples=["ex, ey, hz"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reference_channels: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of reference channels (remote sources)",
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    save_fcs: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the Fourier coefficients are saved [True] or not [False].",
            examples=[True],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    save_fcs_type: Annotated[
        SaveFcsTypeEnum | None,
        Field(
            default=None,
            description="Format to use for fc storage",
            examples=["h5"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    decimation: Annotated[
        Decimation,
        Field(
            default_factory=Decimation,
            description="Decimation settings",
            examples=["Decimation()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
