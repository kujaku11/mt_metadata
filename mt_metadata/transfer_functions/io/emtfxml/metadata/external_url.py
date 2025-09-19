# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, HttpUrl

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class ExternalUrl(MetadataBase):
    description: Annotated[
        str,
        Field(
            default="",
            description="description of where the external URL points towards",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["IRIS DMC Metadata"],
            },
        ),
    ]

    url: Annotated[
        HttpUrl,
        Field(
            default="",
            description="full URL of where the data is stored",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["http://www.iris.edu/mda/EM/NVS11"],
            },
        ),
    ]

    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: input dictionary containing external URL data
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        helpers._read_element(self, input_dict, "external_url")
