# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Job(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
            description="name of the job",
            examples=["yellowstone"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    job_for: Annotated[
        str | None,
        Field(
            default=None,
            description="who the job is for",
            examples=["NSF"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
