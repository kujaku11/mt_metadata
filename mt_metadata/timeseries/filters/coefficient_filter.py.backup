# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from pydantic import Field, PrivateAttr

from mt_metadata.timeseries.filters import FilterBase


try:
    from obspy.core import inventory
except ImportError:
    inventory = None

from mt_metadata.base.helpers import requires


# =====================================================
class CoefficientFilter(FilterBase):
    _filter_type: str = PrivateAttr("coefficient")
    type: Annotated[
        str,
        Field(
            default="coefficient",
            description="Type of filter.  Must be 'coefficient'",
            examples=["coefficient"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="Scale factor for a simple coefficient filter.",
            examples=["100"],
            alias=None,
            gt=0.0,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @requires(obspy=inventory)
    def to_obspy(
        self,
        stage_number=1,
        cf_type="DIGITAL",
        sample_rate=1,
        normalization_frequency=0,
    ):
        """
        stage_sequence_number,
        stage_gain,
        stage_gain_frequency,
        input_units,
        output_units,
        cf_transfer_function_type,
        resource_id=None,
        resource_id2=None,
        name=None,
        numerator=None,
        denominator=None,
        input_units_description=None,
        output_units_description=None,
        description=None,
        decimation_input_sample_rate=None,
        decimation_factor=None,
        decimation_offset=None,
        decimation_delay=None,
        decimation_correction=None

        :param stage_number: DESCRIPTION, defaults to 1
        :type stage_number: TYPE, optional
        :param cf_type: DESCRIPTION, defaults to "DIGITAL"
        :type cf_type: TYPE, optional
        :param sample_rate: DESCRIPTION, defaults to 1
        :type sample_rate: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        stage = inventory.CoefficientsTypeResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in_object.symbol,
            self.units_out_object.symbol,
            cf_type,
            name=self.name,
            decimation_input_sample_rate=sample_rate,
            decimation_factor=1,
            decimation_offset=0,
            decimation_delay=0,
            decimation_correction=0,
            numerator=[1],
            denominator=[],
            description=self.get_filter_description(),
            input_units_description=self.units_in_object.name,
            output_units_description=self.units_out_object.name,
        )

        return stage

    def complex_response(self, frequencies, **kwargs):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        if isinstance(frequencies, (float, int)):
            frequencies = np.array([frequencies])
        return self.gain * np.ones(len(frequencies), dtype=complex)
