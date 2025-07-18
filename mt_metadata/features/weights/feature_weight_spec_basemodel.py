#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


#=====================================================
class FeatureNameEnum(str, Enum):
    coherence = 'coherence'
    multiple_coherence = 'multiple coherence'
class FeatureWeightSpec(MetadataBase):
    feature_name: Annotated[FeatureNameEnum, Field(
    default='''',
    description='The name of the feature to evaluate (e.g., coherence, impedance_ratio).',
    alias=None,
    json_schema_extra={'examples':"['coherence']",'units':None,'required':True,},

    )]
