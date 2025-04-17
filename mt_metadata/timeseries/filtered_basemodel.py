# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated
from typing_extensions import Self
from pydantic import (
    Field,
    computed_field,
    field_validator,
    ValidationInfo,
)

from mt_metadata.base import MetadataBase
from mt_metadata.common.comment_basemodel import Comment


# =====================================================
class Filtered(MetadataBase):
    applied_dict: OrderedDict[str, bool] = {
        Field(
            default_factory=OrderedDict,
            description="Dictionary of filter names and if they have been applied.",
            examples='{"lowpass_magnetic": True, "counts2mv": False}',
            json_schema_extra={
                "units": None,
                "required": True,
            },
        )
    }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def applied(self) -> list[bool]:
        """
        Return a list of booleans indicating if the filter has been applied.
        """
        return list(self.applied_dict.values())

    @computed_field  # type: ignore[prop-decorator]
    @property
    def name(self) -> list[str]:
        """
        Return a list of filter names.
        """
        return list(self.applied_dict.keys())

    @name.setter
    def name(self, value: list[str]) -> None:
        """
        Set the filter names.
        """
        for name in value:
            self.applied_dict[name] = self.applied_dict.get(name, True)

    # this won't work see https://github.com/pydantic/pydantic/issues/1577
    # def __setattr__(self, key, val):
    #     method = self.__config__.property_set_methods.get(key)
    #     if method is None:
    #         super().__setattr__(key, val)
    #     else:
    #         getattr(self, method)(val)

    # class Config:
    #     property_set_methods = {"coords": "set_coords"}
    @applied.setter
    def applied(self, value: list[bool]) -> None:
        """
        Set the filter names.
        """
        if len(value) != len(self.applied_dict.keys()):
            raise ValueError(
                "Length of applied list must match length of filter names."
            )

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
