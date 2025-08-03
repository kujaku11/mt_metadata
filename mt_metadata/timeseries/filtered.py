# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

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
            examples=["low pass"],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    applied: Annotated[
        bool,
        Field(
            default=True,
            description="Whether the filter has been applied.",
            examples=["True"],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    stage: Annotated[
        int | None,
        Field(
            default=None,
            description="Stage of the filter in the processing chain.",
            examples=[1],
            json_schema_extra={"units": None, "required": False},
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),  # type: ignore
            description="Any comments on filters.",
            examples=["low pass is not calibrated"],
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


# class Filter(MetadataBase):
#     _objects_included: dict = PrivateAttr(
#         default_factory=lambda: {"applied_filter": AppliedFilter}
#     )

#     filter_list: Annotated[
#         list[AppliedFilter],
#         Field(
#             default_factory=list,
#             description="List of AppliedFilter() objects.",
#             examples=["[AppliedFilter(name='filter_name', applied=True, stage=1)]"],
#             alias=None,
#             json_schema_extra={
#                 "units": None,
#                 "required": False,
#             },
#         ),
#     ]

#     applied: Annotated[
#         list[bool],
#         Field(
#             default_factory=list,
#             description="List of booleans indicating if the filter has been applied.",
#             examples=[True, False],
#             alias=None,
#             deprecated=deprecated(
#                 "'applied' will be deprecated in the future use an AppliedFilter object."
#             ),
#             json_schema_extra={
#                 "units": None,
#                 "required": False,
#             },
#         ),
#     ]

#     name: Annotated[
#         list[str],
#         Field(
#             default_factory=list,
#             description="List of filter names.",
#             examples=["low pass", "high pass"],
#             alias=None,
#             deprecated=deprecated(
#                 "'name' will be deprecated in the future use an AppliedFilter object."
#             ),
#             json_schema_extra={
#                 "units": None,
#                 "required": False,
#             },
#         ),
#     ]

#     comments: Annotated[
#         Comment,
#         Field(
#             default_factory=Comment,
#             description="Any comments on filters.",
#             examples=["low pass is not calibrated"],
#             alias=None,
#             json_schema_extra={
#                 "units": None,
#                 "required": False,
#             },
#         ),
#     ]

#     @field_validator("comments", mode="before")
#     @classmethod
#     def validate_comments(cls, value, info: ValidationInfo) -> Comment:
#         """
#         Validate that the value is a valid comment.
#         """
#         if isinstance(value, str):
#             return Comment(value=value)
#         return value

#     @model_validator(mode="after")
#     def validate_applied_and_names(self) -> Self:
#         """
#         Validate the applied_list to ensure it contains only AppliedFilter objects.
#         """
#         if self.name != [] or self.applied != []:
#             logger.warning(
#                 "'applied' and 'name' will be deprecated in the future append an "
#                 "AppliedFilter(name='name', applied=True) to 'filter_list'."
#             )

#         if len(self.name) != len(self.applied):
#             diff = len(self.name) - len(self.applied)
#             if diff > 0:
#                 self.applied.extend([True] * diff)
#             else:
#                 self.name.extend(["unknown"] * abs(diff))

#         if len(self.name) != len(self.filter_list):
#             for name, applied, index in zip(
#                 self.name, self.applied, range(len(self.name))
#             ):
#                 self.filter_list.append(
#                     AppliedFilter(name=name, applied=applied, stage=index + 1)
#                 )

#         return self

#     def to_dict(
#         self, single: bool = False, nested: bool = False, required: bool = True
#     ) -> dict:
#         """
#         Convert the object to a dictionary. To be compliant with older versions
#         of the metadata, use name and applied as lists

#         Parameters
#         ----------
#         single : bool, optional
#             Whether to return a single dictionary or a list of dictionaries,
#             by default False.

#         Returns
#         -------
#         dict
#             Dictionary representation of the object.
#         """
#         d = OrderedDict()
#         d["name"] = self.name
#         d["applied"] = self.applied
#         d["comments"] = self.comments.to_dict(single=single, nested=nested)
#         return d

#     def add_filter(
#         self,
#         applied_filter: AppliedFilter = None,
#         name: str = None,
#         applied: bool = True,
#         stage: int | None = None,
#     ) -> None:
#         """
#         Add a filter to the filter list.

#         Parameters
#         ----------
#         name : str
#             Name of the filter.
#         applied : bool, optional
#             Whether the filter has been applied, by default True.
#         stage : int | None, optional
#             Stage of the filter in the processing chain, by default None.
#         """
#         if applied_filter is not None:
#             if not isinstance(applied_filter, AppliedFilter):
#                 raise TypeError("applied_filter must be an instance of AppliedFilter")
#             if applied_filter.stage is None:
#                 applied_filter.stage = len(self.filter_list) + 1
#             self.filter_list.append(applied_filter)
#         else:
#             if name is None:
#                 raise ValueError("name must be provided if applied_filter is None")
#             if not isinstance(name, str):
#                 raise TypeError("name must be a string")
#             if stage is None:
#                 stage = len(self.filter_list) + 1
#             self.filter_list.append(
#                 AppliedFilter(name=name, applied=applied, stage=stage)
#             )

#     def remove_filter(self, name: str, reset_stages: bool = True) -> None:
#         """
#         Remove a filter from the filter list.

#         Parameters
#         ----------
#         name : str
#             Name of the filter to remove.
#         reset_stages : bool, optional
#             Whether to reset the stages of the remaining filters, by default True.
#         """

#         new_list = []
#         for f in self.filter_list:
#             if f.name == name:
#                 continue
#             if reset_stages:
#                 f.stage = len(new_list) + 1
#             new_list.append(f)
#         self.filter_list = new_list
