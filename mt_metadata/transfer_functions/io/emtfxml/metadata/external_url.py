# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, HttpUrl

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
        HttpUrl | str,
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

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: HttpUrl | str | None, info=None) -> HttpUrl | str:
        # Normalize None to empty string
        if value is None:
            value = ""

        # If setting to empty string after a non-empty value, disallow
        try:
            existing = None
            if info is not None and hasattr(info, "data") and info.data is not None:
                existing = info.data.get("url")
        except Exception:
            existing = None

        if value == "":
            if existing not in [None, ""]:
                raise ValueError("Cannot assign empty URL after it has been set")
            return ""

        # If already a HttpUrl, return it
        if isinstance(value, HttpUrl):
            return value

        # Validate string URL via HttpUrl
        return HttpUrl(value)

    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: input dictionary containing external URL data
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        helpers._read_element(self, input_dict, "external_url")
