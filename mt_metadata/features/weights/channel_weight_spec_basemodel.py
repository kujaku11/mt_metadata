"""
Container for weighting strategy to apply to a single tf estimation
having a single output channel (usually one of "ex", "ey", "hz").

candidate data structure is stored in test_helpers/channel_weight_specs_example.json

Candidate names: processing_weights, feature_weights, channel_weights_spec, channel_weighting

Notes, and doc for weights PR.

channel_weight_specs is a candidate name for the json block like the following:
>>> diff processing_configuration_template.json test_processing_config_with_weights_block.json
(Another candidate name could be `processing_weights`, or `weights`, but the final nomenclature
can be sorted out after there is a functional prototype with the appropriate structure.)


This block is basically a dict that maps an output channel name to a ChannelWeightSpec (CWS) object.

There are at least three places we would like to be able to plug in such a dict to the processing flow.
1. At the frequency_band level, so that each band can be associated with a specialty CWS
2. At the decimation_level level, so that all bands in a GIB have a common, default.
3. At a high level, so that all processing uses them.
TAI: In future, hopefully we could insert a custom CWS for a specific band, but leave
all other bands to use the DecimationLevel default CWS, for example.  i.e. the CWS can
be defined for different scopes.

TODO FIXME: IN mt_metadata/transfer_functions/processing/auaora/processing.py
when you output a json, it looks like the `decimations` level should be named:
`decimation_levels` instead.

The general model I'll try to follow will be to open an itearable of objects
with a plural of the object name. For example, the processing block called "bands"
follows with an itearble of:
{
    "band": {
        "center_averaging_type": "geometric",
        ...
        "index_min": 25
    }
}
...
{
    "band": {
        "center_averaging_type": "geometric",
        ...
        "index_min": 25
    }
}

Will start by plugging this into the DecimationLevel.

TODO: Determine if this class, which represents a single element of a list
of channel weight specs, which will be in the json, should have a wrapper or not.

In the same way that a DecimationLevel has Bands,
it will also have ChannelWeightSpecs.
"""

# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class CombinationStyleEnum(StrEnumerationBase):
    multiplication = "multiplication"
    minimum = "minimum"
    maximum = "maximum"
    mean = "mean"


class ChannelWeightSpec(MetadataBase):
    combination_style: Annotated[
        CombinationStyleEnum,
        Field(
            default="multiplication",
            description="How to combine multiple feature weights.",
            examples=["multiplication"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of tf ouput channels for which this weighting scheme will be applied",
            examples=["[ ex ey hz ]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    feature_weight_specs: Annotated[
        int,
        Field(
            default=None,
            items={"type": "integer"},
            description="List of feature weighting schemes to use for TF processing.",
            examples=["[]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
