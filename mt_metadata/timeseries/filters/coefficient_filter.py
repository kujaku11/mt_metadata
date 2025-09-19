import numpy as np
try:
    from obspy.core import inventory
except ImportError:
    inventory = None

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS
from mt_metadata.base.helpers import write_lines, requires

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("coefficient_filter", SCHEMA_FN_PATHS))
# =============================================================================


class CoefficientFilter(FilterBase):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__()

        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        self.type = "coefficient"

        if self.gain == 0.0:
            self.gain = 1.0

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
            self.units_in,
            self.units_out,
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
            input_units_description=self._units_in_obj.name,
            output_units_description=self._units_out_obj.name,
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
