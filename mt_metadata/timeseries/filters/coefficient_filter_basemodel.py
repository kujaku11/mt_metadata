# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.timeseries.filters.filter_base_basemodel import FilterBase


# =====================================================
class CoefficientFilter(FilterBase):
    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="Scale factor for a simple coefficient filter.",
            examples="100",
            alias=None,
            gt=0.0,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
