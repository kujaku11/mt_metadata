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

from .metadata import Header
from mt_metadata.transfer_functions.tf import (
    Survey,
    Station,
    Run,
    Magnetic,
    Electric,
)

# ==============================================================================
# deal with avg files output from mtedit
# ==============================================================================
class ZongeMTAvg:
    """
    deal with avg files output from mtedit
    """

    def __init__(self, fn=None):

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
            "z_err",
            "coherency",
            "fc_use",
            "fc_try",
        ]

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None

        self.comp_index = {
            "zxx": (0, 0),
            "zxy": (0, 1),
            "zyx": (1, 0),
            "zyy": (1, 1),
            "tzx": (0, 0),
            "tzy": (0, 1),
        }

        self.freq_index_dict = None
        self.z_coordinate = "down"

        self.fn = fn

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, value):
        if value is not None:
            self._fn = Path(value)
        else:
            self._fn = None

    def read(self, fn=None):
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

        df = pd.DataFrame(data_list)

        self.frequency = df.frequency.unique()
        self.frequency.sort()
        self.n_freq = self.frequency.size

        self.freq_index_dict = dict(
            [(ff, ii) for ii, ff in enumerate(self.frequency)]
        )

        self.z, self.z_err = self._fill_z(df)
        self.t, self.t_err = self._fill_t(df)

    def to_complex(self, zmag, zphase):
        """
        outputs of mtedit are magnitude and phase of z, convert to real and
        imaginary parts, phase is in milliradians

        """

        if isinstance(zmag, np.ndarray):
            assert len(zmag) == len(zphase)
        if self.z_coordinate == "up":
            zreal = zmag * np.cos((zphase / 1000) % np.pi)
            zimag = zmag * np.sin((zphase / 1000) % np.pi)
        else:
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
        if self.z_coordinate == "up":
            zphase = (np.arctan2(zimag, zreal) % np.pi) * 1000
        else:
            zphase = np.arctan2(zimag, zreal) * 1000
        zmag = np.sqrt(zreal**2 + zimag**2)

        return zmag, zphase

    def _fill_z(self, df):
        """
        create Z array with data, need to take into account when the different
        components have different frequencies, sometimes one might get skipped.
        """

        z = np.zeros((self.n_freq, 2, 2), dtype=complex)
        z_err = np.zeros((self.n_freq, 2, 2), dtype=float)

        for row in df.itertuples():
            if "z" in row.comp:
                z_real, z_imag = self.to_complex(row.z_magnitude, row.z_phase)
                ii, jj = self.comp_index[row.comp]
                f_index = self.freq_index_dict[row.frequency]

                z[f_index, ii, jj] = z_real + 1j * z_imag
                z_err[f_index, ii, jj] = row.z_err * 0.005

        return z, z_err

    def _fill_t(self, df):
        """
        fill tipper values
        """

        if "txy" not in df.comp.to_list():
            self.header.logger.debug("No Tipper found in %s", self.fn.name)
            return None, None

        tipper = np.zeros((self.n_freq, 1, 2), dtype=complex)
        tipper_err = np.ones((self.n_freq, 1, 2), dtype=float)

        for row in df.itertuples():
            if "t" in row.comp:
                t_real, t_imag = self.to_complex(row.z_magnitude, row.z_phase)
                ii, jj = self.comp_index[row.comp]
                f_index = self.freq_index_dict[row.frequency]

                if self.z_coordinate == "up":
                    self.tipper[f_index, ii, jj] = -1 * (t_real + t_imag * 1j)
                else:
                    self.tipper[f_index, ii, jj] = t_real + t_imag * 1j
                # error estimation
                self.tipper_err[f_index, ii, jj] += (
                    row.apparent_resistivity_err
                    * 0.05
                    * np.sqrt(t_real**2 + t_imag**2)
                )

        return tipper, tipper_err

    @property
    def station_metadata(self):
        sm = Station()

        sm.id = self.header.station
        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude
        sm.location.elevation = self.header.elevation
        sm.location.datum = self.header.datum

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
        sm.transfer_function.runs_processed = ["001"]

        sm.data_type = self.header.survey.type
        sm.runs.append(Run(id="001"))
        for comp in self.comp_lst_z + self.comp_lst_tip:
            if "zx" in comp:
                ch = Electric(component="ex")
                ch.dipole_length = self.header.rx.length
                ch.measurement_azimuth = self.header.rx.h_p_r[0]
                ch.translated_azimuth = self.header.rx.h_p_r[0]
                ch.channel_id = 1
                sm.runs[0].add_channel(ch)
            elif "zy" in comp:
                ch = Electric(component="ey")
                ch.dipole_length = self.header.rx.length
                ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
                ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
                ch.channel_id = 2
                sm.runs[0].add_channel(ch)
            if comp[-1] == "x":
                ch = Magnetic(component="hx")
                ch.measurement_azimuth = self.header.rx.h_p_r[0]
                ch.translated_azimuth = self.header.rx.h_p_r[0]
                ch.channel_id = 3
                sm.runs[0].add_channel(ch)
            elif comp[-1] == "y":
                ch = Magnetic(component="hy")
                ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
                ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
                ch.channel_id = 4
                sm.runs[0].add_channel(ch)
            if comp[1] == "z":
                ch = Magnetic(component="hz")
                ch.measurement_tilt = self.header.rx.h_p_r[-1]
                ch.translated_tilt = self.header.rx.h_p_r[-1]
                ch.translated_azimuth = self.header.rx.h_p_r[0]
                ch.channel_id = 5
                sm.runs[0].add_channel(ch)
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
        return Survey()

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


# =============================================================================
# Read
# =============================================================================


def read_avg(fn):
    """
    Read an .avg file output by MTEdit developed by Zonge International.

    :param fn: full path to .avg file to be read
    :type fn: string or :class:`pathlib.Path`
    :return: Transfer Function object
    :rtype: :class:`mt_metadata.transfer_functions.core.TF`

    """
    from mt_metadata.transfer_functions.core import TF

    obj = ZongeMTAvg(fn=fn)

    tf_object = TF()
    tf_object.survey_metadata = obj.survey_metadata
    tf_object.station_metadata = obj.station_metadata

    tf_object.period = 1.0 / obj.frequency
    tf_object.impedance = obj.z
    tf_object.impedance_error = obj.z_err

    if obj.t is not None:
        tf_object.tipper = obj.t
        tf_object.tipper_error = obj.t_err
    tf_object._fn = fn

    return tf_object


def write_avg(tf_object, fn=None, **kwargs):
    """
    write an .avg file.

    :param fn: DESCRIPTION
    :type fn: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    raise AttributeError("Writing an AVG file does not exist yet.")

    # from mt_metadata.transfer_functions.core import TF

    # if not isinstance(tf_object, TF):
    #     raise ValueError("Input must be an mt_metadata.transfer_functions.core object")

    # zavg = ZongeMTAvg()
    # zavg.station_metadata = tf_object.station_metadata

    # zavg.comp_dict = zavg._make_comp_dict(tf_object.period.size)
    # if tf_object.has_impedance():
    #     for key in ["zxx", "zxy", "zyx", "zyy"]:
