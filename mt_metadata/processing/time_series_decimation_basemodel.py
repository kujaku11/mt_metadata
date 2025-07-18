#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class MethodEnum(str, Enum):
    default = 'default'
    other = 'other'
class TimeSeriesDecimation(MetadataBase):
    level: Annotated[int, Field(
    default=None,
    description='Decimation level, must be a non-negative integer starting at 0',
    alias=None,
    json_schema_extra={'examples':"['0']",'units':None,'required':True,},

    )]

    factor: Annotated[float, Field(
    default=1.0,
    description='Decimation factor between parent sample rate and decimated time series sample rate.',
    alias=None,
    json_schema_extra={'examples':"['4.0']",'units':None,'required':True,},

    )]

    method: Annotated[MethodEnum, Field(
    default=''default'',
    description='Type of decimation',
    alias=None,
    json_schema_extra={'examples':"['default']",'units':'','required':True,},

    )]

    sample_rate: Annotated[float, Field(
    default=1.0,
    description='Sample rate of the decimation level data (after decimation).',
    alias=None,
    json_schema_extra={'examples':"['256']",'units':'samples per second','required':True,},

    )]

    anti_alias_filter: Annotated[str, Field(
    default=''default'',
    description='Type of anti alias filter for decimation.',
    alias=None,
    json_schema_extra={'examples':"['default']",'units':None,'required':True,},

    )]
