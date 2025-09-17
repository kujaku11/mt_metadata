# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.timeseries import Station as TSStation
from mt_metadata.transfer_functions.tf.transfer_function import TransferFunction


# =====================================================


class Station(TSStation):
    transfer_function: Annotated[
        TransferFunction,
        Field(
            default=TransferFunction(),  # type: ignore
            description="Transfer function for the station",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["TransferFunction()"],
            },
        ),
    ]
