# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:34:23 2017
@author: jrpeacock

Translated from code by B. Murphy.
"""

# ==============================================================================
# Imports
# ==============================================================================
from pathlib import Path
from collections import OrderedDict

import numpy as np
import xarray as xr

from mt_metadata.transfer_functions.tf import (
    Survey,
    Station,
    Run,
    Electric,
    Magnetic,
)
from .metadata import Channel
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.utils.list_dict import ListDict

# ==============================================================================
class ZMMError(Exception):
    pass


class ZMMHeader(object):
    """
    Container for Header of an Egbert file
    """

    def __init__(self, fn=None, **kwargs):

        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.processing_type = None
        self.num_channels = None
        self.num_freq = None
        self._header_count = 0
        self._component_dict = None
        self.ex = None
        self.ey = None
        self.hx = None
        self.hy = None
        self.hz = None
        self._zfn = None
        self.fn = fn
        self.station_metadata = Station()
        self._channel_order = ["hx", "hy", "hz", "ex", "ey"]
        self._header_lines = [
            "TRANSFER FUNCTIONS IN MEASUREMENT COORDINATES",
            "********* WITH FULL ERROR COVARIANCE ********",
        ]

    @property
    def fn(self):
        return self._zfn

    @fn.setter
    def fn(self, value):
        if value is None:
            return
        value = Path(value)
        if value.suffix.lower() in [".zmm", ".zrr", ".zss"]:
            self._zfn = value
        else:
            msg = f"Input file must be a *.zmm or *.zrr file not {value.suffix}"
            self.logger.error(msg)
            raise ValueError(msg)

    @property
    def latitude(self):
        return self.station_metadata.location.latitude

    @latitude.setter
    def latitude(self, lat):
        self.station_metadata.location.latitude = lat

    @property
    def longitude(self):
        return self.station_metadata.location.longitude

    @longitude.setter
    def longitude(self, lon):
        self.station_metadata.location.longitude = lon

    @property
    def elevation(self):
        return self.station_metadata.location.elevation

    @elevation.setter
    def elevation(self, value):
        self.station_metadata.location.elevation = value

    @property
    def declination(self):
        return self.station_metadata.location.declination.value

    @declination.setter
    def declination(self, value):
        self.station_metadata.location.declination.value = value

    @property
    def station(self):
        return self.station_metadata.id

    @station.setter
    def station(self, value):
        self.station_metadata.id = value

    def read_header(self, fn=None):
        """
        read header information
        """

        if fn is not None:
            self.fn = fn
        with open(self.fn, "r") as fid:
            line = fid.readline()

            self._header_count = 0
            header_list = []
            while "period" not in line:
                header_list.append(line)
                self._header_count += 1

                line = fid.readline()
        self.station_metadata.comments = ""
        station = header_list[3].lower().strip()
        if station.count(":") > 0:
            station = station.split(":")[1]
        self.station = station
        self.station_metadata._runs = ListDict()
        self.station_metadata.add_run(Run(id=f"{self.station}a"))
        self.station_metadata.transfer_function.id = self.station

        for ii, line in enumerate(header_list):
            if line.find("**") >= 0:
                self.station_metadata.comments += line.replace("*", "").strip()
            elif ii == 2:
                self.processing_type = line.lower().strip()
            elif "station" in line:
                self.station_metadata.id = line.split(":")[1].strip()
            elif "coordinate" in line:
                line_list = line.strip().split()
                self.latitude = line_list[1]
                lon = float(line_list[2])
                if lon > 180:
                    lon -= 360
                self.longitude = lon

                self.station_metadata.location.declination.value = float(
                    line_list[-1]
                )
            elif "number" in line:
                line_list = line.strip().split()
                self.num_channels = int(line_list[3])
                self.num_freq = int(line_list[-1])
            elif "orientations" in line:
                pass
            elif line.strip()[-2:].lower() in ["ex", "ey", "hx", "hy", "hz"]:
                line_list = line.strip().split()
                comp = line_list[-1].lower()
                channel_dict = {"channel": comp}
                channel_dict["chn_num"] = int(line_list[0])
                channel_dict["azm"] = float(line_list[1])
                channel_dict["tilt"] = float(line_list[2])
                channel_dict["dl"] = line_list[3]
                if channel_dict["chn_num"] == 0:
                    channel_dict["chn_num"] = self.num_channels
                setattr(self, comp, Channel(channel_dict))

                if comp in ["ex", "ey"]:
                    ch = Electric()
                elif comp in ["hx", "hy", "hz"]:
                    ch = Magnetic()
                ch.component = comp
                ch.measurement_azimuth = channel_dict["azm"]
                ch.measurement_tilt = channel_dict["tilt"]
                ch.translated_azimuth = channel_dict["azm"]
                ch.translated_tilt = channel_dict["tilt"]
                ch.channel_number = channel_dict["chn_num"]

                self.station_metadata.runs[0].add_channel(ch)

    def write_header(self):
        """
        write a zmm header

        TRANSFER FUNCTIONS IN MEASUREMENT COORDINATES
        ********** WITH FULL ERROR COVARINCE*********

        300
        coordinate    34.727  -115.735 declination    13.10
        number of channels   5   number of frequencies  38
        orientations and tilts of each channel
           1     0.00     0.00 300  Hx
           2    90.00     0.00 300  Hy
           3     0.00     0.00 300  Hz
           4     0.00     0.00 300  Ex
           5    90.00     0.00 300  Ey

        :return: properly formatted string
        :rtype: string

        """
        lines = [self._header_lines[0], self._header_lines[1], ""]
        lines += [f"{self.station}"]
        lines += [
            f"coordinate {self.latitude:>9.3f} {self.longitude:>9.3f} declination {self.declination:>8.2f}"
        ]
        lines += [
            f"number of channels  {self.num_channels:>3d}  number of frequencies {self.num_freq:>3d}"
        ]
        lines += [" orientations and tilts of each channel"]
        for ii, ch in enumerate(self._channel_order):
            try:
                channel = getattr(self, ch)
                if channel.number == None:
                    channel.number = int(ii)
                if channel.tilt is None:
                    channel.tilt = 0.0
                if channel.azimuth is None:
                    channel.azimuth = 0.0
                lines += [
                    (
                        f"{channel.number:>5d} "
                        f"{channel.azimuth:>8.2f} "
                        f"{channel.tilt:>8.2f} "
                        f"{self.station:>3} "
                        f"{channel.channel.capitalize():>3}"
                    )
                ]
            except (AttributeError, TypeError):
                self.logger.warning(f"Could not find {ch}")
                continue
        return lines

    @property
    def channels_recorded(self):
        channels = {}
        for cc in ["ex", "ey", "hx", "hy", "hz"]:
            ch = getattr(self, cc)
            if ch is not None:
                channels[ch.index] = ch.channel
        ordered_channels = [channels[k] for k in sorted(channels.keys())]
        return ordered_channels

    @property
    def input_channels(self):
        return self.channels_recorded[0:2]

    @property
    def output_channels(self):
        return self.channels_recorded[2:]

    @property
    def has_tipper(self):
        if "hz" in self.channels_recorded:
            return True
        return False

    @property
    def has_impedance(self):
        if "ex" in self.channels_recorded and "ey" in self.channels_recorded:
            return True
        return False


class ZMM(ZMMHeader):
    """
    Container for Egberts zrr format.

    """

    def __init__(self, fn=None, **kwargs):

        super().__init__()

        self.fn = fn
        self._header_count = 0
        self.transfer_functions = None
        self.sigma_e = None
        self.sigma_s = None
        self.periods = None
        self.dataset = None
        self.decimation_dict = {}

        self._ch_input_dict = {
            "impedance": ["hx", "hy"],
            "tipper": ["hx", "hy"],
            "isp": ["hx", "hy"],
            "res": ["ex", "ey", "hz"],
            "tf": ["hx", "hy"],
        }

        self._ch_output_dict = {
            "impedance": ["ex", "ey"],
            "tipper": ["hz"],
            "isp": ["hx", "hy"],
            "res": ["ex", "ey", "hz"],
            "tf": ["ex", "ey", "hz"],
        }

        self._transfer_function = self._initialize_transfer_function()

        for key in list(kwargs.keys()):
            setattr(self, key, kwargs[key])
        if self.fn is not None:
            self.read()

    def __str__(self):
        lines = [f"Station: {self.station}", "-" * 50]
        lines.append(f"\tSurvey:        {self.survey_metadata.id}")
        lines.append(f"\tProject:       {self.survey_metadata.project}")
        lines.append(
            f"\tAcquired by:   {self.station_metadata.acquired_by.author}"
        )
        lines.append(
            f"\tAcquired date: {self.station_metadata.time_period.start_date}"
        )
        lines.append(f"\tLatitude:      {self.latitude:.3f}")
        lines.append(f"\tLongitude:     {self.longitude:.3f}")
        lines.append(f"\tElevation:     {self.elevation:.3f}")
        if "ex" in self.output_channels:
            lines.append("\tImpedance:     True")
        else:
            lines.append("\tImpedance:     False")
        if "hz" in self.output_channels:
            lines.append("\tTipper:        True")
        else:
            lines.append("\tTipper:        False")
        if self.periods is not None:
            lines.append(f"\tNumber of periods: {self.periods.size}")
            lines.append(
                f"\t\tPeriod Range:   {self.periods.min():.5E} -- {self.periods.max():.5E} s"
            )
            lines.append(
                f"\t\tFrequency Range {1./self.periods.max():.5E} -- {1./self.periods.min():.5E} s"
            )
        return "\n".join(lines)

    def __repr__(self):
        lines = []
        lines.append(f"station='{self.station}'")
        lines.append(f"latitude={self.latitude:.2f}")
        lines.append(f"longitude={self.longitude:.2f}")
        lines.append(f"elevation={self.elevation:.2f}")

        return f"MT( {(', ').join(lines)} )"

    def _initialize_transfer_function(self, periods=[1]):
        """
        create an empty x array for the data.  For now this accommodates
        a single processed station.


        :return: DESCRIPTION
        :rtype: TYPE

        """
        # create an empty array for the transfer function
        tf = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["tf"],
                "input": self._ch_input_dict["tf"],
            },
            name="transfer_function",
        )

        tf_err = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["tf"],
                "input": self._ch_input_dict["tf"],
            },
            name="error",
        )

        inv_signal_power = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["isp"],
                "input": self._ch_input_dict["isp"],
            },
            name="inverse_signal_power",
        )

        residual_covariance = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["res"],
                "input": self._ch_input_dict["res"],
            },
            name="residual_covariance",
        )

        # will need to add in covariance in some fashion
        return xr.Dataset(
            {
                tf.name: tf,
                tf_err.name: tf_err,
                inv_signal_power.name: inv_signal_power,
                residual_covariance.name: residual_covariance,
            }
        )

    @property
    def frequencies(self):
        if self.periods is None:
            return None
        return 1.0 / self.periods

    def initialize_arrays(self):
        """
        make initial arrays based on number of frequencies and channels
        """
        if self.num_freq is None:
            return
        self.periods = np.zeros(self.num_freq)
        self.transfer_functions = np.zeros(
            (self.num_freq, self.num_channels - 2, 2), dtype=np.complex64
        )

        # residual covariance -- square matrix with dimension as number of
        # predicted channels
        self.sigma_e = np.zeros(
            (self.num_freq, self.num_channels - 2, self.num_channels - 2),
            dtype=np.complex64,
        )

        # inverse coherent signal power -- square matrix, with dimension as the
        #    number of predictor channels
        # since EMTF and this code assume N predictors is 2,
        #    this dimension is hard-coded
        self.sigma_s = np.zeros((self.num_freq, 2, 2), dtype=np.complex64)

    def read(self, fn=None):
        """
        Read in Egbert zrr/zmm file

        :param fn: full path to zmm/zrr file
        :type fn: string or pathlib.Path
        """
        if fn is not None:
            self.fn = fn
        self.read_header()
        self.initialize_arrays()

        self._ch_input_dict = {
            "impedance": self.input_channels,
            "tipper": self.input_channels,
            "isp": self.input_channels,
            "res": self.output_channels,
            "tf": self.input_channels,
        }

        self._ch_output_dict = {
            "impedance": ["ex", "ey"],
            "tipper": ["hz"],
            "isp": self.input_channels,
            "res": self.output_channels,
            "tf": self.output_channels,
        }

        self._transfer_function = self._initialize_transfer_function()
        self.dataset = self._initialize_transfer_function()

        ### read each data block and fill the appropriate array
        for ii, period_block in enumerate(self._get_period_blocks()):
            data_block = self._read_period_block(period_block)
            self.periods[ii] = data_block["period"]

            self._fill_tf_array_from_block(data_block["tf"], ii)
            self._fill_sig_array_from_block(data_block["sig"], ii)
            self._fill_res_array_from_block(data_block["res"], ii)
        self._fill_dataset()

        self.station_metadata.id = self.station
        self.station_metadata.data_type = "MT"
        self.station_metadata.channels_recorded = self.channels_recorded
        # provenance
        self.station_metadata.provenance.software.name = "EMTF"
        self.station_metadata.provenance.software.version = "1"
        self.station_metadata.transfer_function.runs_processed = (
            self.station_metadata.run_list
        )
        self.station_metadata.transfer_function.software.name = "EMTF"
        self.station_metadata.transfer_function.software.version = "1"
        self.station_metadata.runs[0].sample_rate = np.median(
            np.array([d["df"] for k, d in self.decimation_dict.items()])
        )

        # add information to runs
        for rr in self.station_metadata.runs:
            if self.transfer_functions.shape[1] >= 2:
                rr.ex = self.ex_metadata
                rr.ey = self.ey_metadata
            rr.hx = self.hx_metadata
            rr.hy = self.hy_metadata
            if self.hz is not None:
                rr.hz = self.hz_metadata

    def write(self, fn, decimation_levels=None):
        """
        write a zmm file

        decimation_levels should be a dictionary with keys

            * decimation_level

        values will be a dictionary with keys

            * frequency_band, value = (min, max)
            * n_points, value = int
            * sampling_freq, value = float
        """
        if fn is not None:
            self.fn = fn
        lines = self.write_header()

        for p in self.dataset.period.data:
            a = self.dataset.sel(period=p)
            try:
                dec_dict = self.decimation_dict[f"{p:10g}"]
            except KeyError:
                dec_dict = {
                    "level": 0,
                    "bands": (0, 0),
                    "npts": 0,
                    "df": self.station_metadata.runs[0].sample_rate,
                }
            lines += [
                (
                    f"period : {p:^18.5f} "
                    f"decimation level {dec_dict['level']:^8d}"
                    f"freq. band from {dec_dict['bands'][0]:>5d} to {dec_dict['bands'][1]:>5d}"
                )
            ]
            lines += [
                f"number of data point {dec_dict['npts']} sampling freq. {dec_dict['df']} Hz"
            ]
            # write tf
            lines += [" Transfer Functions"]
            for c_out in self.output_channels:
                line = ""
                for c_in in self.input_channels:
                    tf_element = a.transfer_function.loc[
                        dict(output=c_out, input=c_in)
                    ].data
                    line += f"{tf_element.real:>12.4E}{tf_element.imag:>12.4E}"
                lines += [line]
            # write signal power
            lines += [" Inverse Coherent Signal Power Matrix"]
            for ii, c_out in enumerate(self.input_channels):
                line = ""
                for c_in in self.input_channels[: ii + 1]:
                    tf_element = a.inverse_signal_power.loc[
                        dict(output=c_out, input=c_in)
                    ].data
                    line += f"{tf_element.real:>12.4E}{tf_element.imag:>12.4E}"
                lines += [line]
            # write residual covariance
            lines += [" Residual Covariance"]
            for ii, c_out in enumerate(self.output_channels):
                line = ""
                for c_in in self.output_channels[: ii + 1]:
                    tf_element = a.residual_covariance.loc[
                        dict(output=c_out, input=c_in)
                    ].data
                    line += f"{tf_element.real:>12.4E}{tf_element.imag:>12.4E}"
                lines += [line]
        with open(self.fn, "w") as fid:
            fid.write("\n".join(lines))
        return self.fn

    def _get_period_blocks(self):
        """
        split file into period blocks
        """

        with open(self.fn, "r") as fid:
            fn_str = fid.read()
        period_strings = fn_str.lower().split("period")
        period_blocks = []
        for per in period_strings:
            period_blocks.append(per.split("\n"))
        return period_blocks[1:]

    def _read_period_block(self, period_block):
        """
        read block:
            period :      0.01587    decimation level   1    freq. band from   46 to   80
            number of data point  951173 sampling freq.   0.004 Hz
             Transfer Functions
              0.1474E+00 -0.2049E-01  0.1618E+02  0.1107E+02
             -0.1639E+02 -0.1100E+02  0.5559E-01  0.1249E-01
             Inverse Coherent Signal Power Matrix
              0.2426E+03 -0.2980E-06
              0.9004E+02 -0.2567E+01  0.1114E+03  0.1192E-06
             Residual Covaraince
              0.8051E-05  0.0000E+00
             -0.2231E-05 -0.2863E-06  0.8866E-05  0.0000E+00
        """

        period = float(period_block[0].strip().split(":")[1].split()[0].strip())
        level = int(
            period_block[0].strip().split("level")[1].split()[0].strip()
        )
        bands = (
            int(period_block[0].strip().split("from")[1].split()[0].strip()),
            int(period_block[0].strip().split("to")[1].split()[0].strip()),
        )

        npts = int(period_block[1].strip().split("point")[1].split()[0].strip())
        sr = float(period_block[1].strip().split("freq.")[1].split()[0].strip())
        self.decimation_dict[f"{period:.10g}"] = {
            "level": level,
            "bands": bands,
            "npts": npts,
            "df": sr,
        }
        data_dict = {"period": period, "tf": [], "sig": [], "res": []}
        key = "tf"
        for line in period_block[2:]:
            if "transfer" in line.lower():
                key = "tf"
                continue
            elif "signal" in line.lower():
                key = "sig"
                continue
            elif "residual" in line.lower():
                key = "res"
                continue
            line_list = [float(xx) for xx in line.strip().split()]
            values = [
                complex(line_list[ii], line_list[ii + 1])
                for ii in range(0, len(line_list), 2)
            ]
            data_dict[key].append(values)
        return data_dict

    def _flatten_list(self, x_list):
        """
        flatten = lambda l: [item for sublist in l for item in sublist]

        Returns
        -------
        None.

        """

        flat_list = [item for sublist in x_list for item in sublist]

        return flat_list

    def _fill_tf_array_from_block(self, tf_block, index):
        """
        fill tf arrays from data blocks
        """
        tf_block = self._flatten_list(tf_block)
        for kk, jj in enumerate(range(0, len(tf_block), 2)):
            self.transfer_functions[index, kk, 0] = tf_block[jj]
            self.transfer_functions[index, kk, 1] = tf_block[jj + 1]

    def _fill_sig_array_from_block(self, sig_block, index):
        """
        fill signal array
        """
        sig_block = self._flatten_list(sig_block)
        self.sigma_s[index, 0, 0] = sig_block[0]
        self.sigma_s[index, 1, 0] = sig_block[1]
        self.sigma_s[index, 0, 1] = sig_block[1]
        self.sigma_s[index, 1, 1] = sig_block[2]

    def _fill_res_array_from_block(self, res_block, index):
        """
        fill residual covariance array
        """
        for jj in range(self.num_channels - 2):
            values = res_block[jj]
            for kk in range(jj + 1):
                if jj == kk:
                    self.sigma_e[index, jj, kk] = values[kk]
                else:
                    self.sigma_e[index, jj, kk] = values[kk]
                    self.sigma_e[index, kk, jj] = values[kk].conjugate()

    def _fill_dataset(self):
        """
        fill the dataset

        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.dataset = self._initialize_transfer_function(periods=self.periods)

        self.dataset.transfer_function.loc[
            dict(input=self.input_channels, output=self.output_channels)
        ] = self.transfer_functions
        self.dataset.inverse_signal_power.loc[
            dict(input=self.input_channels, output=self.input_channels)
        ] = self.sigma_s
        self.dataset.residual_covariance.loc[
            dict(input=self.output_channels, output=self.output_channels)
        ] = self.sigma_e

    def calculate_impedance(self, angle=0.0):
        """
        calculate the impedances from the transfer functions
        """

        # check to see if there are actually electric fields in the TFs
        if not hasattr(self, "ex") or not hasattr(self, "ey"):
            msg = (
                "Cannot return apparent resistivity and phase "
                "data because these TFs do not contain electric "
                "fields as a predicted channel."
            )
            self.logger.error(msg)
            raise ZMMError(msg)
        # transform the TFs first...
        # build transformation matrix for predictor channels
        #    (horizontal magnetic fields)
        hx_index = self.hx.index
        hy_index = self.hy.index
        u = np.eye(2, 2)
        u[hx_index, hx_index] = np.cos(np.deg2rad(self.hx.azimuth - angle))
        u[hx_index, hy_index] = np.sin(np.deg2rad(self.hx.azimuth - angle))
        u[hy_index, hx_index] = np.cos(np.deg2rad(self.hy.azimuth - angle))
        u[hy_index, hy_index] = np.sin(np.deg2rad(self.hy.azimuth - angle))
        u = np.linalg.inv(u)

        # build transformation matrix for predicted channels (electric fields)
        ex_index = self.ex.index
        ey_index = self.ey.index
        v = np.eye(
            self.transfer_functions.shape[1], self.transfer_functions.shape[1]
        )
        v[ex_index - 2, ex_index - 2] = np.cos(
            np.deg2rad(self.ex.azimuth - angle)
        )
        v[ey_index - 2, ex_index - 2] = np.sin(
            np.deg2rad(self.ex.azimuth - angle)
        )
        v[ex_index - 2, ey_index - 2] = np.cos(
            np.deg2rad(self.ey.azimuth - angle)
        )
        v[ey_index - 2, ey_index - 2] = np.sin(
            np.deg2rad(self.ey.azimuth - angle)
        )

        # matrix multiplication...
        rotated_transfer_functions = np.matmul(
            v, np.matmul(self.transfer_functions, u.T)
        )
        rotated_sigma_s = np.matmul(u, np.matmul(self.sigma_s, u.T))
        rotated_sigma_e = np.matmul(v, np.matmul(self.sigma_e, v.T))

        # now pull out the impedance tensor
        z = np.zeros((self.num_freq, 2, 2), dtype=np.complex64)
        z[:, 0, 0] = rotated_transfer_functions[
            :, ex_index - 2, hx_index
        ]  # Zxx
        z[:, 0, 1] = rotated_transfer_functions[
            :, ex_index - 2, hy_index
        ]  # Zxy
        z[:, 1, 0] = rotated_transfer_functions[
            :, ey_index - 2, hx_index
        ]  # Zyx
        z[:, 1, 1] = rotated_transfer_functions[
            :, ey_index - 2, hy_index
        ]  # Zyy

        # and the variance information
        var = np.zeros((self.num_freq, 2, 2))
        var[:, 0, 0] = np.real(
            rotated_sigma_e[:, ex_index - 2, ex_index - 2]
            * rotated_sigma_s[:, hx_index, hx_index]
        )
        var[:, 0, 1] = np.real(
            rotated_sigma_e[:, ex_index - 2, ex_index - 2]
            * rotated_sigma_s[:, hy_index, hy_index]
        )
        var[:, 1, 0] = np.real(
            rotated_sigma_e[:, ey_index - 2, ey_index - 2]
            * rotated_sigma_s[:, hx_index, hx_index]
        )
        var[:, 1, 1] = np.real(
            rotated_sigma_e[:, ey_index - 2, ey_index - 2]
            * rotated_sigma_s[:, hy_index, hy_index]
        )

        error = np.sqrt(var)

        return z, error

    def calculate_tippers(self, angle=0.0):
        """
        calculate induction vectors
        """

        # check to see if there is a vertical magnetic field in the TFs
        if self.hz is None:
            raise ZMMError(
                "Cannot return tipper data because the TFs do not "
                "contain the vertical magnetic field as a "
                "predicted channel."
            )
        # transform the TFs first...
        # build transformation matrix for predictor channels
        #    (horizontal magnetic fields)
        hx_index = self.hx.index
        hy_index = self.hy.index
        u = np.eye(2, 2)
        u[hx_index, hx_index] = np.cos(np.deg2rad(self.hx.azimuth - angle))
        u[hx_index, hy_index] = np.sin(np.deg2rad(self.hx.azimuth - angle))
        u[hy_index, hx_index] = np.cos(np.deg2rad(self.hy.azimuth - angle))
        u[hy_index, hy_index] = np.sin(np.deg2rad(self.hy.azimuth - angle))
        u = np.linalg.inv(u)

        # don't need to transform predicated channels (assuming no tilt in Hz)
        hz_index = self.hz.index
        v = np.eye(
            self.transfer_functions.shape[1], self.transfer_functions.shape[1]
        )

        # matrix multiplication...
        rotated_transfer_functions = np.matmul(
            v, np.matmul(self.transfer_functions, u.T)
        )
        rotated_sigma_s = np.matmul(u, np.matmul(self.sigma_s, u.T))
        rotated_sigma_e = np.matmul(v, np.matmul(self.sigma_e, v.T))

        # now pull out tipper information
        tipper = np.zeros((self.num_freq, 2), dtype=np.complex64)
        tipper[:, 0] = rotated_transfer_functions[
            :, hz_index - 2, hx_index
        ]  # Tx
        tipper[:, 1] = rotated_transfer_functions[
            :, hz_index - 2, hy_index
        ]  # Ty

        # and the variance/error information
        var = np.zeros((self.num_freq, 2))
        var[:, 0] = np.real(
            rotated_sigma_e[:, hz_index - 2, hz_index - 2]
            * rotated_sigma_s[:, hx_index, hx_index]
        )  # Tx
        var[:, 1] = np.real(
            rotated_sigma_e[:, hz_index - 2, hz_index - 2]
            * rotated_sigma_s[:, hy_index, hy_index]
        )  # Ty
        error = np.sqrt(var)

        tipper = tipper.reshape((self.num_freq, 1, 2))
        error = error.reshape((self.num_freq, 1, 2))

        return tipper, error

    @property
    def survey_metadata(self):
        sm = Survey()

        return sm

    def _get_electric_metadata(self, comp):
        """
        get electric information from the various metadata
        """
        comp = comp.lower()
        electric = Electric()
        electric.positive.type = "electric"
        electric.negative.type = "electric"
        if hasattr(self, comp):
            meas = getattr(self, comp)
            electric.measurement_azimuth = meas.azimuth
            electric.measurement_tilt = meas.tilt
            electric.component = comp
            electric.channel_number = meas.number
            electric.channel_id = meas.number
        return electric

    @property
    def ex_metadata(self):
        return self._get_electric_metadata("ex")

    @property
    def ey_metadata(self):
        return self._get_electric_metadata("ey")

    def _get_magnetic_metadata(self, comp):
        """

        get magnetic metadata from the various sources

        :param comp: DESCRIPTION
        :type comp: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        comp = comp.lower()
        magnetic = Magnetic()
        if hasattr(self, comp):
            meas = getattr(self, comp)
            magnetic.measurement_azimuth = meas.azimuth
            magnetic.measurement_tilt = meas.tilt
            magnetic.component = comp
            magnetic.channel_number = meas.number
            magnetic.channel_id = meas.number
        return magnetic

    @property
    def hx_metadata(self):
        return self._get_magnetic_metadata("hx")

    @property
    def hy_metadata(self):
        return self._get_magnetic_metadata("hy")

    @property
    def hz_metadata(self):
        return self._get_magnetic_metadata("hz")


def read_zmm(zmm_fn, **kwargs):
    """
    Write a Z file

    :param zmm_fn: full path to file to be read in
    :type zmm_fn: str :class:`pathlib.Path`
    :return: Returns a TF object
    :rtype: :class:`mt_metadata.transfer_functions.tf.core.TF`

    """

    # need to add this here instead of the top is because of recursive
    # importing.  This may not be the best way to do this but works for now
    # so we don't have to break how MTpy structure is setup now.
    from mt_metadata.transfer_functions.core import TF

    tf_obj = TF(**kwargs)
    tf_obj._fn = zmm_fn
    tf_obj.logger.debug(f"Reading {zmm_fn} using ZMM class")

    zmm_obj = ZMM(zmm_fn)
    zmm_obj.read()

    k_dict = OrderedDict(
        {
            "survey_metadata": "survey_metadata",
            "station_metadata": "station_metadata",
            "period": "periods",
        }
    )

    for tf_key, j_key in k_dict.items():
        setattr(tf_obj, tf_key, getattr(zmm_obj, j_key))
    tf_obj._transfer_function["transfer_function"].loc[
        dict(input=zmm_obj.input_channels, output=zmm_obj.output_channels)
    ] = zmm_obj.dataset.transfer_function.sel(
        input=zmm_obj.input_channels, output=zmm_obj.output_channels
    )
    tf_obj._transfer_function["inverse_signal_power"].loc[
        dict(input=zmm_obj.input_channels, output=zmm_obj.input_channels)
    ] = zmm_obj.dataset.inverse_signal_power.sel(
        input=zmm_obj.input_channels, output=zmm_obj.input_channels
    )
    tf_obj._transfer_function["residual_covariance"].loc[
        dict(input=zmm_obj.output_channels, output=zmm_obj.output_channels)
    ] = zmm_obj.dataset.residual_covariance.sel(
        input=zmm_obj.output_channels, output=zmm_obj.output_channels
    )

    tf_obj._compute_error_from_covariance()
    tf_obj._rotation_angle = -1 * zmm_obj.declination

    return tf_obj


def write_zmm(tf_object, fn=None):
    """
    write a zmm file

    :param tf_object: TF object
    :type tf_object: :class:`mt_metadata.transfer_functions.core.TF`
    :param fn: full path to new file, defaults to None
    :type fn: str or :class:`pathlib.Path`, optional
    :return: ZMM object
    :rtype: `mt_metadata.transfer_functions.io.ZMM`

    """
    from mt_metadata.transfer_functions.core import TF

    if not isinstance(tf_object, TF):
        raise ValueError("Input must be a TF object")
    zmm_obj = ZMM()
    zmm_obj.dataset = tf_object.dataset
    zmm_obj.station_metadata = tf_object.station_metadata

    # need to set the channel numbers according to the z-file format
    # with input channels (h's) and output channels (hz, e's).
    if tf_object.has_tipper():
        if tf_object.has_impedance():
            zmm_obj.num_channels = 5
            number_dict = {"hx": 1, "hy": 2, "hz": 3, "ex": 4, "ey": 5}
        else:
            zmm_obj.num_channels = 3
            number_dict = {"hx": 1, "hy": 2, "hz": 3}
    else:
        if tf_object.has_impedance():
            zmm_obj.num_channels = 4
            number_dict = {"hx": 1, "hy": 2, "ex": 4, "ey": 5}
    if tf_object.station_metadata.runs == []:
        run = Run()
        for ch, ch_num in number_dict.items():
            c = Channel()
            c.channel = ch
            c.number = ch_num
            setattr(zmm_obj, c.channel, c)
            if ch in ["ex", "ey"]:
                rc = Electric(component=ch, channel_number=ch_num)
                run.add_channel(rc)
            elif ch in ["hx", "hy", "hz"]:
                rc = Magnetic(component=ch, channel_number=ch_num)
                run.add_channel(rc)
        tf_object.station_metadata.add_run(run)

    else:
        for comp in tf_object.station_metadata.runs[0].channels_recorded_all:
            if "rr" in comp:
                continue
            ch = getattr(tf_object.station_metadata.runs[0], comp)
            c = Channel()
            c.from_dict(ch.to_dict(single=True))
            c.number = number_dict[c.channel]
            setattr(zmm_obj, c.channel, c)
    zmm_obj.survey_metadata.update(tf_object.survey_metadata)
    zmm_obj.num_freq = tf_object.period.size

    zmm_obj.write(fn)

    return zmm_obj
