# -*- coding: utf-8 -*-
"""
====================
zonge
====================
    * Tools for interfacing with MTFT24
    * Tools for interfacing with MTEdit
    
    
Created on Tue Jul 11 10:53:23 2013
@author: jpeacock-pr
"""

# ==============================================================================
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from .metadata import Header
from mt_metadata.transfer_functions.tf import (
    Survey,
    Station,
    Run,
    Magnetic,
    Electric,
)
from mt_metadata.transfer_functions.io.tools import get_nm_elev

# ==============================================================================
# deal with avg files output from mtedit
# ==============================================================================
class ZongeMTAvg:
    """
    deal with avg files output from mtedit
    """

    def __init__(self, fn=None, **kwargs):

        self.logger = logger
        self.header = Header()

        self.info_keys = [
            "skip",
            "frequency",
            "e_magnitude",
            "b_magnitude",
            "z_magnitude",
            "z_phase",
            "apparent_resistivity",
            "apparent_resistivity_err",
            "z_phase_err",
            "coherency",
            "fc_use",
            "fc_try",
        ]

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.components = []

        self._comp_index_down = {
            "zxx": (0, 0),
            "zxy": (0, 1),
            "zyx": (1, 0),
            "zyy": (1, 1),
            "tzx": (0, 0),
            "tzy": (0, 1),
            "zxxr": (0, 0),
            "zxyr": (0, 1),
            "zyxr": (1, 0),
            "zyyr": (1, 1),
        }

        self._comp_index_up = {
            "zxx": (1, 1),
            "zxy": (1, 0),
            "zyx": (0, 1),
            "zyy": (0, 0),
            "tzx": (0, 1),
            "tzy": (0, 0),
            "zxxr": (1, 1),
            "zxyr": (1, 0),
            "zyxr": (0, 1),
            "zyyr": (0, 0),
        }

        self.freq_index_dict = None
        self.z_positive = "down"

        self.fn = fn

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_comp_index(self):
        """
        get the correct component index dictionary based on z_positive

        Down assumes x is north, y is east

        Up assumes x is east, y is north
        """
        if self.z_positive == "down":
            return self._comp_index_down
        elif self.z_positive == "up":
            return self._comp_index_up
        else:
            raise ValueError("z_postiive must be either [ 'up' | 'down' ]")

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, value):
        if value is not None:
            self._fn = Path(value)
        else:
            self._fn = None

    def read(self, fn=None, get_elevation=True):
        """
        Read into a pandas data frame

        :param fn: DESCRIPTION, defaults to None
        :type fn: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if fn is not None:
            self.fn = Path(fn)

        with self.fn.open("r") as fid:
            lines = fid.readlines()

        # read header
        data_lines = self.header.read_header(lines)

        data_list = []
        for line in data_lines:
            if "$" in line:
                key, comp = [ss.strip() for ss in line.split("=")]
            elif "skp" in line.lower() or len(line) < 2:
                continue
            else:
                line = line.replace("*", "0.50")
                values = [comp.lower()] + [
                    float(ss.strip()) for ss in line.split(",")
                ]
                entry = dict(
                    [
                        (key.lower(), value)
                        for key, value in zip(
                            ["comp"] + self.info_keys, values
                        )
                    ]
                )
                data_list.append(entry)

        self.df = pd.DataFrame(data_list)

        self.frequency = self.df.frequency.unique()
        self.frequency.sort()
        self.n_freq = self.frequency.size
        self.components = self.df.comp.unique()

        self.freq_index_dict = dict(
            [(ff, ii) for ii, ff in enumerate(self.frequency)]
        )

        self.z, self.z_err = self._fill_z()
        self.t, self.t_err = self._fill_t()

        if self.header.elevation == 0 and get_elevation:
            if self.header.latitude != 0 and self.header.longitude != 0:
                self.header.elevation = get_nm_elev(
                    self.header.latitude, self.header.longitude
                )

    def to_complex(self, zmag, zphase):
        """
        outputs of mtedit are magnitude and phase of z, convert to real and
        imaginary parts, phase is in milliradians

        """

        if isinstance(zmag, np.ndarray):
            assert len(zmag) == len(zphase)
        zreal = zmag * np.cos((zphase / 1000))
        zimag = zmag * np.sin((zphase / 1000))
        return zreal, zimag

    def to_amp_phase(self, zreal, zimag):
        """
        Convert to amplitude and phase from real and imaginary

        :param zreal: DESCRIPTION
        :type zreal: TYPE
        :param zimag: DESCRIPTION
        :type zimag: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if isinstance(zreal, np.ndarray):
            assert len(zreal) == len(zimag)
        zphase = np.arctan2(zimag, zreal) * 1000
        zmag = np.sqrt(zreal**2 + zimag**2)

        return zmag, zphase

    def _fill_z(self):
        """
        create Z array with data, need to take into account when the different
        components have different frequencies, sometimes one might get skipped.
        """

        z = np.zeros((self.n_freq, 2, 2), dtype=complex)
        z_err = np.ones((self.n_freq, 2, 2), dtype=float)

        comp_index = self._get_comp_index()

        for row in self.df[self.df.comp.str.startswith("z")].itertuples():
            ii, jj = comp_index[row.comp]
            f_index = self.freq_index_dict[row.frequency]
            z_real, z_imag = self.to_complex(row.z_magnitude, row.z_phase)
            z_real_error, z_imag_error = self.to_complex(
                (
                    np.sqrt(
                        (
                            (row.apparent_resistivity_err / 100)
                            * row.apparent_resistivity
                        )
                        * 5
                        * row.frequency
                    )
                ),
                row.z_phase_err,
            )

            z[f_index, ii, jj] = z_real + 1j * z_imag

            z_err[f_index, ii, jj] = np.sqrt(
                z_real_error**2 + z_imag_error**2
            )

        return z, z_err

    def _fill_t(self):
        """
        fill tipper values
        """

        if "tzx" not in self.df.comp.to_list():
            self.header.logger.debug(
                "No Tipper found in {self.fn.name}",
            )
            return None, None

        t = np.zeros((self.n_freq, 1, 2), dtype=complex)
        t_err = np.ones((self.n_freq, 1, 2), dtype=float)

        comp_index = self._get_comp_index()

        for row in self.df[self.df.comp.str.startswith("t")].itertuples():
            t_real, t_imag = self.to_complex(row.z_magnitude, row.z_phase)
            ii, jj = comp_index[row.comp]
            f_index = self.freq_index_dict[row.frequency]

            if self.z_positive == "up":
                t[f_index, ii, jj] = -1 * (t_real + t_imag * 1j)
            else:
                t[f_index, ii, jj] = t_real + t_imag * 1j
            # error estimation
            t_real_error, t_imag_error = self.to_complex(
                (
                    np.sqrt(
                        (
                            (row.apparent_resistivity_err / 100)
                            * row.apparent_resistivity
                        )
                    )
                ),
                row.z_phase_err,
            )
            t_err[f_index, ii, jj] = np.sqrt(t_real**2 + t_imag**2)

        return t, t_err

    @property
    def run_metadata(self):
        rm = Run(id="001")
        rm.data_logger.id = self.header.instrument_id
        rm.data_logger.type = self.header.instrument_type
        rm.data_logger.manufacturer = "Zonge International"
        rm.data_logger.firmware = self.header.firmware
        if self.header.start_time is not None:
            rm.time_period.start = self.header.start_time

        if "zxy" in self.components:
            rm.add_channel(self.ex_metadata)
            rm.add_channel(self.ey_metadata)
            rm.add_channel(self.hx_metadata)
            rm.add_channel(self.hy_metadata)

        if "tzx" in self.components:
            rm.add_channel(self.hz_metadata)

        return rm

    @property
    def ex_metadata(self):
        ch = Electric(component="ex")
        if self.header._has_channel("zxy"):
            ch.dipole_length = self.header._comp_dict["zxy"]["rx"].length
            ch.measurement_azimuth = self.header._comp_dict["zxy"][
                "ch"
            ].azimuth[0]
            ch.translated_azimuth = self.header._comp_dict["zxy"][
                "ch"
            ].azimuth[0]
            ch.measurement_tilt = self.header._comp_dict["zxy"]["ch"].incl[0]
            ch.translated_tilt = self.header._comp_dict["zxy"]["ch"].incl[0]
            ch.channel_id = self.header._comp_dict["zxy"]["ch"].number[0]
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0]
            ch.translated_azimuth = self.header.rx.h_p_r[0]
            ch.channel_id = 4

        return ch

    @property
    def ey_metadata(self):
        ch = Electric(component="ey")
        if self.header._has_channel("zyx"):
            ch.dipole_length = self.header._comp_dict["zyx"]["rx"].length
            ch.measurement_azimuth = self.header._comp_dict["zyx"][
                "ch"
            ].azimuth[0]
            ch.translated_azimuth = self.header._comp_dict["zyx"][
                "ch"
            ].azimuth[0]
            ch.measurement_tilt = self.header._comp_dict["zyx"]["ch"].incl[0]
            ch.translated_tilt = self.header._comp_dict["zyx"]["ch"].incl[0]
            ch.channel_id = self.header._comp_dict["zyx"]["ch"].number[0]
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
            ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
            ch.channel_id = 5

        return ch

    @property
    def hx_metadata(self):
        ch = Magnetic(component="hx")
        if self.header._has_channel("zyx"):
            ch.measurement_azimuth = self.header._comp_dict["zyx"][
                "ch"
            ].azimuth[1]
            ch.translated_azimuth = self.header._comp_dict["zyx"][
                "ch"
            ].azimuth[1]
            ch.measurement_tilt = self.header._comp_dict["zyx"]["ch"].incl[1]
            ch.translated_tilt = self.header._comp_dict["zyx"]["ch"].incl[1]
            ch.sensor.id = self.header._comp_dict["zyx"]["ch"].number[1]
            ch.channel_id = 1
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0]
            ch.translated_azimuth = self.header.rx.h_p_r[0]
            ch.channel_id = 1

        return ch

    @property
    def hy_metadata(self):
        ch = Magnetic(component="hy")
        if self.header._has_channel("zxy"):
            ch.measurement_azimuth = self.header._comp_dict["zxy"][
                "ch"
            ].azimuth[1]
            ch.translated_azimuth = self.header._comp_dict["zxy"][
                "ch"
            ].azimuth[1]
            ch.measurement_tilt = self.header._comp_dict["zxy"]["ch"].incl[1]
            ch.translated_tilt = self.header._comp_dict["zxy"]["ch"].incl[1]
            ch.sensor.id = self.header._comp_dict["zxy"]["ch"].number[1]
            ch.channel_id = 2
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
            ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
            ch.channel_id = 2

        return ch

    @property
    def hz_metadata(self):
        ch = Magnetic(component="hz")
        if self.header._has_channel("tzx"):
            ch.measurement_azimuth = self.header._comp_dict["tzx"][
                "ch"
            ].azimuth[1]
            ch.translated_azimuth = self.header._comp_dict["tzx"][
                "ch"
            ].azimuth[1]
            ch.measurement_tilt = self.header._comp_dict["tzx"]["ch"].incl[1]
            ch.translated_tilt = self.header._comp_dict["tzx"]["ch"].incl[1]
            ch.sensor.id = self.header._comp_dict["tzx"]["ch"].number[1]
            ch.channel_id = 3
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[-1]
            ch.translated_azimuth = self.header.rx.h_p_r[-1]
            ch.channel_id = 3

        return ch

    @property
    def station_metadata(self):
        sm = Station()

        sm.id = self.header.station
        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude
        sm.location.elevation = self.header.elevation
        sm.location.datum = self.header.datum.upper()

        sm.transfer_function.id = self.header.station
        sm.transfer_function.software.author = "Zonge International"
        sm.transfer_function.software.name = "MTEdit"
        sm.transfer_function.software.version = (
            self.header.m_t_edit.version.split()[0]
        )
        sm.transfer_function.software.last_updated = (
            self.header.m_t_edit.version.split()[-1]
        )

        for key, value in self.header.m_t_edit.to_dict(single=True).items():
            if "version" in key:
                continue
            sm.transfer_function.processing_parameters.append(
                f"mtedit.{key}={value}"
            )

        sm.data_type = self.header.survey.type
        sm.add_run(self.run_metadata)
        sm.transfer_function.runs_processed = [self.run_metadata.id]
        if self.header.start_time is not None:
            sm.time_period.start = self.header.start_time

        return sm

    @station_metadata.setter
    def station_metadata(self, sm):
        self.header.station = sm.id
        self.header.latitdude = sm.location.latitude
        self.header.longitude = sm.location.longitude

        if hasattr(sm.run[0].ex):
            self.header.rx.length = sm.run[0].ex.dipole_length

    @property
    def survey_metadata(self):
        sm = Survey()
        sm.add_station(self.station_metadata)
        sm.update_time_period()
        return sm

    def write(self, fn):
        """
        Write an .avg file

        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        header_lines = self.header.write_header()

        header_lines.append(
            "Skp,Freq,      E.mag,      B.mag,      Z.mag,      Z.phz,   "
            "ARes.mag,   ARes.%err,Z.perr,  Coher,   FC.NUse,FC.NTry"
        )

        for key in self.comp_dict.keys():
            header_lines.append(f"$Rx.comp = {key.capitalize()}")
            value_array = self.comp_dict[key]
            for ii in range(value_array.size):
                line = []
                for jj, ikey, fmt in zip(
                    range(len(self.info_keys)), self.info_keys, self.info_fmt
                ):
                    value = value_array[ikey.lower()][ii]
                    s = f"{value:{fmt}},"
                    if jj == 0:
                        line.append(f"{s:<1}")
                    elif jj > 0 and jj < 8:
                        line.append(f"{s:<10}")
                    else:
                        line.append(f"{s:<7}")
                header_lines.append(" ".join(line))
        with open(fn, "w") as fid:
            fid.write("\n".join(header_lines))
