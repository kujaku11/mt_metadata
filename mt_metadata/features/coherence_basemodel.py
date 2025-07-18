#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class DetrendEnum(str, Enum):
    linear = 'linear'
    constant = 'constant'
class Coherence(MetadataBase):
    ch1: Annotated[str, Field(
    default='',
    description='The first channel of two channels in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['ex']",'units':None,'required':True,},

    )]

    ch2: Annotated[str, Field(
    default='',
    description='The second channel of two channels in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['hy']",'units':None,'required':True,},

    )]

    detrend: Annotated[DetrendEnum, Field(
    default=''linear'',
    description='How to detrend the data segments before fft.',
    alias=None,
    json_schema_extra={'examples':"['constant']",'units':None,'required':True,},

    )]

    station1: Annotated[str, Field(
    default='''',
    description='The station associated with the first channel in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['PKD']",'units':None,'required':True,},

    )]

    station2: Annotated[str, Field(
    default='''',
    description='The station associated with the second channel in the coherence calculation.',
    alias=None,
    json_schema_extra={'examples':"['SAO']",'units':None,'required':True,},

    )]
