# -*- coding: utf-8 -*-
"""
.. module:: JFile
   :synopsis: Deal with J-Files of the format propsed by Alan Jones 

.. moduleauthor:: Jared Peacock <jpeacock@usgs.gov>
"""

# ==============================================================================
from pathlib import Path
import numpy as np
from collections import OrderedDict

from mt_metadata.transfer_functions.tf import Survey, Station, Run
from mt_metadata.utils.mttime import MTime
from mt_metadata.utils.mt_logger import setup_logger
from .metadata import Header

# ==============================================================================
# Class to read j_file
# ==============================================================================
class JFile:
    """
    be able to read and write a j-file
    """

    def __init__(self, fn=None):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.header = Header()
    
        
        self._jfn = None
        self.fn = fn

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.frequency = None

        if self.fn is not None:
            self.read_j_file()

    def __str__(self):
        lines = [f"Station: {self.header.station}", "-" * 50]
        lines.append(f"\tSurvey:        {self.survey_metadata.id}")
        lines.append(f"\tProject:       {self.survey_metadata.project}")
        lines.append(f"\tAcquired by:   {self.station_metadata.acquired_by.author}")
        lines.append(f"\tAcquired date: {self.station_metadata.time_period.start_date}")
        lines.append(f"\tLatitude:      {self.station_metadata.location.latitude:.3f}")
        lines.append(f"\tLongitude:     {self.station_metadata.location.longitude:.3f}")
        lines.append(f"\tElevation:     {self.station_metadata.location.elevation:.3f}")
        if self.z is not None:
            if (self.z == 0).all():
                lines.append("\tImpedance:     False")
            else:
                lines.append("\tImpedance:     True")
        else:
            lines.append("\tImpedance:     False")

        if self.t is not None:
            if (self.t == 0).all():
                lines.append("\tTipper:        False")
            else:
                lines.append("\tTipper:        True")
        else:
            lines.append("\tTipper:        False")

        if self.frequency is not None:
            lines.append(f"\tNumber of periods: {self.frequency.size}")
            lines.append(
                f"\t\tPeriod Range:   {1./self.frequency.max():.5E} -- {1./self.frequency.min():.5E} s"
            )
            lines.append(
                f"\t\tFrequency Range {self.frequency.min():.5E} -- {self.frequency.max():.5E} s"
            )

        return "\n".join(lines)

    def __repr__(self):
        lines = []
        lines.append(f"station='{self.header.station}'")
        lines.append(f"latitude={self.header.latitude:.2f}")
        lines.append(f"longitude={self.header.longitude:.2f}")
        lines.append(f"elevation={self.header.elevation:.2f}")

        return f"JFile({(', ').join(lines)})"

    @property
    def fn(self):
        return self._jfn

    @fn.setter
    def fn(self, value):
        """
        set file name
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if value is None:
            return
        value = Path(value)
        if value.suffix in [".j"]:
            self._jfn = value
        else:
            msg = f"Input file must be a *.j file not {value.suffix}"
            self.logger.error(msg)
            raise ValueError(msg)

    @property
    def periods(self):
        return 1.0 / self.frequency

    def _validate_j_file(self):
        """
        change the lat, lon, elev lines to something machine readable,
        if they are not.
        """

        if not self.fn.exists():
            msg = f"Could not find {self.fn}, check path"
            self.logger.error(msg)
            raise NameError(msg)

        with open(self.fn, "r", errors="replace") as fid:
            j_lines = fid.readlines()

        for variable in ["lat", "lon", "elev"]:
            for ii, line in enumerate(j_lines):
                if variable in line.lower():
                    name = line.split("=")[0]
                    try:
                        value = float(line.split("=")[1].strip())
                    except ValueError:
                        value = 0.0
                        self.logger.debug(f"Changed {name[1:]} to 0.0")
                    j_lines[ii] = "{0} = {1}\n".format(name, value)
                    break

        return j_lines


    def read_j_file(self, fn=None):
        """
        read_j_file will read in a *.j file output by BIRRP (better than reading lots of *.<k>r<l>.rf files)

        Input:
        j-filename

        Output: 4-tuple
        - periods : N-array
        - Z_array : 2-tuple - values and errors
        - tipper_array : 2-tuple - values and errors
        - processing_dict : parsed processing parameters from j-file header

        """
        # read data
        z_index_dict = {"zxx": (0, 0), "zxy": (0, 1), "zyx": (1, 0), "zyy": (1, 1)}
        t_index_dict = {"tzx": (0, 0), "tzy": (0, 1)}

        if fn is not None:
            self.fn = fn

        self.logger.debug(f"Reading {self.fn}")

        j_line_list = self._validate_j_file()

        self.header.read_header(j_line_list)
        self.header.read_metadata(j_line_list)

        data_lines = [
            j_line for j_line in j_line_list if not ">" in j_line and not "#" in j_line
        ][:]

        self.header.station = data_lines[0].strip()

        # sometimes birrp outputs some missing periods, so the best way to deal with
        # this that I could come up with was to get things into dictionaries with
        # key words that are the period values, then fill in Z and T from there
        # leaving any missing values as 0

        # make empty dictionary that have keys as the component
        z_dict = dict([(z_key, {}) for z_key in list(z_index_dict.keys())])
        t_dict = dict([(t_key, {}) for t_key in list(t_index_dict.keys())])
        for d_line in data_lines[1:]:
            # check to see if we are at the beginning of a component block, if so
            # set the dictionary key to that value
            if "z" in d_line.lower():
                d_key = d_line.strip().split()[0].lower()
            # if we are at the number of periods line, skip it
            elif len(d_line.strip().split()) == 1 and "r" not in d_line.lower():
                continue
            elif "r" in d_line.lower():
                break
            # get the numbers into the correct dictionary with a key as period and
            # for now we will leave the numbers as a list, which we will parse later
            else:
                # split the line up into each number
                d_list = d_line.strip().split()

                # make a copy of the list to be sure we don't rewrite any values,
                # not sure if this is necessary at the moment
                d_value_list = list(d_list)
                for d_index, d_value in enumerate(d_list):
                    # check to see if the column number can be converted into a float
                    # if it can't, then it will be set to 0, which is assumed to be
                    # a masked number when writing to an .edi file

                    try:
                        d_value = float(d_value)
                        # need to check for masked points represented by
                        # birrp as -999, apparently
                        if d_value == -999 or np.isnan(d_value):
                            d_value_list[d_index] = 0.0
                        else:
                            d_value_list[d_index] = d_value
                    except ValueError:
                        d_value_list[d_index] = 0.0

                # put the numbers in the correct dictionary as:
                # key = period, value = [real, imaginary, error]
                if d_key in list(z_index_dict.keys()):
                    z_dict[d_key][d_value_list[0]] = d_value_list[1:4]
                elif d_key in list(t_index_dict.keys()):
                    t_dict[d_key][d_value_list[0]] = d_value_list[1:4]

        # --> now we need to get the set of periods for all components
        # check to see if there is any tipper data output

        all_periods = []
        for z_key in list(z_index_dict.keys()):
            for f_key in list(z_dict[z_key].keys()):
                all_periods.append(f_key)

        if len(list(t_dict["tzx"].keys())) == 0:
            self.logger.info(f"Could not find any Tipper data in {self.fn}")
            find_tipper = False

        else:
            for t_key in list(t_index_dict.keys()):
                for f_key in list(t_dict[t_key].keys()):
                    all_periods.append(f_key)
            find_tipper = True

        all_periods = np.array(sorted(list(set(all_periods))))
        all_periods = all_periods[np.nonzero(all_periods)]
        num_per = len(all_periods)

        # fill arrays using the period key from all_periods
        self.z = np.zeros((num_per, 2, 2), dtype=complex)
        self.z_err = np.zeros((num_per, 2, 2), dtype=float)

        self.t = np.zeros((num_per, 1, 2), dtype=complex)
        self.t_err = np.zeros((num_per, 1, 2), dtype=float)

        for p_index, per in enumerate(all_periods):
            for z_key in sorted(z_index_dict.keys()):
                kk = z_index_dict[z_key][0]
                ll = z_index_dict[z_key][1]
                try:
                    z_value = z_dict[z_key][per][0] + 1j * z_dict[z_key][per][1]
                    self.z[p_index, kk, ll] = z_value
                    self.z_err[p_index, kk, ll] = z_dict[z_key][per][2]
                except KeyError:
                    self.logger.debug(f"No value found for period {per:.4g}")
                    self.logger.debug(f"For component {z_key}")
            if find_tipper is True:
                for t_key in sorted(t_index_dict.keys()):
                    kk = t_index_dict[t_key][0]
                    ll = t_index_dict[t_key][1]
                    try:
                        t_value = t_dict[t_key][per][0] + 1j * t_dict[t_key][per][1]
                        self.t[p_index, kk, ll] = t_value
                        self.t_err[p_index, kk, ll] = t_dict[t_key][per][2]
                    except KeyError:
                        self.logger.debug(f"No value found for period {per:.4g}")
                        self.logger.debug(f"For component {t_key}")

        # put the results into mtpy objects
        self.frequency = 1.0 / all_periods
        self.z[np.where(self.z == np.inf)] = 0 + 0j
        self.t[np.where(self.t == np.inf)] = 0 + 0j
        self.z_err[np.where(self.z_err == np.inf)] = 10 ** 6
        self.t_err[np.where(self.t_err == np.inf)] = 10 ** 6


    @property
    def station_metadata(self):
        sm = Station()
        r1 = Run(id="001")

        if not np.all(self.z == 0):
            r1._ex.component = "ex"
            r1._ex.channel_id = 1
            
            r1._ey.component = "ey"
            r1._ey.channel_id = 1
            
            r1._hx.component = "hx"
            r1._hx.channel_id = 1
            
            r1._hy.component = "hy"
            r1._hy.channel_id = 1

        if not np.all(self.t == 0):
            r1._hz.component = "hz"
            r1._hz.channel_id = 5

        sm.runs.append(r1)
        sm.id = self.header.station
        sm.data_type = "MT"

        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude
        sm.location.elevation = self.header.elevation

        # provenance
        sm.provenance.software.name = "BIRRP"
        sm.provenance.software.version = "5"
        sm.transfer_function.processed_date = MTime(self.fn.stat().st_ctime).iso_str
        sm.transfer_function.runs_processed = sm.run_list
        # add birrp parameters
        for key, value in self.header.birrp_parameters.to_dict(single=True).items():
            sm.transfer_function.processing_parameters.append(f"{key} = {value}")

        return sm

    @property
    def survey_metadata(self):
        sm = Survey()

        return sm


def read_jfile(fn):
    """
    Read a .j file output by BIRRP

    :param fn: full path to j file
    :type fn: string or :class:`pathlib.Path`

    """

    from mt_metadata.transfer_functions.core import TF

    j_obj = JFile(fn)

    tf_obj = TF()
    tf_obj._fn = fn

    k_dict = OrderedDict(
        {
            "period": "periods",
            "impedance": "z",
            "tipper": "t",
            "survey_metadata": "survey_metadata",
            "station_metadata": "station_metadata",
        }
    )

    for tf_key, j_key in k_dict.items():
        setattr(tf_obj, tf_key, getattr(j_obj, j_key))

    return tf_obj


def write_jfile(tf_obj, fn=None):
    """

    :param mt_obj: DESCRIPTION
    :type mt_obj: TYPE
    :param fn: DESCRIPTION, defaults to None
    :type fn: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """

    raise IOError("write_jfile not implemented yet.")
