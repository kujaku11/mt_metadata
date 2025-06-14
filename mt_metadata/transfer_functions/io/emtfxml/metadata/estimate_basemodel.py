# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field, HttpUrl

from mt_metadata.base import MetadataBase


# =====================================================
class TypeEnum(str, Enum):
    real = "real"
    complex = "complex"


class IntentionEnum(str, Enum):
    error_estimate = "error estimate"
    signal_coherence = "signal coherence"
    signal_power_estimate = "signal power estimate"
    primary_data_type = "primary data type"


class Estimate(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the statistical estimate",
            examples=["var"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    type: Annotated[
        TypeEnum,
        Field(
            default="",
            description="Type of number contained in the estimate",
            examples=["real"],
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
            description="Description of the statistical estimate",
            examples=["this is an estimate"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    external_url: Annotated[
        HttpUrl,
        Field(
            default="",
            description="Full path to external link that has additional information",
            examples=["http://www.iris.edu/dms/products/emtf/variance.html"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    intention: Annotated[
        IntentionEnum,
        Field(
            default="",
            description="The intension of the statistical estimate",
            examples=["error estimate"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    tag: Annotated[
        str,
        Field(
            default="",
            description="A useful tag for the estimate",
            examples=["tipper"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
