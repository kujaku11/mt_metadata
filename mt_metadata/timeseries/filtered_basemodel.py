# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated
from typing_extensions import Self
from pydantic import Field, computed_field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================

# this will be a better way of keeping track of filter names and
# if they have been applied or not.  This can also include the stage
# number of the filter and could be extended to other attributes.


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
            default=False,
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
    applied_list: Annotated[
        list[AppliedFilter],
        Field(
            default_factory=list,
            description="List of applied filters.",
            examples=["AppliedFilter(name='low pass', applied=True)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @computed_field
    def applied(self) -> list[bool]:
        """
        Return a list of booleans indicating if the filter has been applied.
        """
        return [filter.applied for filter in self.applied_list]

    @computed_field
    def name(self) -> list[str]:
        """
        Return a list of filter names.
        """
        return [filter.name for filter in self.applied_list]

    @computed_field
    def stage(self) -> list[int | None]:
        """
        Return a list of filter stages.
        """
        return [filter.stage for filter in self.applied_list]

    comments: Annotated[
        Comment | None,
        Field(
            default=None,
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

    def to_dict(
        self, nested=False, single=False, required=True, include_stage=False
    ) -> OrderedDict:
        """
        Convert the Filtered object to an OrderedDict. For now stage is not included
        for backwards compatibility.  This should be updated in the future.
        """
        if include_stage:
            return OrderedDict(
                {
                    "applied": self.applied,
                    "name": self.name,
                    "stage": self.stage,
                    "comments": self.comments,
                }
            )
        return OrderedDict(
            {
                "applied": self.applied,
                "name": self.name,
                "comments": self.comments,
            }
        )

    def from_dict(self, data: dict) -> Self:
        """
        Populate the Filtered object from a dictionary.
        """
        applied_list = []
        if "stage" in data:
            for index in range(len(data["applied"])):
                applied_list.append(
                    AppliedFilter(
                        name=data["name"][index],
                        applied=data["applied"][index],
                        stage=data["stage"][index],
                    )
                )
        else:
            # If "stage" is not in data, use the length of "applied" to determine the number of filters
            for index in range(len(data["applied"])):
                applied_list.append(
                    AppliedFilter(
                        name=data["name"][index],
                        applied=data["applied"][index],
                        stage=index,  # Default to index if stage is not provided
                    )
                )

        self.applied_list = applied_list
