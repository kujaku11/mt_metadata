# -*- coding: utf-8 -*-
"""
.. py:module:: JFile
    :synopsis: Deal with J-Files of the format propsed by Alan Jones

.. codeauthor:: Jared Peacock <jpeacock@usgs.gov>

"""

# ==============================================================================
from pathlib import Path

import numpy as np
from loguru import logger

from mt_metadata.common.mttime import MTime
from mt_metadata.timeseries import Electric, Magnetic, Run, Survey
from mt_metadata.transfer_functions.io.tools import get_nm_elev
from mt_metadata.transfer_functions.tf import Station

from .metadata import Header


# ==============================================================================
# Class to read j_file
# ==============================================================================
class JFile:
    """
    be able to read and write a j-file
    """

    def __init__(self, fn: str | Path | None = None, **kwargs):
        self.header = Header()

        self._jfn = None
        self.fn = fn

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.frequency = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.fn is not None:
            self.read()

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
            logger.error(msg)
            raise ValueError(msg)

    @property
    def periods(self) -> None | np.typing.NDArray[np.float64]:
        if self.frequency is not None:
            return 1.0 / self.frequency

    def _validate_j_file(self) -> list[str]:
        """
        change the lat, lon, elev lines to something machine readable,
        if they are not.
        """
        if self.fn is not None:
            if not self.fn.exists():
                msg = f"Could not find {self.fn}, check path"
                logger.error(msg)
                raise NameError(msg)

        with open(str(self.fn), "r", errors="replace") as fid:
            j_lines = fid.readlines()

        for variable in ["lat", "lon", "elev"]:
            for ii, line in enumerate(j_lines):
                if variable in line.lower():
                    name = line.split("=")[0]
                    try:
                        value = float(line.split("=")[1].strip())
                    except ValueError:
                        value = 0.0
                        logger.debug(f"Changed {name[1:]} to 0.0")
                    j_lines[ii] = "{0} = {1}\n".format(name, value)
                    break

        return j_lines

    def read(self, fn: str | Path | None = None, get_elevation=False):
        """
        Read data from a j file

        parameters
        ----------
        fn : str | Path | None
            full path to j-file to read, defaults to None

        get_elevation : bool, optional
            if True, will try to get elevation from the NM elevation service,
            defaults to False

        Raises
        ------
        ValueError
            If the file is not found or cannot be opened.
        NameError
            If the file is not a valid j-file.

        Returns
        -------
        None
            Reads the data into the instance variables.

        """
        # read data
        z_index_dict = {
            "zxx": (0, 0),
            "zxy": (0, 1),
            "zyx": (1, 0),
            "zyy": (1, 1),
        }
        t_index_dict = {"tzx": (0, 0), "tzy": (0, 1)}

        if fn is not None:
            self.fn = fn

        logger.debug(f"Reading {self.fn}")

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
                            d_value_list[d_index] = "0.0"
                        else:
                            d_value_list[d_index] = str(d_value)
                    except ValueError:
                        d_value_list[d_index] = "0.0"

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
            logger.debug(f"Could not find any Tipper data in {self.fn}")
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
                    logger.debug(f"No value found for period {per:.4g}")
                    logger.debug(f"For component {z_key}")
            if find_tipper is True:
                for t_key in sorted(t_index_dict.keys()):
                    kk = t_index_dict[t_key][0]
                    ll = t_index_dict[t_key][1]
                    try:
                        t_value = t_dict[t_key][per][0] + 1j * t_dict[t_key][per][1]
                        self.t[p_index, kk, ll] = t_value
                        self.t_err[p_index, kk, ll] = t_dict[t_key][per][2]
                    except KeyError:
                        logger.debug(f"No value found for period {per:.4g}")
                        logger.debug(f"For component {t_key}")

        # put the results into mtpy objects
        self.frequency = 1.0 / all_periods
        self.z[np.where(self.z == np.inf)] = 0 + 0j
        self.t[np.where(self.t == np.inf)] = 0 + 0j
        self.z_err[np.where(self.z_err == np.inf)] = 10**6
        self.t_err[np.where(self.t_err == np.inf)] = 10**6

        if self.header.elevation == 0 and get_elevation:
            if self.header.latitude != 0 and self.header.longitude != 0:
                self.header.elevation = get_nm_elev(
                    self.header.latitude, self.header.longitude
                )

    @property
    def station_metadata(self):
        sm = Station()
        r1 = Run(id="001")
        if self.header.birrp_parameters.deltat < 0:
            r1.sample_rate = abs(self.header.birrp_parameters.deltat)
        else:
            r1.sample_rate = 1.0 / (self.header.birrp_parameters.deltat)

        if not np.all(self.z == 0):
            for ii, comp in enumerate(["ex", "ey", "hx", "hy"], 1):
                if comp.startswith("e"):
                    ch = Electric(component=comp, channel_id=ii)
                elif comp.startswith("h"):
                    ch = Magnetic(component=comp, channel_id=ii)
                r1.add_channel(ch)

        if not np.all(self.t == 0):
            ch = Magnetic(component="hz", channel_id=5)
            r1.add_channel(ch)

        sm.runs.append(r1)
        sm.id = self.header.station
        sm.data_type = "MT"

        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude
        sm.location.elevation = self.header.elevation

        # provenance
        sm.provenance.software.name = "BIRRP"
        sm.provenance.software.version = "5"
        sm.transfer_function.id = self.header.station
        if self.fn is not None:
            sm.transfer_function.processed_date = MTime(self.fn.stat().st_ctime).iso_str
        sm.transfer_function.runs_processed = sm.run_list
        # add birrp parameters
        for key, value in self.header.birrp_parameters.to_dict(single=True).items():
            sm.transfer_function.processing_parameters.append(f"{key} = {value}")

        return sm

    @property
    def survey_metadata(self):
        sm = Survey()
        sm.add_station(self.station_metadata)

        return sm
