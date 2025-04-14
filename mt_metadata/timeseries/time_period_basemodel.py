#=====================================================
# Imports
#=====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class TimePeriod(MetadataBase):
    end: Annotated[str, Field(
    default=1980-01-01T00:00:00+00:00,
    description='End date and time of collection in UTC.',
    examples='2020-02-04T16:23:45.453670+00:00',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    start: Annotated[str, Field(
    default=1980-01-01T00:00:00+00:00,
    description='Start date and time of collection in UTC.',
    examples='2020-02-01T09:23:45.453670+00:00',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]
