#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class CenterAveragingTypeEnum(str, Enum):
    arithmetic = 'arithmetic'
    geometric = 'geometric'
class ClosedEnum(str, Enum):
    left = 'left'
    right = 'right'
    both = 'both'
class Band(MetadataBase):
    decimation_level: Annotated[int, Field(
    default=None,
    description='Decimation level for the band',
    alias=None,
    json_schema_extra={'examples':"['0']",'units':None,'required':True,},

    )]

    index_max: Annotated[int, Field(
    default=None,
    description='maximum band index',
    alias=None,
    json_schema_extra={'examples':"['10']",'units':None,'required':True,},

    )]

    index_min: Annotated[int, Field(
    default=None,
    description='minimum band index',
    alias=None,
    json_schema_extra={'examples':"['10']",'units':None,'required':True,},

    )]

    frequency_max: Annotated[float, Field(
    default=0.0,
    description='maximum band frequency',
    alias=None,
    json_schema_extra={'examples':"['0.04296875']",'units':'Hertz','required':True,},

    )]

    frequency_min: Annotated[float, Field(
    default=0.0,
    description='minimum band frequency',
    alias=None,
    json_schema_extra={'examples':"['0.03515625']",'units':'Hertz','required':True,},

    )]

    center_averaging_type: Annotated[CenterAveragingTypeEnum, Field(
    default=''geometric'',
    description='type of average to apply when computing the band center',
    alias=None,
    json_schema_extra={'examples':"['geometric']",'units':None,'required':True,},

    )]

    closed: Annotated[ClosedEnum, Field(
    default=''left'',
    description='whether interval is open or closed',
    alias=None,
    json_schema_extra={'examples':"['left']",'units':None,'required':True,},

    )]
