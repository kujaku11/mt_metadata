# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, HttpUrl

from mt_metadata.base import MetadataBase


# =====================================================
class ExternalUrl(MetadataBase):
    description: Annotated[
        str,
        Field(
            default="",
            description="description of where the external URL points towards",
            examples="IRIS DMC Metadata",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    url: Annotated[
        HttpUrl,
        Field(
            default="",
            description="full URL of where the data is stored",
            examples="http://www.iris.edu/mda/EM/NVS11",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
