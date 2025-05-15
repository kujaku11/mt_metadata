# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class ReleaseStatusEnum(str, Enum):
    Unrestricted_release = "Unrestricted release"
    Restricted_release = "Restricted release"
    Paper_Citation_Required = "Paper Citation Required"
    Academic_Use_Only = "Academic Use Only"
    Conditions_Apply = "Conditions Apply"
    Data_Citation_Required = "Data Citation Required"


class Copyright(MetadataBase):
    selected_publications: Annotated[
        str | None,
        Field(
            default=None,
            description="Any publications that use this data",
            examples="my paper",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    release_status: Annotated[
        ReleaseStatusEnum,
        Field(
            default="Unrestricted Release",
            description="the release status of the data",
            examples="Unrestricted release",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    conditions_of_use: Annotated[
        str,
        Field(
            default="All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided this data set is cited as the reference. While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, not IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.",
            description="Any notes on conditions of use",
            examples="Cite data upon usage.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    acknowledgement: Annotated[
        str | None,
        Field(
            default=None,
            description="any acknowledgments the transfer function should have.",
            examples="This project was funded by x.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    additional_info: Annotated[
        str | None,
        Field(
            default=None,
            description="any additional information about the data.",
            examples="This purpose of this project is ...",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
