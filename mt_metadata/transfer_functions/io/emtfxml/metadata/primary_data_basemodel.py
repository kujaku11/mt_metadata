# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class PrimaryData(MetadataBase):
    filename: Annotated[
        str,
        Field(
            default="",
            description="file name of the figure file that displays the data",
            examples=["example.png"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    def read_dict(self, input_dict: dict) -> None:
        """
        Read the primary_data element from the input dictionary.

        Parameters
        ----------
        input_dict : dict
            The input dictionary containing the primary_data element.
        """
        helpers._read_element(self, input_dict, "primary_data")
