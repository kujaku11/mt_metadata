# =====================================================
# Imports
# =====================================================
from typing import Annotated
from pydantic import Field, PrivateAttr
from mt_metadata.timeseries import Channel


# =====================================================


class Auxiliary(Channel):
    """
    Auxiliary channel class for storing auxiliary channel information.
    """

    _channel_type: str = PrivateAttr("auxiliary")

    type: Annotated[
        str,
        Field(
            default="auxiliary",
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            examples="auxiliary",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
