# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, HttpUrl

from mt_metadata.common import Citation as CommonCitation
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class Citation(CommonCitation):
    survey_d_o_i: Annotated[
        HttpUrl | None,
        Field(
            default=None,
            description="doi number of the survey",
            examples=["###/###"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=[
                "title",
                "authors",
                "year",
                "survey_d_o_i",
            ],
        )
