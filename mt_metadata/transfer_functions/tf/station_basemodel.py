# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.timeseries import Station as TSStation
from mt_metadata.transfer_functions.tf.transfer_function_basemodel import (
    TransferFunction,
)


# =====================================================


class Station(TSStation):
    transfer_function: Annotated[
        TransferFunction,
        Field(
            default=TransferFunction(),
            description="Transfer function for the station",
            examples=["TransferFunction()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
