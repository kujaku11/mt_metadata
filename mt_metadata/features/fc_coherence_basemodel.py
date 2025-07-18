#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class BandDefinitionTypeEnum(str, Enum):
    Q = 'Q'
    fractional_bandwidth = 'fractional bandwidth'
    user_defined = 'user defined'
class QRadiusEnum(str, Enum):
    constant_Q = 'constant Q'
    user_defined = 'user defined'
class FcCoherence(MetadataBase):
    channel_1: Annotated[str, Field(
    default='',
    description='The first channel of two channels in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['ex']",'units':None,'required':True,},

    )]

    channel_2: Annotated[str, Field(
    default='',
    description='The second channel of two channels in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['hy']",'units':None,'required':True,},

    )]

    minimum_fcs: Annotated[int, Field(
    default=None,
    description='The minimum number of Fourier coefficients needed to compute the feature.',
    alias=None,
    json_schema_extra={'examples':"['2']",'units':None,'required':True,},

    )]

    band_definition_type: Annotated[BandDefinitionTypeEnum, Field(
    default=''Q'',
    description='How the feature frequency bands are defined.',
    alias=None,
    json_schema_extra={'examples':"['user defined']",'units':None,'required':True,},

    )]

    q_radius: Annotated[QRadiusEnum, Field(
    default=''constant Q'',
    description='How the feature frequency bands are defined.',
    alias=None,
    json_schema_extra={'examples':"['user defined']",'units':None,'required':True,},

    )]
