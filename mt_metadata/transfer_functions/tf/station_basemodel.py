# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.timeseries import Station as TSStation
from mt_metadata.transfer_functions.tf import TransferFunction
from mt_metadata.common import ChannelLayoutEnum, Comment, DataTypeEnum, StationLocation


# =====================================================


class Station(TSStation):
    transfer_function: Annotated[
        TransferFunction,
        Field(
            default_factory=TransferFunction,
            description="Transfer function properties",
            examples="TransferFunction()",
            alias=None,
            json_schema_extra={"units": None, "required": True},
        ),
    ]
