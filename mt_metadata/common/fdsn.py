# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Fdsn(MetadataBase):
    id: Annotated[
        str | None,
        Field(
            default=None,
            description="Given FDSN archive ID name.",
            examples="MT001",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    network: Annotated[
        str | None,
        Field(
            default=None,
            description="Given two character FDSN archive network code. Needs to be 2 alpha numeric characters.",
            examples="EM",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]{2}$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    channel_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Three character FDSN channel code. http://docs.fdsn.org/projects/source-identifiers/en/v1.0/channel-codes.html",
            examples="LQN",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]{3}*$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    new_epoch: Annotated[
        bool | None,
        Field(
            default=None,
            description="Boolean telling if a new epoch needs to be created or not.",
            examples="False",
            type="boolean",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    alternate_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Alternate Code",
            examples="_INT-NON_FDSN,.UNRESTRICTED,_US-ALL,_US-MT,_US-MT-TA",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    alternate_network_code: Annotated[
        str | None,
        Field(
            default=None,
            description="Alternate Network Code",
            examples="_INT-NON_FDSN,.UNRESTRICTED,_US-ALL,_US-MT,_US-MT-TA",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
