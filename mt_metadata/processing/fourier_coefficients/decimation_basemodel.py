#=====================================================
# Imports
#=====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class Decimation(MetadataBase):
    id: Annotated[str, Field(
    default=",
    description='Decimation level ID',
    examples=['1'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    channels_estimated: Annotated[str, Field(
    default='[]',
    items={'type': 'string'},
    description='list of channels',
    examples=['[ex, hy]'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]
