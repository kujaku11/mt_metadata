# =====================================================
# Imports
# =====================================================
from pydantic import Field
from typing import Annotated, Optional, List, Dict, Any

from mt_metadata.base import MetadataBase


# =====================================================
class FilterBase(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of filter applied or to be applied. If more than one filter input as a comma separated list.",
            examples='"lowpass_magnetic"',
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments about the filter.",
            examples="ambient air temperature",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    type: Annotated[
        str,
        Field(
            default="",
            description="Type of filter, must be one of the available filters.",
            examples="fap_table",
            type="string",
            alias=None,
            enum=["fap_table", "zpk", "time_delay", "coefficient", "fir", "other"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units_in: Annotated[
        str,
        Field(
            default="",
            description="Name of the input units to the filter. Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            examples="count",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units_out: Annotated[
        str,
        Field(
            default="",
            description="Name of the output units.  Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            examples="millivolt",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    calibration_date: Annotated[
        str | None,
        Field(
            default=None,
            description="Most recent date of filter calibration in ISO format of YYY-MM-DD.",
            examples="2020-01-01",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    gain: Annotated[
        float,
        Field(
            default=None,
            description="scalar gain of the filter across all frequencies, producted with any frequency depenendent terms",
            examples="1.0",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
