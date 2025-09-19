# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import LicenseEnum


# =====================================================


class Copyright(MetadataBase):
    release_license: Annotated[
        LicenseEnum,
        Field(
            default="CC BY 4.0",
            description="How the data can be used. The options are based on https://github.com/spdx/license-list-data",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "CC BY",
                "type": "string",
            },
        ),
    ]

    @field_validator("release_license", mode="before")
    @classmethod
    def validate_license(cls, value: str, info: ValidationInfo) -> str:
        """
        Validate that the value is a valid license.
        """
        value = (
            value.replace("-", "_")
            .replace(" ", "_")
            .replace(".", "_")
            .replace("(", "_")
            .replace(")", "_")
            .replace("/", "_")
            .replace(":", "_")
        )
        if value in LicenseEnum.__members__:
            return LicenseEnum[value].value
        else:
            raise NameError(f"License is not an acceptable license: {value}")
