#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class WeightTypeEnum(str, Enum):
    monotonic = 'monotonic'
    learned = 'learned'
    spatial = 'spatial'
    custom = 'custom'
class Base(MetadataBase):
    weight_type: Annotated[WeightTypeEnum, Field(
    default=''monotonic'',
    description='Type of weighting kernel (e.g., monotonic, learned, spatial).',
    alias=None,
    json_schema_extra={'examples':"['monotonic']",'units':None,'required':True,},

    )]

    description: Annotated[str | None, Field(
    default=None,
    description='Human-readable description of what this kernel is for.',
    alias=None,
    json_schema_extra={'examples':"['This kernel smoothly transitions between 0 and 1 in a monotonic way']",'units':None,'required':False,},

    )]

    active: Annotated[bool | None, Field(
    default=None,
    description='If false, this kernel will be skipped during weighting.',
    alias=None,
    json_schema_extra={'examples':"['false']",'units':None,'required':False,},

    )]
