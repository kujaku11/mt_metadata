#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class MethodEnum(str, Enum):
    fft = 'fft'
    wavelet = 'wavelet'
    other = 'other'
class Fc(MetadataBase):
    decimation_levels: Annotated[str, Field(
    default='[]',
    items={'type': 'string'},
    description='List of decimation levels',
    examples=['[1, 2, 3]'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    id: Annotated[str, Field(
    default=",
    description='ID given to the FC group',
    examples=['aurora_01'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    channels_estimated: Annotated[str, Field(
    default='[]',
    items={'type': 'string'},
    description='list of channels estimated',
    examples=['[ex, hy]'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    starting_sample_rate: Annotated[float, Field(
    default=1.0,
    description='Starting sample rate of the time series used to estimate FCs.',
    examples=[60],
    alias=None,
    json_schema_extra={'units':'samples per second','required':True,},

    )]

    method: Annotated[MethodEnum, Field(
    default="fft",
    description='Fourier transform method',
    examples=['fft'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]
