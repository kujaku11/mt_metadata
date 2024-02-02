# -*- coding: utf-8 -*-
"""
.. module:: TF
   :synopsis: The main container for transfer functions

.. moduleauthor:: Jared Peacock <jpeacock@usgs.gov>
"""

# ==============================================================================
from pathlib import Path
from copy import deepcopy
from collections import OrderedDict

import numpy as np
import xarray as xr

from loguru import logger

from mt_metadata.timeseries import Survey as TSSurvey
from mt_metadata.transfer_functions.tf import (
    Survey,
    Station,
    Run,
    Electric,
    Magnetic,
)
from mt_metadata.transfer_functions.io import (
    EDI,
    EMTFXML,
    ZMM,
    JFile,
    ZongeMTAvg,
)
from mt_metadata.transfer_functions.io.zfiles.metadata import (
    Channel as ZChannel,
)
from mt_metadata.base.helpers import validate_name
from mt_metadata.utils.list_dict import ListDict
from mt_metadata.transfer_functions import DEFAULT_CHANNEL_NOMENCLATURE

# =============================================================================


class TF:
    """
    Generic container to hold information about an electromagnetic
    transfer funtion

    The thought here is to have a central container TF.dataset which is an
    xarray.Dataset that contains the impedance, tipper, errors and covariance
    values.  There are helper functions to get and set these from the
    TF.dataset.  Cause most of the time the user will want just the impedance
    or the tipper and associated errors.  We are accommodating EMTF style
    covariances to accurately rotated data errors.

    When reading and writing edi files this information will be lost.

    """

    def __init__(self, fn=None, **kwargs):
        self.logger = logger

        # set metadata for the station
        self._survey_metadata = self._initialize_metadata()
        self.channel_nomenclature = DEFAULT_CHANNEL_NOMENCLATURE
        self._inverse_channel_nomenclature = {}

        self._rotation_angle = 0
        self.save_dir = Path.cwd()

        self._dataset_attr_dict = {
            "survey": "survey_metadata.id",
            "project": "survey_metadata.project",
            "id": "station_metadata.id",
            "name": "station_metadata.geographic_name",
            "latitude": "station_metadata.location.latitude",
            "longitude": "station_metadata.location.longitude",
            "elevation": "station_metadata.location.elevation",
            "declination": "station_metadata.location.declination.value",
            "datum": "station_metadata.location.datum",
            "acquired_by": "station_metadata.acquired_by.author",
            "start": "station_metadata.time_period.start",
            "end": "station_metadata.time_period.end",
            "runs_processed": "station_metadata.run_list",
            "coordinate_system": "station_metadata.orientation.reference_frame",
        }

        self._read_write_dict = {
            "edi": {"write": self.to_edi, "read": self.from_edi},
            "xml": {"write": self.to_emtfxml, "read": self.from_emtfxml},
            "emtfxml": {"write": self.to_emtfxml, "read": self.from_emtfxml},
            "j": {"write": self.to_jfile, "read": self.from_jfile},
            "zmm": {"write": self.to_zmm, "read": self.from_zmm},
            "zrr": {"write": self.to_zrr, "read": self.from_zrr},
            "zss": {"write": self.to_zss, "read": self.from_zss},
            "avg": {"write": self.to_avg, "read": self.from_avg},
        }

        tf_set = False
        try:
            period = kwargs.pop("period")
            self._transfer_function = self._initialize_transfer_function(
                periods=period
            )
            tf_set = True
        except KeyError:
            try:
                period = 1.0 / kwargs.pop("frequency")
                self._transfer_function = self._initialize_transfer_function(
                    periods=period
                )
                tf_set = True
            except KeyError:
                pass
            pass

        for key, value in kwargs.items():
            setattr(self, key, value)

        if not tf_set:
            self._transfer_function = self._initialize_transfer_function()

        self.fn = fn

    @property
    def inverse_channel_nomenclature(self):
        if not self._inverse_channel_nomenclature:
            self._inverse_channel_nomenclature = {
                v: k for k, v in self.channel_nomenclature.items()
            }
        return self._inverse_channel_nomenclature

    def __str__(self):
        lines = [f"Station: {self.station}", "-" * 50]
        lines.append(f"\tSurvey:            {self.survey_metadata.id}")
        lines.append(f"\tProject:           {self.survey_metadata.project}")
        lines.append(
            f"\tAcquired by:       {self.station_metadata.acquired_by.author}"
        )
        lines.append(
            f"\tAcquired date:     {self.station_metadata.time_period.start_date}"
        )
        lines.append(f"\tLatitude:          {self.latitude:.3f}")
        lines.append(f"\tLongitude:         {self.longitude:.3f}")
        lines.append(f"\tElevation:         {self.elevation:.3f}")
        lines.append("\tDeclination:   ")
        lines.append(
            f"\t\tValue:     {self.station_metadata.location.declination.value}"
        )
        lines.append(
            f"\t\tModel:     {self.station_metadata.location.declination.model}"
        )
        lines.append(
            f"\tCoordinate System: {self.station_metadata.orientation.reference_frame}"
        )

        lines.append(f"\tImpedance:         {self.has_impedance()}")
        lines.append(f"\tTipper:            {self.has_tipper()}")

        if self.period is not None:
            lines.append(f"\tN Periods:     {len(self.period)}")

            lines.append("\tPeriod Range:")
            lines.append(f"\t\tMin:   {self.period.min():.5E} s")
            lines.append(f"\t\tMax:   {self.period.max():.5E} s")

            lines.append("\tFrequency Range:")
            lines.append(f"\t\tMin:   {1./self.period.max():.5E} Hz")
            lines.append(f"\t\tMax:   {1./self.period.min():.5E} Hz")
        return "\n".join(lines)

    def __repr__(self):
        lines = []
        lines.append(f"survey='{self.survey}'")
        lines.append(f"station='{self.station}'")
        lines.append(f"latitude={self.latitude:.2f}")
        lines.append(f"longitude={self.longitude:.2f}")
        lines.append(f"elevation={self.elevation:.2f}")

        return f"TF( {(', ').join(lines)} )"

    def __eq__(self, other):
        is_equal = True
        if not isinstance(other, TF):
            self.logger.info(f"Comparing object is not TF, type {type(other)}")
            is_equal = False
        if self.station_metadata != other.station_metadata:
            self.logger.info("Station metadata is not equal")
            is_equal = False
        if self.survey_metadata != other.survey_metadata:
            self.logger.info("Survey Metadata is not equal")
            is_equal = False
        if self.has_transfer_function() and other.has_transfer_function():
            if not self.transfer_function.equals(other.transfer_function):
                self.logger.info("TF is not equal")
                is_equal = False
        elif (
            not self.has_transfer_function()
            and not other.has_transfer_function()
        ):
            pass
        else:
            self.logger.info("TF is not equal")
            is_equal = False

        return is_equal

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in ["logger"]:
                continue

            setattr(result, k, deepcopy(v, memo))
        return result

    def copy(self):
        return deepcopy(self)

    def _add_channels(
        self, run_metadata, default=["ex", "ey", "hx", "hy", "hz"]
    ):
        """
        add channels to a run

        """
        for ch in [cc for cc in default if cc.startswith("e")]:
            run_metadata.add_channel(Electric(component=ch))
        for ch in [cc for cc in default if cc.startswith("h")]:
            run_metadata.add_channel(Magnetic(component=ch))

        return run_metadata

    def _initialize_metadata(self):
        """
        Create a single `Survey` object to store all metadata

        :param channel_type: DESCRIPTION
        :type channel_type: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        survey_metadata = Survey(id="0")
        survey_metadata.stations.append(Station(id="0"))
        survey_metadata.stations[0].runs.append(Run(id="0"))

        self._add_channels(survey_metadata.stations[0].runs[0])

        return survey_metadata

    def _validate_run_metadata(self, run_metadata):
        """
        validate run metadata

        """

        if not isinstance(run_metadata, Run):
            if isinstance(run_metadata, dict):
                if "run" not in [cc.lower() for cc in run_metadata.keys()]:
                    run_metadata = {"Run": run_metadata}
                r_metadata = Run()
                r_metadata.from_dict(run_metadata)
                self.logger.debug("Loading from metadata dict")
                return r_metadata
            else:
                msg = (
                    f"input metadata must be type {type(self.run_metadata)} "
                    f"or dict, not {type(run_metadata)}"
                )
                self.logger.error(msg)
                raise TypeError(msg)
        return run_metadata.copy()

    def _validate_station_metadata(self, station_metadata):
        """
        validate station metadata
        """

        if not isinstance(station_metadata, Station):
            if isinstance(station_metadata, dict):
                if "station" not in [
                    cc.lower() for cc in station_metadata.keys()
                ]:
                    station_metadata = {"Station": station_metadata}
                st_metadata = Station()
                st_metadata.from_dict(station_metadata)
                self.logger.debug("Loading from metadata dict")
                return st_metadata
            else:
                msg = (
                    f"input metadata must be type {type(self.station_metadata)}"
                    f" or dict, not {type(station_metadata)}"
                )
                self.logger.error(msg)
                raise TypeError(msg)
        return station_metadata.copy()

    def _validate_survey_metadata(self, survey_metadata):
        """
        validate station metadata
        """

        if not isinstance(survey_metadata, Survey):
            if isinstance(survey_metadata, TSSurvey):
                sm = Survey()
                sm.from_dict(survey_metadata.to_dict())
                sm.stations = survey_metadata.stations
                survey_metadata = sm

            elif isinstance(survey_metadata, dict):
                if "survey" not in [
                    cc.lower() for cc in survey_metadata.keys()
                ]:
                    survey_metadata = {"Survey": survey_metadata}
                sv_metadata = Survey()
                sv_metadata.from_dict(survey_metadata)
                self.logger.debug("Loading from metadata dict")
                return sv_metadata
            else:
                msg = (
                    f"input metadata must be type {type(self.survey_metadata)}"
                    f" or dict, not {type(survey_metadata)}"
                )
                self.logger.error(msg)
                raise TypeError(msg)
        return survey_metadata.copy()

    ### Properties ------------------------------------------------------------
    @property
    def survey_metadata(self):
        """
        survey metadata
        """
        return self._survey_metadata

    @survey_metadata.setter
    def survey_metadata(self, survey_metadata):
        """

        :param survey_metadata: survey metadata object or dictionary
        :type survey_metadata: :class:`mt_metadata.timeseries.Survey` or dict

        """

        if survey_metadata is not None:
            survey_metadata = self._validate_survey_metadata(survey_metadata)
            self._survey_metadata.update(survey_metadata)
            for station in survey_metadata.stations:
                station.update_time_period()
                self._survey_metadata.add_station(station)

            if len(self._survey_metadata.stations.keys()) > 1:
                if "0" in self._survey_metadata.stations.keys():
                    self._survey_metadata.stations.remove("0")

            self._survey_metadata.update_time_period()

    @property
    def station_metadata(self):
        """
        station metadata
        """

        return self.survey_metadata.stations[0]

    @station_metadata.setter
    def station_metadata(self, station_metadata):
        """
        set station metadata from a valid input
        """

        if station_metadata is not None:
            station_metadata = self._validate_station_metadata(station_metadata)

            runs = ListDict()
            if self.run_metadata.id not in ["0", 0, None]:
                runs.append(self.run_metadata.copy())
            runs.extend(station_metadata.runs)
            if len(runs) == 0:
                runs[0] = Run(id="0")
            # be sure there is a level below
            if len(runs[0].channels) == 0:
                self._add_channels(runs[0])
            stations = ListDict()
            stations.append(station_metadata)
            stations[0].runs = runs
            stations[0].update_time_period()

            self.survey_metadata.stations = stations
            self._survey_metadata.update_time_period()

    @property
    def run_metadata(self):
        """
        station metadata
        """

        return self.survey_metadata.stations[0].runs[0]

    @run_metadata.setter
    def run_metadata(self, run_metadata):
        """
        set run metadata from a valid input
        """

        # need to make sure the first index is the desired channel
        if run_metadata is not None:
            run_metadata = self._validate_run_metadata(run_metadata)

            runs = ListDict()
            runs.append(run_metadata)
            channels = ListDict()
            if self.component is not None:
                key = str(self.component)

                channels.append(self.station_metadata.runs[0].channels[key])
                # add existing channels
                channels.extend(
                    self.run_metadata.channels, skip_keys=[key, "0"]
                )
            # add channels from input metadata
            channels.extend(run_metadata.channels)

            runs[0].channels = channels
            runs.extend(
                self.station_metadata.runs, skip_keys=[run_metadata.id, "0"]
            )

            self._survey_metadata.stations[0].runs = runs

    def _initialize_transfer_function(self, periods=[1]):
        """
        create an empty x array for the data.  For now this accommodates
        a single processed station.


        :return: DESCRIPTION
        :rtype: TYPE

        """
        # create an empty array for the transfer function
        tf = xr.DataArray(
            data=0.0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
            name="transfer_function",
        )

        tf_err = xr.DataArray(
            data=0.0,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
            name="transfer_function_error",
        )

        tf_model_err = xr.DataArray(
            data=0.0,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
            name="transfer_function_model_error",
        )

        inv_signal_power = xr.DataArray(
            data=0.0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
            name="inverse_signal_power",
        )

        residual_covariance = xr.DataArray(
            data=0.0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
            name="residual_covariance",
        )

        # will need to add in covariance in some fashion
        return xr.Dataset(
            {
                tf.name: tf,
                tf_err.name: tf_err,
                tf_model_err.name: tf_model_err,
                inv_signal_power.name: inv_signal_power,
                residual_covariance.name: residual_covariance,
            },
            coords={
                "period": periods,
                "output": self._ch_output_dict["all"],
                "input": self._ch_input_dict["all"],
            },
        )

    # ==========================================================================
    # Properties
    # ==========================================================================
    @property
    def channel_nomenclature(self):
        return self._channel_nomenclature

    @channel_nomenclature.setter
    def channel_nomenclature(self, ch_dict):
        """
        channel dictionary
        """

        if not isinstance(ch_dict, dict):
            raise TypeError(
                "Channel_nomenclature must be a dictionary with keys "
                "['ex', 'ey', 'hx', 'hy', 'hz']."
            )

        self._channel_nomenclature = ch_dict
        # unpack channel nomenclature dict
        self.ex = self._channel_nomenclature["ex"]
        self.ey = self._channel_nomenclature["ey"]
        self.hx = self._channel_nomenclature["hx"]
        self.hy = self._channel_nomenclature["hy"]
        self.hz = self._channel_nomenclature["hz"]
        self.ex_ey = [self.ex, self.ey]
        self.hx_hy = [self.hx, self.hy]
        self.ex_ey_hz = [self.ex, self.ey, self.hz]

    @property
    def _ch_input_dict(self):
        return {
            "impedance": self.hx_hy,
            "tipper": self.hx_hy,
            "impedance_error": self.hx_hy,
            "impedance_model_error": self.hx_hy,
            "tipper_error": self.hx_hy,
            "tipper_model_error": self.hx_hy,
            "isp": self.hx_hy,
            "res": self.ex_ey_hz,
            "tf": self.hx_hy,
            "tf_error": self.hx_hy,
            "all": [self.ex, self.ey, self.hz, self.hx, self.hy],
        }

    @property
    def _ch_output_dict(self):
        return {
            "impedance": self.ex_ey,
            "tipper": [self.hz],
            "impedance_error": self.ex_ey,
            "impedance_model_error": self.ex_ey,
            "tipper_error": [self.hz],
            "tipper_model_error": [self.hz],
            "isp": self.hx_hy,
            "res": self.ex_ey_hz,
            "tf": self.ex_ey_hz,
            "tf_error": self.ex_ey_hz,
            "all": [self.ex, self.ey, self.hz, self.hx, self.hy],
        }

    @property
    def index_zxx(self):
        return {"input": self.hx, "output": self.ex}

    @property
    def index_zxy(self):
        return {"input": self.hy, "output": self.ex}

    @property
    def index_zyx(self):
        return {"input": self.hx, "output": self.ey}

    @property
    def index_zyy(self):
        return {"input": self.hy, "output": self.ey}

    @property
    def index_tzx(self):
        return {"input": self.hx, "output": self.hz}

    @property
    def index_tzy(self):
        return {"input": self.hy, "output": self.hz}

    @property
    def fn(self):
        """reference to original data file"""
        return self._fn

    @fn.setter
    def fn(self, value):
        """set file name"""
        if value is None:
            self._fn = None
            return
        self._fn = Path(value)
        self.save_dir = self._fn.parent

    @property
    def latitude(self):
        """Latitude"""
        return self.station_metadata.location.latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        set latitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.latitude = latitude

    @property
    def longitude(self):
        """Longitude"""
        return self.station_metadata.location.longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        set longitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.longitude = longitude

    @property
    def elevation(self):
        """Elevation"""
        return self.station_metadata.location.elevation

    @elevation.setter
    def elevation(self, elevation):
        """
        set elevation, should be input as meters
        """

        self.station_metadata.location.elevation = elevation

    @property
    def dataset(self):
        """
        This will return an xarray dataset with proper metadata

        :return: DESCRIPTION
        :rtype: TYPE

        """

        for key, mkey in self._dataset_attr_dict.items():
            obj, attr = mkey.split(".", 1)
            value = getattr(self, obj).get_attr_from_name(attr)

            self._transfer_function.attrs[key] = value
        return self._transfer_function

    def _validate_input_ndarray(self, ndarray, atype="impedance"):
        """
        Validate the input based on array type and component
        :param atype: DESCRIPTION, defaults to "impedance"
        :type atype: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        shape_dict = {
            "impedance": (2, 2),
            "tipper": (1, 2),
            "impedance_error": (2, 2),
            "impedance_model_error": (2, 2),
            "tipper_error": (1, 2),
            "tipper_model_error": (1, 2),
            "isp": (2, 2),
            "res": (3, 3),
            "transfer_function": (3, 2),
            "transfer_function_error": (3, 2),
            "tf": (3, 2),
            "tf_error": (3, 2),
        }

        shape = shape_dict[atype]
        if ndarray.shape[1:] != shape:
            msg = (
                f"{atype} must be have shape (n_periods, {shape[0]}, "
                f"{shape[1]}), not {ndarray.shape}"
            )
            self.logger.error(msg)
            raise TFError(msg)
        if ndarray.shape[0] != self.period.size:
            msg = (
                f"New {atype} shape {ndarray.shape} not same as old {shape}, "
                "suggest creating a new instance."
            )
            self.logger.error(msg)
            raise TFError(msg)

    def _validate_input_dataarray(self, da, atype="impedance"):
        """
        Validate an input data array

        :param da: DESCRIPTION
        :type da: TYPE
        :param atype: DESCRIPTION, defaults to "impedance"
        :type atype: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        ch_in = self._ch_input_dict[atype]
        ch_out = self._ch_output_dict[atype]

        # should test for shape
        if "period" not in da.coords.keys() or "input" not in da.coords.keys():
            msg = f"Coordinates must be period, output, input, not {list(da.coords.keys())}"
            self.logger.error(
                msg,
            )
            raise TFError(msg)
        if sorted(ch_out) != sorted(da.coords["output"].data.tolist()):
            msg = (
                f"Output dimensions must be {ch_out} not "
                f"{da.coords['output'].data.tolist()}"
            )
            self.logger.error(msg)
            raise TFError(msg)
        if sorted(ch_in) != sorted(da.coords["input"].data.tolist()):
            msg = (
                f"Input dimensions must be {ch_in} not "
                f"{da.coords['input'].data.tolist()}"
            )
            self.logger.error(msg)
            raise TFError(msg)
        # need to reorder the data array to the expected coordinates
        da = da.reindex(output=ch_out, input=ch_in)
        # if this is the first instantiation then just resize the
        # transfer function to fit the input
        if (
            self._transfer_function.transfer_function.data.shape[0] == 1
            and not self.has_tipper()
            and not self.has_impedance()
        ):
            self._transfer_function = self._initialize_transfer_function(
                da.period
            )
            return da
        elif (
            self._transfer_function.transfer_function.data.shape[0]
            == da.data.shape[0]
        ):
            return da
        else:
            msg = "Reassigning with a different shape is dangerous.  Should re-initialize transfer_function or make a new instance of TF"
            self.logger.error(msg)
            raise TFError(msg)

    def _set_data_array(self, value, atype):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :param atype: DESCRIPTION
        :type atype: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if value is None:
            return
        key_dict = {
            "tf": "transfer_function",
            "impedance": "transfer_function",
            "tipper": "transfer_function",
            "isp": "inverse_signal_power",
            "res": "residual_covariance",
            "transfer_function": "transfer_function",
            "impedance_error": "transfer_function_error",
            "impedance_model_error": "transfer_function_model_error",
            "tipper_error": "transfer_function_error",
            "tipper_model_error": "transfer_function_model_error",
            "tf_error": "transfer_function_error",
            "tf_model_error": "transfer_function_model_error",
            "transfer_function_error": "transfer_function_error",
            "transfer_function_model_error": "transfer_function_model_error",
        }
        key = key_dict[atype]
        ch_in = self._ch_input_dict[atype]
        ch_out = self._ch_output_dict[atype]
        comps = dict(input=ch_in, output=ch_out)

        if isinstance(value, (list, tuple, np.ndarray)):
            value = np.array(value)
            self._validate_input_ndarray(value, atype=atype)

            self._transfer_function[key].loc[comps] = value
        elif isinstance(value, xr.DataArray):
            nda = self._validate_input_dataarray(value, atype=atype)

            self._transfer_function[key].loc[comps] = nda
        else:
            msg = (
                f"Data type {type(value)} not supported use a numpy "
                "array or xarray.DataArray"
            )
            self.logger.error(msg)
            raise TFError(msg)

    def has_transfer_function(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.ex in outputs or self.ey in outputs or self.hz in outputs:
            if np.all(
                self._transfer_function.transfer_function.sel(
                    input=self._ch_input_dict["tf"],
                    output=self._ch_output_dict["tf"],
                ).data
                == 0
            ):
                return False
            return True
        return False

    @property
    def transfer_function(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function.setter
    def transfer_function(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf")

    @property
    def transfer_function_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function_error.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function_error.setter
    def transfer_function_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf_error")

    @property
    def transfer_function_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function_model_error.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function_model_error.setter
    def transfer_function_model_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf_model_error")

    def has_impedance(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.ex in outputs or self.ey in outputs:
            if np.all(
                self._transfer_function.transfer_function.sel(
                    input=self._ch_input_dict["impedance"],
                    output=self._ch_output_dict["impedance"],
                ).data
                == 0
            ):
                return False
            return True
        return False

    @property
    def impedance(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z = self.dataset.transfer_function.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z.name = "impedance"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z.attrs[key] = value
            return z

    @impedance.setter
    def impedance(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance")

    @property
    def impedance_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z_err = self.dataset.transfer_function_error.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z_err.name = "impedance_error"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z_err.attrs[key] = value
            return z_err

    @impedance_error.setter
    def impedance_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance_error")

    @property
    def impedance_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z_err = self.dataset.transfer_function_model_error.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z_err.name = "impedance_model_error"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z_err.attrs[key] = value
            return z_err

    @impedance_model_error.setter
    def impedance_model_error(self, value):
        """
        Set the impedance model errors from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance_model_error")

    def has_tipper(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.hz in outputs:
            if np.all(
                np.nan_to_num(
                    self._transfer_function.transfer_function.sel(
                        input=self._ch_input_dict["tipper"],
                        output=self._ch_output_dict["tipper"],
                    ).data
                )
                == 0
            ):
                return False
            return True
        return False

    @property
    def tipper(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper.setter
    def tipper(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper")

    @property
    def tipper_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function_error.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper_error"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper_error.setter
    def tipper_error(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper_error")

    @property
    def tipper_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function_model_error.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper_model_error"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper_model_error.setter
    def tipper_model_error(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper_model_error")

    def has_inverse_signal_power(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """

        if np.all(
            self._transfer_function.inverse_signal_power.sel(
                input=self._ch_input_dict["isp"],
                output=self._ch_output_dict["isp"],
            ).data
            == 0
        ):
            return False
        return True

    @property
    def inverse_signal_power(self):
        if self.has_inverse_signal_power():
            ds = self.dataset.inverse_signal_power.sel(
                input=self._ch_input_dict["isp"],
                output=self._ch_output_dict["isp"],
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds
        return None

    @inverse_signal_power.setter
    def inverse_signal_power(self, value):
        """
        Set the inverse signal power


        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "isp")
        if self.has_residual_covariance():
            self._compute_error_from_covariance()

    def has_residual_covariance(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """

        if np.all(
            self._transfer_function.residual_covariance.sel(
                input=self._ch_input_dict["res"],
                output=self._ch_output_dict["res"],
            ).data
            == 0
        ):
            return False
        return True

    @property
    def residual_covariance(self):
        if self.has_residual_covariance():
            ds = self.dataset.residual_covariance.sel(
                input=self._ch_input_dict["res"],
                output=self._ch_output_dict["res"],
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds
        return None

    @residual_covariance.setter
    def residual_covariance(self, value):
        """
        Set the residual covariance

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "res")
        if self.has_inverse_signal_power():
            self._compute_error_from_covariance()

    def _compute_impedance_error_from_covariance(self):
        """
        Compute transfer function errors from covariance matrices

        This will become important when writing edi files.

        Translated from code written by Ben Murphy.

        :return: DESCRIPTION
        :rtype: TYPE

        """
        sigma_e = self.residual_covariance.loc[
            dict(input=self.ex_ey, output=self.ex_ey)
        ]
        sigma_s = self.inverse_signal_power.loc[
            dict(input=self.hx_hy, output=self.hx_hy)
        ]

        z_err = np.zeros((self.period.size, 2, 2), dtype=float)
        z_err[:, 0, 0] = np.abs(
            sigma_e.loc[dict(input=[self.ex], output=[self.ex])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        z_err[:, 0, 1] = np.abs(
            sigma_e.loc[dict(input=[self.ex], output=[self.ex])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )
        z_err[:, 1, 0] = np.abs(
            sigma_e.loc[dict(input=[self.ey], output=[self.ey])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        z_err[:, 1, 1] = np.abs(
            sigma_e.loc[dict(input=[self.ey], output=[self.ey])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )

        z_err = np.sqrt(np.abs(z_err))

        self.dataset.transfer_function_error.loc[
            dict(input=self.hx_hy, output=self.ex_ey)
        ] = z_err

    def _compute_tipper_error_from_covariance(self):
        """
        Compute transfer function errors from covariance matrices

        This will become important when writing edi files.

        Translated from code written by Ben Murphy.

        :return: DESCRIPTION
        :rtype: TYPE

        """
        sigma_e = self.residual_covariance.loc[
            dict(input=[self.hz], output=[self.hz])
        ]
        sigma_s = self.inverse_signal_power.loc[
            dict(input=self.hx_hy, output=self.hx_hy)
        ]

        t_err = np.zeros((self.period.size, 1, 2), dtype=float)
        t_err[:, 0, 0] = np.abs(
            sigma_e.loc[dict(input=[self.hz], output=[self.hz])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        t_err[:, 0, 1] = np.abs(
            sigma_e.loc[dict(input=[self.hz], output=[self.hz])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )

        t_err = np.sqrt(np.abs(t_err))

        self.dataset.transfer_function_error.loc[
            dict(input=self.hx_hy, output=[self.hz])
        ] = t_err

    def _compute_error_from_covariance(self):
        """
        convenience method to compute errors from covariance

        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._compute_impedance_error_from_covariance()
        self._compute_tipper_error_from_covariance()

    @property
    def period(self):
        return self.dataset.period.data

    @period.setter
    def period(self, value):
        if self.period is not None:
            if len(self.period) == 1 and (self.period == np.array([1])).all():
                self._transfer_function = self._initialize_transfer_function(
                    periods=value
                )
            elif len(value) != len(self.period):
                msg = (
                    f"New period size {value.size} is not the same size as "
                    f"old ones {self.period.size}, suggest creating a new "
                    "instance of TF."
                )
                self.logger.error(msg)
                raise TFError(msg)
            elif not (self.period == value).all():
                self.dataset["period"] = value
        else:
            self._transfer_function = self._initialize_transfer_function(
                periods=value
            )
        return

    @property
    def frequency(self):
        if self.period is not None:
            return 1.0 / self.period
        return None

    @frequency.setter
    def frequency(self, value):
        self.period = 1.0 / value

    @property
    def station(self):
        """station name"""
        return self.station_metadata.id

    @station.setter
    def station(self, station_name):
        """
        set station name
        """
        self.station_metadata.id = validate_name(station_name)
        if self.station_metadata.runs[0].id is None:
            r = self.station_metadata.runs[0].copy()
            r.id = f"{self.station_metadata.id}a"
            self.station_metadata.runs.remove(None)
            self.station_metadata.runs.append(r)

    @property
    def survey(self):
        """
        Survey ID
        """
        return self.survey_metadata.id

    @survey.setter
    def survey(self, survey_id):
        """
        set survey id
        """
        if survey_id is None:
            survey_id = "unkown_survey"
        self.survey_metadata.id = validate_name(survey_id)

    @property
    def tf_id(self):
        """transfer function id"""
        return self.station_metadata.transfer_function.id

    @tf_id.setter
    def tf_id(self, value):
        """set transfer function id"""
        self.station_metadata.transfer_function.id = validate_name(value)

    def to_ts_station_metadata(self):
        """
        need a convinience function to translate to ts station metadata
        for MTH5

        """

        from mt_metadata.timeseries import Station as TSStation

        ts_station_metadata = TSStation()
        for key, value in self.station_metadata.to_dict(single=True).items():
            if "transfer_function" in key:
                continue
            try:
                ts_station_metadata.set_attr_from_name(key, value)
            except AttributeError:
                self.logger.debug(f"Attribute {key} could not be set.")
        return ts_station_metadata

    def from_ts_station_metadata(self, ts_station_metadata):
        """
        need a convinience function to translate to ts station metadata
        for MTH5

        """

        for key, value in ts_station_metadata.to_dict(single=True).items():
            try:
                self.station_metadata.set_attr_from_name(key, value)
            except AttributeError:
                continue

    def merge(self, other, period_min=None, period_max=None, inplace=False):
        """
        metadata will be assumed to be from self.

        Merge transfer functions together. `other` can be another `TF` object
        or a tuple of `TF` objects

        to set bounds should be of the format

        [{"tf": tf_01, "period_min": .01, "period_max": 100},
         {"tf": tf_02, "period_min": 100, "period_max": 1000}]

        or to just use whats in the transfer function
        [tf_01, tf_02, ...]

        The bounds are inclusive, so if you want to merge at say 1 s choose
        the best one and set the other to a value lower or higher depending
        on the periods for that transfer function, for example

        [{"tf": tf_01, "period_min": .01, "period_max": 100},
         {"tf": tf_02, "period_min": 100.1, "period_max": 1000}]

        :param other: other transfer functions to merge with
        :type other: TF, list of dicts, list of TF objects, dict
        :param period_min: minimum period for the original TF
        :type period_min: float
        :param period_max: maximum period for the original TF
        :type period_max: float
        :return: merged TF object with metadata equal to the original
         (if inplace=False)
        :rtype: TF

        """

        def get_slice_dict(period_min, period_max):
            """
            Get an the correct dictionary for slicing an xarray.

            :param period_min: minimum period
            :type period_min: float
            :param period_max: maximum period
            :type period_max: float
            :return: variable to slice an xarray
            :rtype: dict

            """
            return {"period": slice(period_min, period_max)}

        def sort_by_period(tf):
            """
            period needs to be monotonically increasing for slice to work.
            """
            return tf.sortby("period")

        def is_tf(item):
            """
            If the item is a transfer function return it sorted by period

            :param item: transfer function
            :type item: :class:`mt_metadata.transfer_function.core.TF`
            :return: sorted by period transfer function
            :rtype: xarray.Dataset

            """
            return sort_by_period(item._transfer_function)

        def validate_dict(item):
            """
            Make sure input dictionary has proper keys.

            - **tf** :class:`mt_metadata.transfer_function.core.TF`
            - **period_min** minumum period (s)
            - **period_max** maximum period (s)

            :param item: dictionary to slice a transfer function
            :type item: dict
            :raises KeyError: If keys are not what they should be
            :return: validated dictionary
            :rtype: dict

            """
            accepted_keys = sorted(["tf", "period_min", "period_max"])

            if accepted_keys != sorted(list(item.keys())):
                msg = f"Input dictionary must have keys of {accepted_keys}"
                self.logger.error(msg)
                raise KeyError(msg)
            return item

        def is_dict(item):
            """
            If the item is a dictionary then be sure to sort the transfer
            function and then apply the slice.

            :param item: dictionary with keys 'tf', 'period_min', 'period_max'
            :type item: dict
            :return: sliced transfer function
            :rtype: xarray.Dataset

            """
            item = validate_dict(item)
            period_slice = get_slice_dict(
                item["period_min"], item["period_max"]
            )
            item["tf"]._transfer_function = sort_by_period(
                item["tf"]._transfer_function
            )
            return get_slice(item["tf"], period_slice)

        def get_slice(tf, period_slice):
            """
            get slice of a transfer function most of the time we can use .loc
            but sometimes a key error occurs if the period index is not
            monotonic (which is should be now after using .sortby('period')),
            but leaving in place just in case.  If .loc does not work, then
            we can use .where(conditions) to slice the transfer function.
            """
            try:
                return tf._transfer_function.loc[period_slice]

            except KeyError:
                if (
                    period_slice["period"].start is not None
                    and period_slice["period"].stop is not None
                ):
                    return tf._transfer_function.where(
                        (
                            tf._transfer_function.period
                            >= period_slice["period"].start
                        )
                        & (
                            tf._transfer_function.period
                            <= period_slice["period"].stop
                        ),
                        drop=True,
                    )
                elif (
                    period_slice["period"].start is None
                    and period_slice["period"].stop is not None
                ):
                    return tf._transfer_function.where(
                        (
                            tf._transfer_function.period
                            <= period_slice["period"].stop
                        ),
                        drop=True,
                    )
                elif (
                    period_slice["period"].start is not None
                    and period_slice["period"].stop is None
                ):
                    return tf._transfer_function.where(
                        (
                            tf._transfer_function.period
                            >= period_slice["period"].start
                        ),
                        drop=True,
                    )

        period_slice_self = get_slice_dict(period_min, period_max)
        tf_list = [get_slice(self, period_slice_self)]
        if not isinstance(other, list):
            other = [other]

        for item in other:
            if isinstance(item, TF):
                tf_list.append(is_tf(item))
            elif isinstance(item, dict):
                tf_list.append(is_dict(item))
            else:
                msg = f"Type {type(item)} not supported"
                self.logger.error(msg)
                raise TypeError(msg)

        new_tf = xr.combine_by_coords(tf_list, combine_attrs="override")

        if inplace:
            self._transfer_function = new_tf
        else:
            return_tf = self.copy()
            return_tf._transfer_function = new_tf
            return return_tf

    def write(
        self,
        fn=None,
        save_dir=None,
        fn_basename=None,
        file_type="edi",
        **kwargs,
    ):
        """
        Write an mt file, the supported file types are EDI and XML.

        .. todo:: j-files and avg files

        :param fn: full path to file to save to
        :type fn: :class:`pathlib.Path` or string

        :param save_dir: full path save directory
        :type save_dir: string

        :param fn_basename: name of file with or without extension
        :type fn_basename: string

        :param file_type: [ 'edi' | 'xml' | "zmm" ]
        :type file_type: string

        keyword arguments include

        :param longitude_format:  whether to write longitude as longitude or LONG.
                                  options are 'longitude' or 'LONG', default 'longitude'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns: full path to file
        :rtype: string

        :Example: ::

            >>> tf_obj.write(file_type='xml')

        """

        if fn is not None:
            new_fn = Path(fn)
            self.save_dir = new_fn.parent
            fn_basename = new_fn.name
            file_type = new_fn.suffix.lower()[1:]
        if save_dir is not None:
            self.save_dir = Path(save_dir)
        if fn_basename is not None:
            fn_basename = Path(fn_basename)
            if fn_basename.suffix in ["", None]:
                fn_basename = fn_basename.with_name(
                    f"{fn_basename.name}.{file_type}"
                )
        if fn_basename is None:
            fn_basename = Path(f"{self.station}.{file_type}")
        if file_type is None:
            file_type = fn_basename.suffix.lower()[1:]
        if file_type not in self._read_write_dict.keys():
            msg = f"File type {file_type} not supported yet."
            self.logger.error(msg)
            raise TFError(msg)
        fn = self.save_dir.joinpath(fn_basename)

        obj = self._read_write_dict[file_type]["write"]()
        obj._fn = fn
        obj.write(fn, **kwargs)

        return obj

    def write_tf_file(self, **kwargs):
        self.logger.error("'write_tf_file' has been deprecated use 'write()'")

    def read_tf_file(self, **kwargs):
        self.logger.error("'read_tf_file' has been deprecated use 'read()'")

    def read(self, fn=None, file_type=None, get_elevation=False, **kwargs):
        """

        Read an TF response file.

        .. note:: Currently only .edi, .xml, .j, .zmm/rr/ss, .avg
           files are supported



        :param fn: full path to input file
        :type fn: string

        :param file_type: ['edi' | 'j' | 'xml' | 'avg' | 'zmm' | 'zrr' | 'zss' | ... ]
                          if None, automatically detects file type by
                          the extension.
        :type file_type: string
        :param get_elevation: Get elevation from US National Map DEM
        :type get_elevation: bool

        :Example: ::

            >>> import mt_metadata.transfer_functions import TF
            >>> tf_obj = TF()
            >>> tf_obj.read(fn=r"/home/mt/mt01.xml")

        .. note:: If your internet is slow try setting 'get_elevation' = False,
         It can get hooked in a slow loop and slow down reading.

        """
        if fn is not None:
            self.fn = fn
        self.save_dir = self.fn.parent
        if file_type is None:
            file_type = self.fn.suffix.lower()[1:]
        self._read_write_dict[file_type]["read"](
            self.fn, get_elevation=get_elevation, **kwargs
        )

        self.station_metadata.update_time_period()
        self.survey_metadata.update_bounding_box()
        self.survey_metadata.update_time_period()

    def to_edi(self):
        """

        Convert the TF object to a
        :class:`mt_metadata.transfer_functions.io.edi.EDI` object.  From there
        attributes of an EDI object can be manipulated previous to writing
        to a file.

        :return: EDI object
        :rtype: :class:`mt_metadata.transfer_functions.io.edi.EDI`

        >>> from mt_metadata.transfer_functions import TF
        >>> from mt_metadata import TF_XML
        >>> t = TF(TF_XML)
        >>> t.read()
        >>> edi_object = t.to_edi()
        >>> edi_object.Header.acqby = "me"
        >>> edi_object.write()

        """

        edi_obj = EDI()
        if self.has_impedance():
            edi_obj.z = self.impedance.data
            edi_obj.z_err = self.impedance_error.data
        if self.has_tipper():
            edi_obj.t = self.tipper.data
            edi_obj.t_err = self.tipper_error.data
        edi_obj.frequency = 1.0 / self.period
        edi_obj.rotation_angle = np.repeat(
            self._rotation_angle, self.period.size
        )

        # fill from survey metadata
        edi_obj.survey_metadata = self.survey_metadata

        # fill from station metadata
        edi_obj.station_metadata = self.station_metadata

        edi_obj.Info.read_info(edi_obj.Info.write_info())

        # input data section
        edi_obj.Data.data_type = self.station_metadata.data_type
        edi_obj.Data.nfreq = self.period.size
        edi_obj.Data.sectid = self.station
        edi_obj.Data.nchan = len(edi_obj.Measurement.channel_ids.keys())
        edi_obj.Data.maxblks = 999

        for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
            if hasattr(edi_obj.Measurement, f"meas_{comp}"):
                setattr(
                    edi_obj.Data,
                    comp,
                    getattr(edi_obj.Measurement, f"meas_{comp}").id,
                )
        edi_obj.Data.read_data(edi_obj.Data.write_data())

        edi_obj.Measurement.read_measurement(
            edi_obj.Measurement.write_measurement()
        )

        return edi_obj

    def from_edi(self, edi_obj, get_elevation=False, **kwargs):
        """
        Read in an EDI file or a
        :class:`mt_metadata.transfer_functions.io.edi.EDI` ojbect

        :param edi_obj: path to edi file or EDI object
        :type edi_obj: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.edi.EDI`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Key word arguments for an EDI object
        :type kwargs: dictionary
        :raises TypeError: If input is incorrect

        """

        if isinstance(edi_obj, (str, Path)):
            self._fn = Path(edi_obj)
            edi_obj = EDI(**kwargs)
            edi_obj.read(self._fn, get_elevation=get_elevation)
        if not isinstance(edi_obj, EDI):
            raise TypeError(f"Input must be a EDI object not {type(edi_obj)}")
        if edi_obj.tf is not None and edi_obj.tf.shape[1:] == (3, 2):
            k_dict = OrderedDict(
                {
                    "period": "period",
                    "transfer_function": "tf",
                    "inverse_signal_power": "signal_inverse_power",
                    "residual_covariance": "residual_covariance",
                    "transfer_function_error": "tf_err",
                    "survey_metadata": "survey_metadata",
                    "station_metadata": "station_metadata",
                }
            )
        else:
            k_dict = OrderedDict(
                {
                    "period": "period",
                    "impedance": "z",
                    "impedance_error": "z_err",
                    "tipper": "t",
                    "tipper_error": "t_err",
                    "survey_metadata": "survey_metadata",
                    "station_metadata": "station_metadata",
                }
            )
        for tf_key, edi_key in k_dict.items():
            setattr(self, tf_key, getattr(edi_obj, edi_key))

    def to_emtfxml(self):
        """
        Convert TF to a :class:`mt_metadata.transfer_function.io.emtfxml.EMTFXML`
        object.

        :return: EMTFXML object
        :rtype: :class:`mt_metadata.transfer_function.io.emtfxml.EMTFXML`

        >>> from mt_metadata.transfer_functions import TF
        >>> from mt_metadata import TF_XML
        >>> t = TF(TF_XML)
        >>> t.read()
        >>> xml_object = t.to_emtfxml()
        >>> xml_object.site.country = "Here"
        >>> xml_object.write()

        """

        emtf = EMTFXML()
        emtf.survey_metadata = self.survey_metadata
        emtf.station_metadata = self.station_metadata

        if emtf.description is None:
            emtf.description = "Magnetotelluric Transfer Functions"
        if emtf.product_id is None:
            emtf.product_id = (
                f"{emtf.survey_metadata.project}."
                f"{emtf.station_metadata.id}."
                f"{emtf.station_metadata.time_period._start_dt.year}"
            )
        tags = []

        emtf.data.period = self.period

        if self.has_impedance():
            tags += ["impedance"]
            emtf.data.z = self.impedance.data
            emtf.data.z_var = self.impedance_error.data**2
        if self.has_residual_covariance() and self.has_inverse_signal_power():
            emtf.data.z_invsigcov = self.inverse_signal_power.loc[
                dict(input=self.hx_hy, output=self.hx_hy)
            ].data
            emtf.data.z_residcov = self.residual_covariance.loc[
                dict(input=self.ex_ey, output=self.ex_ey)
            ].data
        if self.has_tipper():
            tags += ["tipper"]
            emtf.data.t = self.tipper.data
            emtf.data.t_var = self.tipper_error.data**2
        if self.has_residual_covariance() and self.has_inverse_signal_power():
            emtf.data.t_invsigcov = self.inverse_signal_power.loc[
                dict(input=self.hx_hy, output=self.hx_hy)
            ].data
            emtf.data.t_residcov = self.residual_covariance.loc[
                dict(
                    input=[self.channel_nomenclature["hz"]],
                    output=[self.channel_nomenclature["hz"]],
                )
            ].data
        emtf.tags = ", ".join(tags)
        emtf.period_range.min = emtf.data.period.min()
        emtf.period_range.max = emtf.data.period.max()

        emtf._get_data_types()
        emtf._get_statistical_estimates()

        return emtf

    def from_emtfxml(self, emtfxml_obj, get_elevation=False, **kwargs):
        """

        :param emtfxml_object: path to emtf xml file or EMTFXML object
        :type emtfxml_object: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_function.io.emtfxml.EMTFXML`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for EMTFXML object
        :type kwargs: dictionary

        """

        if isinstance(emtfxml_obj, (str, Path)):
            self._fn = Path(emtfxml_obj)
            emtfxml_obj = EMTFXML(**kwargs)
            emtfxml_obj.read(self._fn, get_elevation=get_elevation)
        if not isinstance(emtfxml_obj, EMTFXML):
            raise TypeError(
                f"Input must be a EMTFXML object not {type(emtfxml_obj)}"
            )
        self.survey_metadata = emtfxml_obj.survey_metadata
        self.station_metadata = emtfxml_obj.station_metadata

        self.period = emtfxml_obj.data.period
        self.impedance = emtfxml_obj.data.z
        self.impedance_error = np.sqrt(emtfxml_obj.data.z_var)
        self._transfer_function.inverse_signal_power.loc[
            dict(input=["hx", "hy"], output=["hx", "hy"])
        ] = emtfxml_obj.data.z_invsigcov
        self._transfer_function.residual_covariance.loc[
            dict(input=["ex", "ey"], output=["ex", "ey"])
        ] = emtfxml_obj.data.z_residcov

        self.tipper = emtfxml_obj.data.t
        self.tipper_error = np.sqrt(emtfxml_obj.data.t_var)
        self._transfer_function.inverse_signal_power.loc[
            dict(input=["hx", "hy"], output=["hx", "hy"])
        ] = emtfxml_obj.data.t_invsigcov
        self._transfer_function.residual_covariance.loc[
            dict(input=["hz"], output=["hz"])
        ] = emtfxml_obj.data.t_residcov

    def to_jfile(self):
        """

        Translate TF object ot JFile object.

        .. note:: Not Implemented yet

        :return: JFile object
        :rtype: :class:`mt_metadata.transfer_functions.io.jfile.JFile`

        """

        raise IOError("to_jfile not implemented yet.")

    def from_jfile(self, j_obj, get_elevation=False, **kwargs):
        """

        :param jfile_obj: path ot .j file or JFile object
        :type jfile_obj: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.jfile.JFile`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for JFile object
        :type kwargs: dictionary

        """
        if isinstance(j_obj, (str, Path)):
            self._fn = Path(j_obj)
            j_obj = JFile(**kwargs)
            j_obj.read(self._fn, get_elevation=get_elevation)
        if not isinstance(j_obj, JFile):
            raise TypeError(f"Input must be a JFile object not {type(j_obj)}")
        k_dict = OrderedDict(
            {
                "period": "periods",
                "impedance": "z",
                "impedance_error": "z_err",
                "tipper": "t",
                "tipper_error": "t_err",
                "survey_metadata": "survey_metadata",
                "station_metadata": "station_metadata",
            }
        )

        for tf_key, j_key in k_dict.items():
            setattr(self, tf_key, getattr(j_obj, j_key))

    def make_zmm_run(self, zmm_obj, number_dict):
        """
        Helper function to provide a run for a zmm object to aid writing z-file

        Parameters
        ----------
        :param zmm_obj: a ZMM that will be written to file, that needs a run associated
        :type zmm_obj:  :class: `mt_metadata.transfer_functions.io.zfiles.zmm.ZMM`
        :param number_dict: mapping between hexy keys and integers, needed for emtf
        z-files, e.g. {"hx": 1, "hy": 2, "hz": 3, "ex": 4, "ey": 5}
        :type number_dict: dictionary

        :return: run
        :rtype: :class:` mt_metadata.timeseries.run.Run`
        """
        run = Run()
        for ch, ch_num in number_dict.items():
            c = ZChannel()
            c.channel = ch
            c.number = ch_num
            setattr(zmm_obj, c.channel, c)
            if ch in ["ex", "ey"]:
                rc = Electric(component=ch, channel_number=ch_num)
                run.add_channel(rc)
            elif ch in ["hx", "hy", "hz"]:
                rc = Magnetic(component=ch, channel_number=ch_num)
                run.add_channel(rc)
        return run

    def to_zmm(self):
        """

        Translate TF object to ZMM object.

        :return: ZMM object
        :rtype: :class:`mt_metadata.transfer_function.io.zfiles.ZMM`

        >>> from mt_metadata.transfer_functions import TF
        >>> from mt_metadata import TF_XML
        >>> t = TF(TF_XML)
        >>> t.read()
        >>> zmm_object = t.to_zmm()
        >>> zmm_object.processing_type = "new and fancy"
        >>> zmm_object.write()

        """
        zmm_kwargs = {}
        zmm_kwargs["channel_nomenclature"] = self.channel_nomenclature
        zmm_kwargs[
            "inverse_channel_nomenclature"
        ] = self.inverse_channel_nomenclature
        if hasattr(self, "decimation_dict"):
            zmm_kwargs["decimation_dict"] = self.decimation_dict
        zmm_obj = ZMM(**zmm_kwargs)

        zmm_obj.dataset = self.dataset
        zmm_obj.station_metadata = self.station_metadata

        # need to set the channel numbers according to the z-file format
        # with input channels (h's) and output channels (hz, e's).
        if self.has_tipper():
            if self.has_impedance():
                zmm_obj.num_channels = 5
                number_dict = {"hx": 1, "hy": 2, "hz": 3, "ex": 4, "ey": 5}
            else:
                zmm_obj.num_channels = 3
                number_dict = {"hx": 1, "hy": 2, "hz": 3}
        else:
            if self.has_impedance():
                zmm_obj.num_channels = 4
                number_dict = {"hx": 1, "hy": 2, "ex": 3, "ey": 4}
        if len(self.station_metadata.runs) == 0:
            run = self.make_zmm_run(zmm_obj, number_dict)
            self.station_metadata.add_run(run)
        elif len(self.station_metadata.runs[0].channels_recorded_all) == 0:
            # avoid the default metadata getting interpretted as a real metadata object
            # Overwrite this "spoof" run with a run that has recorded channels
            if len(self.station_metadata.runs[0].channels_recorded_all) == 0:
                run = self.make_zmm_run(zmm_obj, number_dict)
                self.station_metadata.runs[0] = run
        else:
            for comp in self.station_metadata.runs[0].channels_recorded_all:
                if "rr" in comp:
                    continue
                ch = self.station_metadata.runs[0].get_channel(comp)
                ch.component = self.inverse_channel_nomenclature[comp]
                c = ZChannel()
                c.from_dict(ch.to_dict(single=True))
                ch.component = comp
                try:
                    c.number = number_dict[c.channel]
                    setattr(zmm_obj, c.channel, c)
                except KeyError:
                    self.logger.debug(f"Could not find channel {c.channel}")
        zmm_obj.survey_metadata.update(self.survey_metadata)
        zmm_obj.num_freq = self.period.size

        return zmm_obj

    def from_zmm(self, zmm_obj, get_elevation=False, **kwargs):
        """

        :param zmm_obj: path ot .zmm file or ZMM object
        :type zmm_obj: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.zfiles.ZMM`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for ZMM object
        :type kwargs: dictionary

        """

        if isinstance(zmm_obj, (str, Path)):
            self._fn = Path(zmm_obj)
            zmm_obj = ZMM(**kwargs)
            zmm_obj.read(self._fn, get_elevation=get_elevation)
        if not isinstance(zmm_obj, ZMM):
            raise TypeError(f"Input must be a ZMM object not {type(zmm_obj)}")
        self.decimation_dict = zmm_obj.decimation_dict
        k_dict = OrderedDict(
            {
                "survey_metadata": "survey_metadata",
                "station_metadata": "station_metadata",
                "period": "periods",
            }
        )

        for tf_key, j_key in k_dict.items():
            setattr(self, tf_key, getattr(zmm_obj, j_key))
        self._transfer_function["transfer_function"].loc[
            dict(input=zmm_obj.input_channels, output=zmm_obj.output_channels)
        ] = zmm_obj.dataset.transfer_function.sel(
            input=zmm_obj.input_channels, output=zmm_obj.output_channels
        )
        self._transfer_function["inverse_signal_power"].loc[
            dict(input=zmm_obj.input_channels, output=zmm_obj.input_channels)
        ] = zmm_obj.dataset.inverse_signal_power.sel(
            input=zmm_obj.input_channels, output=zmm_obj.input_channels
        )
        self._transfer_function["residual_covariance"].loc[
            dict(input=zmm_obj.output_channels, output=zmm_obj.output_channels)
        ] = zmm_obj.dataset.residual_covariance.sel(
            input=zmm_obj.output_channels, output=zmm_obj.output_channels
        )

        self._compute_error_from_covariance()
        self._rotation_angle = -1 * zmm_obj.declination

    def to_zrr(self):
        """

        Translate TF object to ZMM object.

        :return: ZMM object
        :rtype: :class:`mt_metadata.transfer_function.io.zfiles.ZMM`

        >>> from mt_metadata.transfer_functions import TF
        >>> from mt_metadata import TF_XML
        >>> t = TF(TF_XML)
        >>> t.read()
        >>> zmm_object = t.to_zmm()
        >>> zmm_object.processing_type = "new and fancy"
        >>> zmm_object.write()

        """
        return self.to_zmm()

    def from_zrr(self, zrr_obj, get_elevation=False, **kwargs):
        """

        :param zmm_obj: path ot .zmm file or ZMM object
        :type zmm_obj: str, :calss:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.zfiles.ZMM`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for ZMM object
        :type kwargs: dictionary

        """

        self.from_zmm(zrr_obj, get_elevation=get_elevation, **kwargs)

    def to_zss(self):
        """

        Translate TF object to ZMM object.

        :return: ZMM object
        :rtype: :class:`mt_metadata.transfer_function.io.zfiles.ZMM`

        >>> from mt_metadata.transfer_functions import TF
        >>> from mt_metadata import TF_XML
        >>> t = TF(TF_XML)
        >>> t.read()
        >>> zmm_object = t.to_zmm()
        >>> zmm_object.processing_type = "new and fancy"
        >>> zmm_object.write()

        """
        return self.to_zmm()

    def from_zss(self, zss_obj, get_elevation=False, **kwargs):
        """

        :param zmm_obj: path to .zmm file or ZMM object
        :type zmm_obj: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.zfiles.ZMM`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for ZMM object
        :type kwargs: dictionary

        """

        self.from_zmm(zss_obj, get_elevation=get_elevation, **kwargs)

    def to_avg(self):
        """

        Translate TF object to ZongeMTAvg object.

        .. note:: Not Implemented yet

        :return: ZongeMTAvg object
        :rtype: :class:`mt_metadata.transfer_function.io.zonge.ZongeMTAvg`


        """

        raise AttributeError("to_avg does not exist yet.")

    def from_avg(self, avg_obj, get_elevation=False, **kwargs):
        """

        :param avg_obj: path to .avg file or ZongeMTAvg object
        :type avg_obj: str, :class:`pathlib.Path`,
         :class:`mt_metadata.transfer_functions.io.zonge.ZongeMTAvg`
        :param get_elevation: Try to get elevation from US National Map,
         defaults to True
        :type get_elevation: bool
        :param kwargs: Keyword arguments for ZongeMTAvg object
        :type kwargs: dictionary

        """
        if isinstance(avg_obj, (str, Path)):
            self._fn = Path(avg_obj)
            avg_obj = ZongeMTAvg(**kwargs)
            avg_obj.read(self._fn, get_elevation=get_elevation)
        if not isinstance(avg_obj, ZongeMTAvg):
            raise TypeError(f"Input must be a ZMM object not {type(avg_obj)}")
        self.survey_metadata = avg_obj.survey_metadata
        self.station_metadata = avg_obj.station_metadata

        self.period = 1.0 / avg_obj.frequency
        self.impedance = avg_obj.z
        self.impedance_error = avg_obj.z_err

        if avg_obj.t is not None:
            self.tipper = avg_obj.t
            self.tipper_error = avg_obj.t_err


# ==============================================================================
#             Error
# ==============================================================================


class TFError(Exception):
    pass
    pass
