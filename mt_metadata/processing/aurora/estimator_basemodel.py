#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class EngineEnum(str, Enum):
    RME_RR = 'RME_RR'
    RME = 'RME'
    other = 'other'
class Estimator(MetadataBase):
    engine: Annotated[EngineEnum, Field(
    default=''RME_RR'',
    description='The transfer function estimator engine',
    alias=None,
    json_schema_extra={'examples':"['RME_RR']",'units':None,'required':True,},

    )]

    estimate_per_channel: Annotated[bool, Field(
    default=True,
    description='Estimate per channel',
    alias=None,
    json_schema_extra={'examples':"['True']",'units':None,'required':True,},

    )]
