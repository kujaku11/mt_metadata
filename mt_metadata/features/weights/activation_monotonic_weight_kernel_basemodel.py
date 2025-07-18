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
class ActivationStyleEnum(str, Enum):
    sigmoid = 'sigmoid'
    hard_sigmoid = 'hard_sigmoid'
    tanh = 'tanh'
    hard_tanh = 'hard_tanh'
class ActivationMonotonicWeightKernel(MetadataBase):
    threshold: Annotated[ThresholdEnum, Field(
    default=''low cut'',
    description='Which side of a threshold should be downweighted.',
    alias=None,
    json_schema_extra={'examples':"['low cut']",'units':None,'required':True,},

    )]

    activation_style: Annotated[ActivationStyleEnum, Field(
    default=''sigmoid'',
    description='Tapering/activation function to use between transition bounds.',
    alias=None,
    json_schema_extra={'examples':"['tanh']",'units':None,'required':True,},

    )]

    steepness: Annotated[float | None, Field(
    default=None,
    description='Controls the sharpness of the activation transition.',
    alias=None,
    json_schema_extra={'examples':"['10']",'units':None,'required':False,},

    )]
