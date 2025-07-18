#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class BandSpecificationStyleEnum(str, Enum):
    EMTF = 'EMTF'
    band_edges = 'band_edges'
class Processing(MetadataBase):
    decimations: Annotated[str, Field(
    default='[]',
    items={'type': 'string'},
    description='decimation levels',
    examples=['0'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]

    band_specification_style: Annotated[BandSpecificationStyleEnum | None, Field(
    default=None,
    description='describes how bands were sourced',
    examples=['EMTF'],
    alias=None,
    json_schema_extra={'units':None,'required':False,},

    )]

    band_setup_file: Annotated[str | None, Field(
    default=None,
    description='the band setup file used to define bands',
    examples=['/home/user/bs_test.cfg'],
    alias=None,
    json_schema_extra={'units':None,'required':False,},

    )]

    id: Annotated[str, Field(
    default=",
    description='Configuration ID',
    examples=['0'],
    alias=None,
    json_schema_extra={'units':None,'required':True,},

    )]
