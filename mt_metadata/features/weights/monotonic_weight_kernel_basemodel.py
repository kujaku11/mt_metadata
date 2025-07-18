#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class ThresholdEnum(str, Enum):
    low_cut = 'low cut'
    high_cut = 'high cut'
class StyleEnum(str, Enum):
    taper = 'taper'
    activation = 'activation'
class MonotonicWeightKernel(MetadataBase):
    threshold: Annotated[ThresholdEnum, Field(
    default=''low cut'',
    description='Which side of a threshold should be downweighted.',
    alias=None,
    json_schema_extra={'examples':"['low cut']",'units':None,'required':True,},

    )]

    style: Annotated[StyleEnum, Field(
    default=''taper'',
    description='Tapering/activation function to use between transition bounds.',
    alias=None,
    json_schema_extra={'examples':"['activation']",'units':None,'required':True,},

    )]

    transition_lower_bound: Annotated[float, Field(
    default=-1000000000.0,
    description='Start of the taper region (weight begins to change).',
    alias=None,
    json_schema_extra={'examples':"['-inf']",'units':None,'required':True,},

    )]

    transition_upper_bound: Annotated[float, Field(
    default=1000000000.0,
    description='End of the taper region (weight finishes changing).',
    alias=None,
    json_schema_extra={'examples':"['+inf']",'units':None,'required':True,},

    )]
