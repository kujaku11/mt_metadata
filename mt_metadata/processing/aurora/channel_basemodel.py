#=====================================================
# Imports
#=====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class Channel(MetadataBase):
    id: Annotated[str, Field(
    default=",
    description='channel ID',
    examples=['mt001'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    scale_factor: Annotated[float, Field(
    default=1.0,
    description='scale factor of the channel',
    examples=['10.0'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]
