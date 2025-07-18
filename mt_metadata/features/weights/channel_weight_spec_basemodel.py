#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class CombinationStyleEnum(str, Enum):
    multiplication = 'multiplication'
    minimum = 'minimum'
    maximum = 'maximum'
    mean = 'mean'
class ChannelWeightSpec(MetadataBase):
    combination_style: Annotated[CombinationStyleEnum, Field(
    default=''multiplication'',
    description='How to combine multiple feature weights.',
    alias=None,
    json_schema_extra={'examples':"['multiplication']",'units':None,'required':True,},

    )]

    output_channels: Annotated[str, Field(
    default='[]',
    items={'type': 'string'},
    description='list of tf ouput channels for which this weighting scheme will be applied',
    alias=None,
    json_schema_extra={'examples':"['[ ex ey hz ]']",'units':None,'required':True,},

    )]

    feature_weight_specs: Annotated[int, Field(
    default=None,
    items={'type': 'integer'},
    description='List of feature weighting schemes to use for TF processing.',
    alias=None,
    json_schema_extra={'examples':"['[]']",'units':None,'required':True,},

    )]
