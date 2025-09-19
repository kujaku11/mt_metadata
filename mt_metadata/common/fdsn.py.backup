# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Fdsn(MetadataBase):
    id: Annotated[
        str | None,
        Field(
            default=None,
            description="Given FDSN archive ID name.",
            examples=["MT001"],
            alias=None,
            pattern="^[a-zA-Z0-9._-]*$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    network: Annotated[
        str | None,
        Field(
            default=None,
            description="Given two character FDSN archive network code. Needs to be 2 alpha numeric characters.",
            examples=["EM"],
            alias=None,
            pattern="^[a-zA-Z0-9]{2}$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    channel_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Three character FDSN channel code. http://docs.fdsn.org/projects/source-identifiers/en/v1.0/channel-codes.html",
            examples=["LQN"],
            alias=None,
            pattern="^[a-zA-Z0-9]{3}*$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    new_epoch: Annotated[
        bool | None,
        Field(
            default=None,
            description="Boolean telling if a new epoch needs to be created or not.",
            examples=["False"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    alternate_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Alternate Code",
            examples=[
                "_INT-NON_FDSN",
                ".UNRESTRICTED",
                "_US-ALL",
                "_US-MT",
                "_US-MT-TA",
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    alternate_network_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Alternate Network Code",
            examples=[
                "_INT-NON_FDSN",
                ".UNRESTRICTED",
                "_US-ALL",
                "_US-MT",
                "_US-MT-TA",
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
