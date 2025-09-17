# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from loguru import logger
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string

from . import Estimate


# =====================================================
class StatisticalEstimates(MetadataBase):
    estimates_list: Annotated[
        list[Estimate | dict] | dict,
        Field(
            default_factory=list,
            description="list of statistical estimates",
            examples=["[var cov]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("estimates_list", mode="before")
    @classmethod
    def validate_estimates_list(cls, value: list) -> list[Estimate]:
        if not isinstance(value, list):
            value = [value]
        estimates_list = []
        for item in value:
            est = Estimate()  # type: ignore
            if isinstance(item, dict):
                est.from_dict(item)
            elif isinstance(item, Estimate):
                est = item
            else:
                est.name = item
            estimates_list.append(est)
        return estimates_list

    def read_dict(self, input_dict: dict) -> None:
        """
        Read in statistical estimate descriptions

        :param input_dict: input dictionary containing statistical estimates
        :type input_dict: dict
        :return: None
        :rtype: None

        """

        try:
            self.estimates_list = input_dict["statistical_estimates"]["estimate"]
        except KeyError:
            logger.warning("Could not statistical estimates")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the StatisticalEstimates instance to XML format.

        Parameters
        ----------
        string : bool, optional
            If True, return the XML as a string, by default False
        required : bool, optional
            If True, include required fields in the XML, by default True

        Returns
        -------
        str | et.Element
            The XML representation of the instance
        """

        root = et.Element(self.__class__.__name__)

        for estimate in self.estimates_list:
            root.append(estimate.to_xml(required=required))  # type: ignore

        if string:
            return element_to_string(root)
        return root
