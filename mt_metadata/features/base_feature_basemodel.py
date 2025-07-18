#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import Field, field_validator, ValidationInfo


#=====================================================
class DomainEnum(str, Enum):
    time = 'time'
    frequency = 'frequency'
    fc = 'fc'
    ts = 'ts'
    fourier = 'fourier'
class BaseFeature(MetadataBase):
    name: Annotated[str, Field(
    default='',
    description='Name of the feature.',
    alias=None,
    json_schema_extra={'examples':"['simple coherence']",'units':None,'required':True,},

    )]

    description: Annotated[str, Field(
    default='',
    description='A full description of what the feature estimates.',
    alias=None,
    json_schema_extra={'examples':"['Simple coherence measures the coherence between measured electric and magnetic fields.']",'units':None,'required':True,},

    )]

    domain: Annotated[DomainEnum, Field(
    default=''frequency'',
    description="Temporal domain the feature is estimated in [ 'frequency' | 'time' ]",
    alias=None,
    json_schema_extra={'examples':"['frequency']",'units':None,'required':True,},

    )]

    comments: Annotated[Comment, Field(
    default_factory=lambda: Comment(),
    description='Any comments about the feature',
    alias=None,
    json_schema_extra={'examples':"['estimated using hilburt transform.']",'units':None,'required':False,},

    )]

    @field_validator('comments', mode='before')
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value
