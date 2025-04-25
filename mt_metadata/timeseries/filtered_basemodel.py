# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated
from typing_extensions import Self, deprecated
from loguru import logger
from pydantic import (
    Field,
    field_validator,
    model_validator,
    ValidationInfo,
)

from mt_metadata.base import MetadataBase
from mt_metadata.common.comment import Comment


# =====================================================

# this will be a better way of keeping track of filter names and
# if they have been applied or not.  This can also include the stage
# number of the filter and could be extended to other attributes.
# TODO: figure out setting a applied and name.


class AppliedFilter(MetadataBase):
    name: Annotated[
        str,
        Field(
            default=None,
            description="Name of the filter.",
            examples="low pass",
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    applied: Annotated[
        bool,
        Field(
            default=True,
            description="Whether the filter has been applied.",
            examples=True,
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    stage: Annotated[
        int | None,
        Field(
            default=None,
            description="Stage of the filter in the processing chain.",
            examples=1,
            json_schema_extra={"units": None, "required": False},
        ),
    ]


class Filtered(MetadataBase):

    filter_list: Annotated[
        list[AppliedFilter],
        Field(
            default_factory=list,
            description="List of AppliedFilter() objects.",
            examples=("[AppliedFilter(name='filter_name', applied=True, stage=1)]"),
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    applied: Annotated[
        list[bool],
        Field(
            default_factory=list,
            description="List of booleans indicating if the filter has been applied.",
            examples=[True, False],
            alias=None,
            deprecated=deprecated(
                "'applied' will be deprecated in the future use an AppliedFilter object."
            ),
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    name: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of filter names.",
            examples=["low pass", "high pass"],
            alias=None,
            deprecated=deprecated(
                "'name' will be deprecated in the future use an AppliedFilter object."
            ),
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments on filters.",
            examples="low pass is not calibrated",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @model_validator(mode="after")
    def validate_applied_and_names(self) -> Self:
        """
        Validate the applied_list to ensure it contains only AppliedFilter objects.
        """
        if self.name != [] or self.applied != []:
            logger.warning(
                "'applied' and 'name' will be deprecated in the future append an "
                "AppliedFilter(name='name', applied=True) to 'filter_list'."
            )
        if len(self.name) != len(self.applied):
            diff = len(self.name) - len(self.applied)
            if diff > 0:
                self.applied.extend([True] * diff)
            else:
                self.name.extend(["unknown"] * abs(diff))
        return self

    # def to_dict(
    #     self, nested=False, single=False, required=True, include_stage=False
    # ) -> OrderedDict:
    #     """
    #     Convert the Filtered object to an OrderedDict. For now stage is not included
    #     for backwards compatibility.  This should be updated in the future.
    #     """
    #     if include_stage:
    #         return OrderedDict(
    #             {
    #                 "applied": self.applied,
    #                 "name": self.name,
    #                 "stage": self.stage,
    #                 "comments": self.comments.to_dict(),
    #             }
    #         )
    #     return OrderedDict(
    #         {
    #             "applied": self.applied,
    #             "name": self.name,
    #             "comments": self.comments.to_dict(),
    #         }
    #     )

    # def from_dict(self, data: dict) -> Self:
    #     """
    #     Populate the Filtered object from a dictionary.
    #     """
    #     applied_list = []
    #     if "stage" in data:
    #         for index in range(len(data["applied"])):
    #             applied_list.append(
    #                 AppliedFilter(
    #                     name=data["name"][index],
    #                     applied=data["applied"][index],
    #                     stage=data["stage"][index],
    #                 )
    #             )
    #     else:
    #         # If "stage" is not in data, use the length of "applied" to determine the number of filters
    #         for index in range(len(data["applied"])):
    #             applied_list.append(
    #                 AppliedFilter(
    #                     name=data["name"][index],
    #                     applied=data["applied"][index],
    #                     stage=index,  # Default to index if stage is not provided
    #                 )
    #             )

    #     self.applied_list = applied_list
