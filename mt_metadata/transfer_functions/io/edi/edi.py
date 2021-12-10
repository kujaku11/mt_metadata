# -*- coding: utf-8 -*-
"""
.. module:: EDI
   :synopsis: Deal with EDI files.  The Edi class can read and write an .edi
             file, the 'standard format' of magnetotellurics.  Each section
             of the .edi file is given its own class, so the elements of each
             section are attributes for easy access.

.. moduleauthor:: Jared Peacock <jpeacock@usgs.gov>
"""

# ==============================================================================
#  Imports
# ==============================================================================
import numpy as np
from pathlib import Path
from collections import OrderedDict

from mt_metadata.transfer_functions.io.edi.metadata import (
    Header, Information, DefineMeasurement, DataSection)
from mt_metadata.transfer_functions import tf as metadata
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.transfer_functions.io.tools import (
    _validate_str_with_equals, index_locator, _validate_edi_lines)
from mt_metadata.utils.mttime import MTime
from mt_metadata import __version__

import scipy.stats.distributions as ssd

# ==============================================================================
# EDI Class
# ==============================================================================
class EDI(object):
    """
    This class is for .edi files, mainly reading and writing.  Has been tested
    on Winglink and Phoenix output .edi's, which are meant to follow the
    archaic EDI format put forward by SEG. Can read impedance, Tipper and/or
    spectra data.

    The Edi class contains a class for each major section of the .edi file.

    Frequency and components are ordered from highest to lowest frequency.

    :param fn: full path to .edi file to be read in.
                  *default* is None. If an .edi file is input, it is
                  automatically read in and attributes of Edi are filled
    :type fn: string

    ===================== =====================================================
    Methods               Description
    ===================== =====================================================
    read_edi_file         Reads in an edi file and populates the associated
                          classes and attributes.
    write_edi_file        Writes an .edi file following the EDI format given
                          the apporpriate attributes are filled.  Writes out
                          in impedance and Tipper format.
    _read_data            Reads in the impedance and Tipper blocks, if the
                          .edi file is in 'spectra' format, read_data converts
                          the data to impedance and Tipper.
    _read_mt              Reads impedance and tipper data from the appropriate
                          blocks of the .edi file.
    _read_spectra         Reads in spectra data and converts it to impedance
                          and Tipper data.
    ===================== =====================================================

    ===================== ========================================== ==========
    Attributes            Description                                default
    ===================== ========================================== ==========
    Data             DataSection class, contains basic
                          information on the data collected and in
                          whether the data is in impedance or
                          spectra.
    Measurement    DefineMeasurement class, contains
                          information on how the data was
                          collected.
    fn                full path to edi file read in              None
    Header                Header class, contains metadata on
                          where, when, and who collected the data
    Info                  Information class, contains information
                          on how the data was processed and how the
                          transfer functions where estimated.
    Tipper                mtpy.core.z.Tipper class, contains the
                          tipper data
    Z                     mtpy.core.z.Z class, contains the
                          impedance data
    _block_len            number of data in one line.                6
    _data_header_str      header string for each of the data         '>!****{0}****!'
                          section
    _num_format           string format of data.                     ' 15.6e'
    _t_labels             labels for tipper blocks
    _z_labels             labels for impedance blocks
    ===================== ========================================== ==========

    :Change Latitude: ::

        >>> import mtpy.core.edi as mtedi
        >>> edi_obj = mtedi.Edi(fn=r"/home/mt/mt01.edi")
        >>> # change the latitude
        >>> edi_obj.header.lat = 45.7869
        >>> new_edi_fn = edi_obj.write_edi_file()
    """

    def __init__(self, fn=None):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self._fn = None
        self._edi_lines = None

        self.Header = Header()
        self.Info = Information()
        self.Measurement = DefineMeasurement()
        self.Data = DataSection()

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.frequency = None
        self.rotation_angle = None
        self.residual_covariance = None
        self.signal_inverse_power = None

        self._z_labels = [
            ["zxxr", "zxxi", "zxx.var"],
            ["zxyr", "zxyi", "zxy.var"],
            ["zyxr", "zyxi", "zyx.var"],
            ["zyyr", "zyyi", "zyy.var"],
        ]

        self._t_labels = [
            ["txr.exp", "txi.exp", "txvar.exp"],
            ["tyr.exp", "tyi.exp", "tyvar.exp"],
        ]

        self._data_header_str = ">!****{0}****!\n"

        self._num_format = " 15.6e"
        self._block_len = 6

        self.fn = fn

    def __str__(self):
        lines = [f"Station: {self.station}", "-" * 50]
        lines.append(f"\tSurvey:        {self.survey_metadata.id}")
        lines.append(f"\tProject:       {self.survey_metadata.project}")
        lines.append(f"\tAcquired by:   {self.station_metadata.acquired_by.author}")
        lines.append(f"\tAcquired date: {self.station_metadata.time_period.start_date}")
        lines.append(f"\tLatitude:      {self.station_metadata.location.latitude:.3f}")
        lines.append(f"\tLongitude:     {self.station_metadata.location.longitude:.3f}")
        lines.append(f"\tElevation:     {self.station_metadata.location.elevation:.3f}")
        if self.z is not None:
            lines.append("\tImpedance:     True")
        else:
            lines.append("\tImpedance:     False")

        if self.t is not None:
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
        return self.__str__()

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, fn):
        if fn is not None:
            self._fn = Path(fn)
            if self._fn.exists():
                self.read()

    @property
    def period(self):
        if self.frequency is not None:
            return 1.0 / self.frequency
        return None

    def read(self, fn=None):
        """
        Read in an edi file and fill attributes of each section's classes.
        Including:
            * Header
            * Info
            * Measurement
            * Data
            * Z
            * Tipper

            .. note:: Automatically detects if data is in spectra format.  All
                  data read in is converted to impedance and Tipper.


        :param fn: full path to .edi file to be read in
                       *default* is None
        :type fn: string

        :Example: ::

            >>> import mtpy.core.Edi as mtedi
            >>> edi_obj = mtedi.Edi()
            >>> edi_obj.read_edi_file(fn=r"/home/mt/mt01.edi")

        """

        if fn is not None:
            self._fn = Path(fn)

        if self.fn is None:
            msg = "Must input EDI file to read"
            self.logger.error(msg)
            raise IOError(msg)

        if not self.fn.exists():
            msg = f"Cannot find EDI file: {self.fn}"
            self.logger.error(msg)
            raise IOError(msg)

        with open(self.fn, "r") as fid:
            self._edi_lines = _validate_edi_lines(fid.readlines())

        self.Header.read_header(self._edi_lines)
        self.Info.read_info(self._edi_lines)
        self.Measurement.read_measurement(self._edi_lines)
        self.Data.read_data(self._edi_lines)
        self.Data.match_channels(self.Measurement.channel_ids)

        self._read_data()

        if self.Header.lat is None:
            self.Header.lat = self.Measurement.reflat
            self.logger.debug(
                "Got latitude from reflat for {0}".format(self.Header.dataid)
            )
        if self.Header.lon is None:
            self.Header.lon = self.Measurement.reflon
            self.logger.debug(
                "Got longitude from reflon for {0}".format(self.Header.dataid)
            )
        if self.Header.elev is None:
            self.Header.elev = self.Measurement.refelev
            self.logger.debug(
                "Got elevation from refelev for {0}".format(self.Header.dataid)
            )

    def _read_data(self):
        """
        Read either impedance or spectra data depending on what the type is
        in the data section.
        """

        lines = self._edi_lines[self.Data._line_num:]

        if self.Data.data_type_in == "spectra":
            self.logger.debug("Converting Spectra to Impedance and Tipper")
            self.logger.debug(
                "Check to make sure input channel list is correct if the data looks incorrect"
            )
            if self.Data.nchan == 5:
                c_list = ["hx", "hy", "hz", "ex", "ey"]
            elif self.Data.nchan == 4:
                c_list = ["hx", "hy", "ex", "ey"]
            elif self.Data.nchan == 6:
                c_list = ["hx", "hy", "ex", "ey", "rhx", "rhy"]
            elif self.Data.nchan == 7:
                c_list = ["hx", "hy", "hz", "ex", "ey", "rhx", "rhy"]
            self._read_spectra(lines, comp_list=c_list)

        elif self.Data.data_type_in == "z":
            self._read_mt(lines)

    def _read_mt(self, data_lines):
        """
        Read in impedance and tipper data

        :param data_lines: list of data lines from the edi file
        :type data_lines: list
        """
        flip = False
        data_dict = {}
        data_find = False
        for line in data_lines:
            line = line.strip()
            if ">" in line and "!" not in line:
                line_list = line[1:].strip().split()
                if len(line_list) == 0:
                    continue
                key = line_list[0].lower()
                if key[0] == "z" or key[0] == "t" or key == "freq":
                    data_find = True
                    data_dict[key] = []
                else:
                    data_find = False

            elif data_find and ">" not in line and "!" not in line:
                d_lines = line.strip().split()
                for ii, dd in enumerate(d_lines):
                    # check for empty values and set them to 0, check for any
                    # other characters sometimes there are ****** for a null
                    # component
                    try:
                        d_lines[ii] = float(dd)
                        if d_lines[ii] == 1.0e32:
                            d_lines[ii] = 0.0
                    except ValueError:
                        d_lines[ii] = 0.0
                data_dict[key] += d_lines

        # fill useful arrays
        freq_arr = np.array(data_dict["freq"], dtype=float)
        self.z = np.zeros((freq_arr.size, 2, 2), dtype=complex)
        self.z_err = np.zeros((freq_arr.size, 2, 2), dtype=float)

        # fill impedance tensor
        if "zxxr" in data_dict.keys():
            self.z[:, 0, 0] = (
                np.array(data_dict["zxxr"]) + np.array(data_dict["zxxi"]) * 1j
            )
            self.z_err[:, 0, 0] = np.abs(np.array(data_dict["zxx.var"])) ** 0.5
        if "zxyr" in data_dict.keys():
            self.z[:, 0, 1] = (
                np.array(data_dict["zxyr"]) + np.array(data_dict["zxyi"]) * 1j
            )
            self.z_err[:, 0, 1] = np.abs(np.array(data_dict["zxy.var"])) ** 0.5
        if "zyxr" in data_dict.keys():
            self.z[:, 1, 0] = (
                np.array(data_dict["zyxr"]) + np.array(data_dict["zyxi"]) * 1j
            )
            self.z_err[:, 1, 0] = np.abs(np.array(data_dict["zyx.var"])) ** 0.5
        if "zyyr" in data_dict.keys():
            self.z[:, 1, 1] = (
                np.array(data_dict["zyyr"]) + np.array(data_dict["zyyi"]) * 1j
            )
            self.z_err[:, 1, 1] = np.abs(np.array(data_dict["zyy.var"])) ** 0.5

        # check for order of frequency, we want high togit  low
        if freq_arr[0] < freq_arr[1]:
            self.logger.debug(
                "Ordered arrays to be arranged from high to low frequency"
            )
            freq_arr = freq_arr[::-1]
            self.z = self.z[::-1]
            self.z_err = self.z_err[::-1]
            flip = True

        # set the attributes as private variables to avoid redundant estimation
        # of res and phase
        self.frequency = freq_arr
        self.z = self.z
        self.z_err = self.z_err

        try:
            self.rotation_angle = np.array(data_dict["zrot"])
        except KeyError:
            self.rotation_angle = np.zeros_like(freq_arr)

        # fill tipper data if there it exists
        self.t = np.zeros((freq_arr.size, 1, 2), dtype=complex)
        self.t_err = np.zeros((freq_arr.size, 1, 2), dtype=float)

        if "txr.exp" in list(data_dict.keys()):
            self.t[:, 0, 0] = (
                np.array(data_dict["txr.exp"]) + np.array(data_dict["txi.exp"]) * 1j
            )
            self.t[:, 0, 1] = (
                np.array(data_dict["tyr.exp"]) + np.array(data_dict["tyi.exp"]) * 1j
            )

            self.t_err[:, 0, 0] = np.abs(np.array(data_dict["txvar.exp"])) ** 0.5
            self.t_err[:, 0, 1] = np.abs(np.array(data_dict["tyvar.exp"])) ** 0.5

            if flip:
                self.t = self.t[::-1]
                self.t_err = self.t_err[::-1]

        else:
            self.logger.debug("Could not find any Tipper data.")


    def _read_spectra(
        self, data_lines, comp_list=["hx", "hy", "hz", "ex", "ey", "rhx", "rhy"]
    ):
        """
        Read in spectra data and convert to impedance and Tipper.

        :param data_lines: list of lines from edi file
        :type data_lines: list

        :param comp_list: list of components that correspond to the columns
                          of the spectra data.
        :type comp_list: list
        """

        data_dict = {}
        avgt_dict = {}
        data_find = False
        for line in data_lines:
            if line.lower().find(">spectra") == 0 and line.find("!") == -1:
                line_list = _validate_str_with_equals(line)
                data_find = True

                # frequency will be the key
                try:
                    key = float(
                        [
                            ss.split("=")[1]
                            for ss in line_list
                            if ss.lower().find("freq") == 0
                        ][0]
                    )
                    data_dict[key] = []
                    avgt = float(
                        [
                            ss.split("=")[1]
                            for ss in line_list
                            if ss.lower().find("avgt") == 0
                        ][0]
                    )
                    avgt_dict[key] = avgt
                except ValueError:
                    self.logger.debug("did not find frequency key")

            elif data_find and line.find(">") == -1 and line.find("!") == -1:
                data_dict[key] += [float(ll) for ll in line.strip().split()]

            elif line.find(">spectra") == -1:
                data_find = False

        # get an object that contains the indices for each component
        cc = index_locator(comp_list)
        print(cc)

        self.frequency = np.array(sorted(list(data_dict.keys()), reverse=True))

        self.z = np.zeros((len(list(data_dict.keys())), 2, 2), dtype=complex)
        self.t = np.zeros((len(list(data_dict.keys())), 1, 2), dtype=complex)

        self.z_err = np.zeros_like(self.z, dtype=float)
        self.t_err = np.zeros_like(self.t, dtype=float)

        for kk, key in enumerate(self.frequency):
            spectra_arr = np.reshape(
                np.array(data_dict[key]), (len(comp_list), len(comp_list))
            )

            # compute cross powers
            s_arr = np.zeros_like(spectra_arr, dtype=complex)
            for ii in range(s_arr.shape[0]):
                for jj in range(ii, s_arr.shape[0]):
                    if ii == jj:
                        s_arr[ii, jj] = spectra_arr[ii, jj]
                    else:
                        # minus sign for complex conjugation
                        # original spectra data are of form <A,B*>, but we need
                        # the order <B,A*>...
                        # this is achieved by complex conjugation of the
                        # original entries
                        s_arr[ii, jj] = complex(
                            spectra_arr[jj, ii], -spectra_arr[ii, jj]
                        )
                        # keep complex conjugated entries in the lower
                        # triangular matrix:
                        s_arr[jj, ii] = complex(
                            spectra_arr[jj, ii], spectra_arr[ii, jj]
                        )

            # use formulas from Bahr/Simpson to convert the Spectra into Z
            # the entries of S are sorted like
            # <X,X*>  <X,Y*>  <X,Z*>  <X,En*>  <X,Ee*>  <X,Rx*>  <X,Ry*>
            #         <Y,Y*>  <Y,Z*>  <Y,En*>  <Y,Ee*>  <Y,Rx*>  <Y,Ry*>
            # .....

            self.z[kk, 0, 0] = (
                s_arr[cc.ex, cc.rhx] * s_arr[cc.hy, cc.rhy]
                - s_arr[cc.ex, cc.rhy] * s_arr[cc.hy, cc.rhx]
            )
            self.z[kk, 0, 1] = (
                s_arr[cc.ex, cc.rhy] * s_arr[cc.hx, cc.rhx]
                - s_arr[cc.ex, cc.rhx] * s_arr[cc.hx, cc.rhy]
            )
            self.z[kk, 1, 0] = (
                s_arr[cc.ey, cc.rhx] * s_arr[cc.hy, cc.rhy]
                - s_arr[cc.ey, cc.rhy] * s_arr[cc.hy, cc.rhx]
            )
            self.z[kk, 1, 1] = (
                s_arr[cc.ey, cc.rhy] * s_arr[cc.hx, cc.rhx]
                - s_arr[cc.ey, cc.rhx] * s_arr[cc.hx, cc.rhy]
            )

            self.z[kk] /= (
                s_arr[cc.hx, cc.rhx] * s_arr[cc.hy, cc.rhy]
                - s_arr[cc.hx, cc.rhy] * s_arr[cc.hy, cc.rhx]
            )

            # compute error only if scipy package exists
            # 68% Quantil of the Fisher distribution:
            z_det = np.real(
                s_arr[cc.hx, cc.hx] * s_arr[cc.hy, cc.hy]
                - np.abs(s_arr[cc.hx, cc.hy] ** 2)
            )

            sigma_quantil = ssd.f.ppf(0.68, 4, avgt_dict[key] - 4)

            ## 1) Ex
            a = (
                s_arr[cc.ex, cc.hx] * s_arr[cc.hy, cc.hy]
                - s_arr[cc.ex, cc.hy] * s_arr[cc.hy, cc.hx]
            )
            b = (
                s_arr[cc.ex, cc.hy] * s_arr[cc.hx, cc.hx]
                - s_arr[cc.ex, cc.hx] * s_arr[cc.hx, cc.hy]
            )
            a /= z_det
            b /= z_det

            psi_squared = np.real(
                1.0
                / s_arr[cc.ex, cc.ex].real
                * (a * s_arr[cc.hx, cc.ex] + b * s_arr[cc.hy, cc.ex])
            )
            epsilon_squared = 1.0 - psi_squared

            scaling = (
                sigma_quantil
                * 4
                / (avgt_dict[key] - 4.0)
                * epsilon_squared
                / z_det
                * s_arr[cc.ex, cc.ex].real
            )
            self.z_err[kk, 0, 0] = np.sqrt(abs(scaling * s_arr[cc.hy, cc.hy].real))
            self.z_err[kk, 0, 1] = np.sqrt(abs(scaling * s_arr[cc.hx, cc.hx].real))

            # 2) EY
            a = (
                s_arr[cc.ey, cc.hx] * s_arr[cc.hy, cc.hy]
                - s_arr[cc.ey, cc.hy] * s_arr[cc.hy, cc.hx]
            )
            b = (
                s_arr[cc.ey, cc.hy] * s_arr[cc.hx, cc.hx]
                - s_arr[cc.ey, cc.hx] * s_arr[cc.hx, cc.hy]
            )
            a /= z_det
            b /= z_det

            psi_squared = np.real(
                1.0
                / np.real(s_arr[cc.ey, cc.ey])
                * (a * s_arr[cc.hx, cc.ey] + b * s_arr[cc.hy, cc.ey])
            )
            epsilon_squared = 1.0 - psi_squared

            scaling = (
                sigma_quantil
                * 4
                / (avgt_dict[key] - 4.0)
                * epsilon_squared
                / z_det
                * s_arr[cc.ey, cc.ey].real
            )
            self.z_err[kk, 1, 0] = np.sqrt(abs(scaling * s_arr[cc.hy, cc.hy].real))
            self.z_err[kk, 1, 1] = np.sqrt(abs(scaling * s_arr[cc.hx, cc.hx].real))

            # if HZ information is present:
            if len(comp_list) > 5:
                self.t[kk, 0, 0] = (
                    s_arr[cc.hz, cc.rhx] * s_arr[cc.hy, cc.rhy]
                    - s_arr[cc.hz, cc.rhy] * s_arr[cc.hy, cc.rhx]
                )
                self.t[kk, 0, 1] = (
                    s_arr[cc.hz, cc.rhy] * s_arr[cc.hx, cc.rhx]
                    - s_arr[cc.hz, cc.rhx] * s_arr[cc.hx, cc.rhy]
                )

                self.t[kk] /= (
                    s_arr[cc.hx, cc.rhx] * s_arr[cc.hy, cc.rhy]
                    - s_arr[cc.hx, cc.rhy] * s_arr[cc.hy, cc.rhx]
                )

                a = (
                    s_arr[cc.hz, cc.hx] * s_arr[cc.hy, cc.hy]
                    - s_arr[cc.hz, cc.hy] * s_arr[cc.hy, cc.hx]
                )
                b = (
                    s_arr[cc.hz, cc.hy] * s_arr[cc.hx, cc.hx]
                    - s_arr[cc.hz, cc.hx] * s_arr[cc.hx, cc.hy]
                )
                a /= z_det
                b /= z_det

                psi_squared = np.real(
                    1.0
                    / s_arr[cc.hz, cc.hz].real
                    * (a * s_arr[cc.hx, cc.hz] + b * s_arr[cc.hy, cc.hz])
                )
                epsilon_squared = 1.0 - psi_squared

                scaling = (
                    sigma_quantil
                    * 4
                    / (avgt_dict[key] - 4.0)
                    * epsilon_squared
                    / z_det
                    * s_arr[cc.hz, cc.hz].real
                )
                self.t_err[kk, 0, 0] = np.sqrt(abs(scaling * s_arr[cc.hy, cc.hy].real))
                self.t_err[kk, 0, 1] = np.sqrt(abs(scaling * s_arr[cc.hx, cc.hx].real))

        # check for nans
        self.z_err = np.nan_to_num(self.z_err)
        self.t_err = np.nan_to_num(self.t_err)

        self.z_err[np.where(self.z_err == 0.0)] = 1.0
        self.t_err[np.where(self.t_err == 0.0)] = 1.0

    def write(self, new_edi_fn=None, longitude_format="LON", latlon_format="dms"):
        """
        Write a new edi file from either an existing .edi file or from data
        input by the user into the attributes of Edi.


        :param new_edi_fn: full path to new edi file.
                           *default* is None, which will write to the same
                           file as the input .edi with as:
                           r"/home/mt/mt01_1.edi"
        :type new_edi_fn: string
        :param longitude_format:  whether to write longitude as LON or LONG.
                                  options are 'LON' or 'LONG', default 'LON'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns: full path to new edi file
        :rtype: string

        :Example: ::

            >>> import mtpy.core.edi as mtedi
            >>> edi_obj = mtedi.Edi(fn=r"/home/mt/mt01/edi")
            >>> edi_obj.Header.dataid = 'mt01_rr'
            >>> n_edi_fn = edi_obj.write_edi_file()
        """

        if new_edi_fn is None:
            if self.fn is not None:
                new_edi_fn = self.fn
            else:
                new_edi_fn = Path().cwd().joinpath(f"{self.Header.dataid}.edi")

        # write lines
        extra_lines = []
        if self.Header.progname != "mt_metadata":
            extra_lines.append(f"\toriginal_program.name={self.Header.progname}\n")
        if self.Header.progvers != __version__:
            extra_lines.append(f"\toriginal_program.version={self.Header.progvers}\n")
        if self.Header.progdate != "2021-12-01":
            extra_lines.append(f"\toriginal_program.date={self.Header.progdate}\n")
        if self.Header.fileby != "1980-01-01":
            extra_lines.append(f"\toriginal_file.date={self.Header.filedate}\n")
            
        
        header_lines = self.Header.write_header(
            longitude_format=longitude_format, latlon_format=latlon_format
        )
        
        info_lines = self.Info.write_info()
        info_lines.insert(1, "".join(extra_lines))
        
        define_lines = self.Measurement.write_measurement(
            longitude_format=longitude_format, latlon_format=latlon_format
        )
        
        self.Data.nfreq = len(self.frequency)
        dsect_lines = self.Data.write_data()

        # write out frequencies
        freq_lines = [self._data_header_str.format("frequencies".upper())]
        freq_lines += self._write_data_block(self.frequency, "freq")

        # write out rotation angles
        zrot_lines = [self._data_header_str.format("impedance rotation angles".upper())]
        if self.rotation_angle is None:
            self.rotation_angle = np.zeros(self.frequency.size)
        elif len(self.rotation_angle) != self.frequency.size:
            self.rotation_angle = np.repeat(self.rotation_angle[0], self.frequency.size)

        zrot_lines += self._write_data_block(self.rotation_angle, "zrot")

        # write out data only impedance and tipper
        z_data_lines = [self._data_header_str.format("impedances".upper())]
        self.z = np.nan_to_num(self.z)
        self.z_err = np.nan_to_num(self.z_err)
        self.t = np.nan_to_num(self.t)
        self.t_err = np.nan_to_num(self.t_err)
        if self.z is not None:
            for ii in range(2):
                for jj in range(2):
                    z_lines_real = self._write_data_block(
                        self.z[:, ii, jj].real, self._z_labels[2 * ii + jj][0]
                    )
                    z_lines_imag = self._write_data_block(
                        self.z[:, ii, jj].imag, self._z_labels[2 * ii + jj][1]
                    )
                    z_lines_var = self._write_data_block(
                        self.z_err[:, ii, jj] ** 2.0, self._z_labels[2 * ii + jj][2]
                    )
    
                    z_data_lines += z_lines_real
                    z_data_lines += z_lines_imag
                    z_data_lines += z_lines_var

        if self.t is None:
            trot_lines = [""]
            t_data_lines = [""]
        elif np.all(self.t == 0):
            trot_lines = [""]
            t_data_lines = [""]
        else:
            try:
                # write out rotation angles
                trot_lines = [
                    self._data_header_str.format("tipper rotation angles".upper())
                ]
                if isinstance(self.rotation_angle, float):
                    trot = np.repeat(self.rotation_angle, self.frequency.size)
                else:
                    trot = self.rotation_angle
                trot_lines += self._write_data_block(np.array(trot), "trot")

                # write out tipper lines
                t_data_lines = [self._data_header_str.format("tipper".upper())]
                for jj in range(2):
                    t_lines_real = self._write_data_block(
                        self.t[:, 0, jj].real, self._t_labels[jj][0]
                    )
                    t_lines_imag = self._write_data_block(
                        self.t[:, 0, jj].imag, self._t_labels[jj][1]
                    )
                    t_lines_var = self._write_data_block(
                        self.t_err[:, 0, jj] ** 2.0, self._t_labels[jj][2]
                    )

                    t_data_lines += t_lines_real
                    t_data_lines += t_lines_imag
                    t_data_lines += t_lines_var
            except AttributeError:
                trot_lines = [""]
                t_data_lines = [""]

        edi_lines = (
            header_lines
            + info_lines
            + define_lines
            + dsect_lines
            + freq_lines
            + zrot_lines
            + z_data_lines
            + trot_lines
            + t_data_lines
            + [">END"]
        )

        with open(new_edi_fn, "w") as fid:
            fid.write("".join(edi_lines))

        self.logger.info("Wrote {0}".format(new_edi_fn))
        return new_edi_fn

    def _write_data_block(self, data_comp_arr, data_key):
        """
        Write a data block

        :param data_comp_arr: array of data components
        :type data_comp_arr: np.ndarray

        :param data_key: the component to write out
        :type data_key: string

        :returns: list of lines to write to edi file
        :rtype: list
        """
        if data_key.lower().find("z") >= 0 and data_key.lower() not in ["zrot", "trot"]:
            block_lines = [
                ">{0} ROT=ZROT // {1:.0f}\n".format(
                    data_key.upper(), data_comp_arr.size
                )
            ]
        elif data_key.lower().find("t") >= 0 and data_key.lower() not in [
            "zrot",
            "trot",
        ]:
            block_lines = [
                ">{0} ROT=TROT // {1:.0f}\n".format(
                    data_key.upper(), data_comp_arr.size
                )
            ]
        elif data_key.lower() == "freq":
            block_lines = [
                ">{0} // {1:.0f}\n".format(data_key.upper(), data_comp_arr.size)
            ]

        elif data_key.lower() in ["zrot", "trot"]:
            block_lines = [
                ">{0} // {1:.0f}\n".format(data_key.upper(), data_comp_arr.size)
            ]

        else:
            raise ValueError("Cannot write block for {0}".format(data_key))

        for d_index, d_comp in enumerate(data_comp_arr, 1):
            if d_comp == 0.0 and data_key.lower() not in ["zrot", "trot"]:
                d_comp = float(self.Header.empty)
            # write the string in the specified format
            num_str = "{0:{1}}".format(d_comp, self._num_format)

            # check to see if a new line is needed
            if d_index % self._block_len == 0:
                num_str += "\n"
            # at the end of the block add a return
            if d_index == data_comp_arr.size:
                num_str += "\n"

            block_lines.append(num_str)

        return block_lines

    # -----------------------------------------------------------------------
    # set a few important properties
    # --> Latitude
    @property
    def lat(self):
        """latitude in decimal degrees"""
        return self.Header.lat

    @lat.setter
    def lat(self, input_lat):
        """set latitude and make sure it is converted to a float"""
        self.Header.lat = input_lat


    # --> Longitude
    @property
    def lon(self):
        """longitude in decimal degrees"""
        return self.Header.lon

    @lon.setter
    def lon(self, input_lon):
        """set latitude and make sure it is converted to a float"""
        self.Header.lon = input_lon

    # --> Elevation
    @property
    def elev(self):
        """Elevation in elevation units"""
        return self.Header.elev

    @elev.setter
    def elev(self, input_elev):
        """set elevation and make sure it is converted to a float"""
        self.Header.elev = input_elev

    # --> station
    @property
    def station(self):
        """station name"""
        if self.Header.dataid is not None:
            return self.Header.dataid.replace(r"/", "_")
        elif self.Measurement.refloc is not None:
            return self.Measurement.refloc.replace('"', "")
        elif self.Data.sectid is not None:
            return self.Data.sectid

    @station.setter
    def station(self, new_station):
        """station name"""
        if not isinstance(new_station, str):
            new_station = f"{new_station}".replace(r"/", "_")
        self.Header.dataid = new_station
        self.Data.sectid = new_station

    @property
    def survey_metadata(self):
        sm = metadata.Survey()
        sm.project = self.Header.project
        if sm.project is None:
            try:
                sm.project = self.Header.prospect
            except AttributeError:
                pass
        sm.id = self.Header.survey
        sm.acquired_by.author = self.Header.acqby
        sm.geographic_name = self.Header.loc
        sm.country = self.Header.country

        for key, value in self.Info.info_dict.items():
            if key is None:
                key = "extra"
            key = key.lower()
            if key in ["project"]:
                setattr(sm, key, value)
            if key in ["survey"]:
                sm.id = value

        return sm

    @survey_metadata.setter
    def survey_metadata(self, survey):
        """
        Update metadata from a survey metadata object

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if not isinstance(survey, metadata.Survey):
            raise TypeError(
                "Input must be a mt_metadata.transfer_function.Survey object"
                f" not {type(survey)}"
            )

        self.Header.survey = survey.id
        self.Header.project = survey.project
        self.Header.loc = survey.geographic_name
        self.Header.country = survey.country

    @property
    def station_metadata(self):
        sm = metadata.Station()
        sm.runs.append(metadata.Run(id=f"{self.station}a"))
        sm.id = self.station
        sm.data_type = "MT"
        sm.channels_recorded = self.Measurement.channels_recorded
        # location
        sm.location.latitude = self.lat
        sm.location.longitude = self.lon
        sm.location.elevation = self.elev
        sm.location.datum = self.Header.datum
        sm.location.declination.value = self.Header.declination.value
        sm.orientation.reference_frame = self.Header.coordinate_system.split()[0]
        # provenance
        sm.acquired_by.author = self.Header.acqby
        sm.provenance.creation_time = self.Header.filedate
        sm.provenance.submitter.author = self.Header.fileby
        sm.provenance.software.name = self.Header.fileby
        sm.provenance.software.version = self.Header.progvers
        sm.transfer_function.processed_date = self.Header.filedate
        sm.transfer_function.runs_processed = sm.run_list

        for key, value in self.Info.info_dict.items():
            if key is None:
                continue
            if "provenance" in key:
                sm.set_attr_from_name(key, value)

        # dates
        if self.Header.acqdate is not None:
            sm.time_period.start = self.Header.acqdate

        # processing information
        for key, value in self.Info.info_dict.items():
            if key is None:
                continue
            key = key.lower()
            if "transfer_function" in key:
                key = key.split("transfer_function.")[1]
                sm.transfer_function.set_attr_from_name(key, value)
            if "processing." in key:
                key = key.split("processing.")[1]
                if key in ["software"]:
                    sm.transfer_function.software.name = value
                elif key in ["tag"]:
                    if value.count(",") > 0:
                        sm.transfer_function.remote_references = value.split(",")
                    else:
                        sm.transfer_function.remote_references = value.split()

            elif key in ["processedby", "processed_by"]:
                sm.transfer_function.processed_by.author = value

            elif key in ["runlist", "run_list"]:
                if value.count(",") > 0:
                    runs = value.split(",")
                else:
                    runs = value.split()
                sm.run_list = []
                for rr in runs:
                    sm.run_list.append(metadata.Run(id=rr))
                sm.transfer_function.runs_processed = runs

            elif key == "sitename":
                sm.geographic_name = value
            elif key == "signconvention":
                sm.transfer_function.sign_convention = value
            if "mtft" in key or "emtf" in key or "mtedit" in key:
                sm.transfer_function.processing_parameters.append(f"{key}={value}")

            if "provenance" in key:
                sm.set_attr_from_name(key, value)

        if self.Header.filedate is not None:
            sm.transfer_function.processed_date = self.Header.filedate

        # make any extra information in info list into a comment
        sm.comments = "\n".join(self.Info.info_list)

        # add information to runs
        for rr in sm.runs:
            rr.ex = self.ex_metadata
            rr.ey = self.ey_metadata
            rr.hx = self.hx_metadata
            rr.hy = self.hy_metadata
            if self.hz_metadata.component in ["hz"]:
                rr.hz = self.hz_metadata
            if self.rrhx_metadata.component in ["rrhx"]:
                rr.rrhx = self.rrhx_metadata
            if self.rrhy_metadata.component in ["rrhy"]:
                rr.rrhy = self.rrhy_metadata

        return sm

    @station_metadata.setter
    def station_metadata(self, sm):
        """
        Set EDI metadata from station metadata object

        :param sm: Station object to pull metadata from
        :type sm: :class:`mt_metadata.transfer_functions.tf.Station`

        """

        ### fill header information from station
        self.Header.acqby = sm.acquired_by.author
        self.Header.acqdate = sm.time_period.start_date
        self.Header.coordinate_system = sm.orientation.reference_frame
        self.Header.dataid = sm.id
        self.Header.declination = sm.location.declination.value
        self.Header.elev = sm.location.elevation
        self.Header.fileby = sm.provenance.submitter.author
        self.Header.filedate = sm.provenance.creation_time
        self.Header.lat = sm.location.latitude
        self.Header.lon = sm.location.longitude
        self.Header.datum = sm.location.datum
        self.Header.units = sm.transfer_function.units

        ### write notes
        # write comments, which would be anything in the info section from an edi
        if isinstance(sm.comments, str):
            self.Info.info_list += sm.comments.split("\n")
        # write transfer function info first
        for k, v in sm.transfer_function.to_dict(single=True).items():
            if not v in [None]:
                if k in ["processing_parameters"]:
                    for item in v:
                        self.Info.info_list.append(
                            f"processing_parameters.{item.replace('=', ' = ')}"
                        )
                else:
                    self.Info.info_list.append(f"transfer_function.{k} = {v}")

        # write provenance
        for k, v in sm.provenance.to_dict(single=True).items():
            if not v in [None, "None", "null"]:
                self.Info.info_list.append(f"provenance.{k} = {v}")

        # write field notes
        for run in sm.runs:
            write_dict = dict(
                [
                    (comp, False)
                    for comp in [
                        "ex",
                        "ey",
                        "hx",
                        "hy",
                        "hz",
                        "temperature",
                        "rrhx",
                        "rrhy",
                    ]
                ]
            )
            for cc in write_dict.keys():
                if getattr(run, cc).component is not None:
                    write_dict[cc] = True

            r_dict = run.to_dict(single=True)

            for rk, rv in r_dict.items():
                if rv in [None, "1980-01-01T00:00:00+00:00"]:
                    continue
                if rk[0:2] in ["ex", "ey", "hx", "hy", "hz", "te", "rr"]:
                    if rk[0:2] == "te":
                        comp = "temperature"
                    elif rk[0:2] == "rr":
                        comp = rk[0:4]
                    else:
                        comp = rk[0:2]
                    if write_dict[comp] is False:
                        continue
                    skip_list = [
                        f"{comp}.{ff}"
                        for ff in [
                            "filter.name",
                            "filter.applied",
                            "time_period.start",
                            "time_period.end",
                            "location.elevation",
                            "location.latitude",
                            "location.longitude",
                            "location.x",
                            "location.y",
                            "location.z",
                            "positive.latitude",
                            "positive.longitude",
                            "positive.elevation",
                            "positive.x",
                            "positive.x2",
                            "positive.y",
                            "positive.y2",
                            "positive.z",
                            "positive.z2",
                            "negative.latitude",
                            "negative.longitude",
                            "negative.elevation",
                            "negative.x",
                            "negative.x2",
                            "negative.y",
                            "negative.y2",
                            "negative.z",
                            "negative.z2",
                            "sample_rate",
                            "data_quality.rating.value",
                            "data_quality.flag",
                        ]
                    ]

                    if rk not in skip_list:
                        self.Info.info_list.append(f"{run.id}.{rk} = {rv}")
                else:
                    self.Info.info_list.append(f"{run.id}.{rk} = {rv}")

        ### fill measurement
        self.Measurement.refelev = sm.location.elevation
        self.Measurement.reflat = sm.location.latitude
        self.Measurement.reflon = sm.location.longitude
        self.Measurement.maxchan = len(sm.channels_recorded)
        if len(sm.channels_recorded) > 0:
            for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
                try:
                    self.Measurement.from_metadata(getattr(sm.runs[0], f"{comp}"))
                except AttributeError as error:
                    self.logger.info(error)
                    self.logger.debug(f"Did not find information on {comp}")

    def _get_electric_metadata(self, comp):
        """
        get electric information from the various metadata
        """
        comp = comp.lower()
        electric = metadata.Electric()
        electric.positive.type = "electric"
        electric.negative.type = "electric"
        if hasattr(self.Measurement, f"meas_{comp}"):
            meas = getattr(self.Measurement, f"meas_{comp}")
            electric.dipole_length = meas.dipole_length
            electric.channel_id = meas.id
            electric.measurement_azimuth = meas.azimuth
            electric.translated_azimuth = meas.azimuth
            electric.component = meas.chtype
            electric.channel_number = meas.channel_number
            electric.negative.x = meas.x
            electric.positive.x2 = meas.x2
            electric.negative.y = meas.y
            electric.positive.y2 = meas.y2
            for k, v in self.Info.info_dict.items():
                if k is None:
                    continue
                if f"{comp}." in k:
                    key = k.split(f"{comp}.")[1].strip()
                    if key == "manufacturer":
                        electric.negative.manufacturer = v
                        electric.positive.manufacturer = v
                    if key == "type":
                        electric.negative.type = v
                        electric.positive.type = v

            if (
                electric.positive.x2 == 0
                and electric.positive.y2 == 0.0
                and electric.negative.x == 0
                and electric.negative.y == 0.0
            ):
                electric.positive.x2 = electric.dipole_length * np.cos(
                    np.deg2rad(meas.azimuth)
                )
                electric.positive.y2 = electric.dipole_length * np.sin(
                    np.deg2rad(meas.azimuth)
                )

            for key, value in self.Info.info_dict.items():
                if key is None:
                    continue
                if f".{comp}." in key:
                    key = key.split(f".{comp}.", 1)[-1]
                    electric.set_attr_from_name(key, value)

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

        magnetic = metadata.Magnetic()
        magnetic.sensor.type = "magnetic"
        if hasattr(self.Measurement, f"meas_{comp}"):
            meas = getattr(self.Measurement, f"meas_{comp}")
            magnetic.measurement_azimuth = meas.azm
            magnetic.translated_azimuth = meas.azm
            magnetic.component = meas.chtype
            magnetic.channel_number = meas.channel_number
            magnetic.channel_id = meas.id
            magnetic.location.x = meas.x
            magnetic.location.y = meas.y
            try:
                magnetic.sensor.id = meas.meas_magnetic.sensor
            except AttributeError:
                pass
            for k, v in self.Info.info_dict.items():
                if k is None:
                    continue
                if f"{comp}." in k:
                    key = k.split(f"{comp}.")[1].strip()
                    if key == "manufacturer":
                        magnetic.sensor.manufacturer = v
                    if key == "type":
                        magnetic.sensor.type = v

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

    @property
    def rrhx_metadata(self):
        return self._get_magnetic_metadata("rrhx")

    @property
    def rrhy_metadata(self):
        return self._get_magnetic_metadata("rrhy")


# =============================================================================
#  Generic read and write
# =============================================================================
def read_edi(fn):
    """

    Read an edi file and return a :class:`mtpy.core.mt.MT` object

    :param fn: DESCRIPTION
    :type fn: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    # need to add this here instead of the top is because of recursive
    # importing.  This may not be the best way to do this but works for now
    # so we don't have to break how MTpy structure is setup now.
    from mt_metadata.transfer_functions.core import TF

    st = MTime().now()

    edi_obj = EDI()
    edi_obj.read(fn)

    tf_obj = TF()
    tf_obj._fn = fn

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
        setattr(tf_obj, tf_key, getattr(edi_obj, edi_key))

    # need to set latitude to compute UTM coordinates to make sure station
    # location is estimated for ModEM
    tf_obj.latitude = edi_obj.station_metadata.location.latitude

    et = MTime().now()
    tf_obj.logger.debug(
        f"Reading EDI for {tf_obj.station} and conversion to MT took {et - st:.2f} seconds"
    )

    return tf_obj


def write_edi(tf_object, fn=None):
    """
    Write an edi file from an :class:`mtpy.core.mt.MT` object

    :param tf_object: DESCRIPTION
    :type tf_object: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    from mt_metadata.transfer_functions.core import TF

    if not isinstance(tf_object, TF):
        raise ValueError("Input must be an mt_metadata.transfer_functions.core object")

    edi_obj = EDI()
    if tf_object.has_impedance():
        edi_obj.z = tf_object.impedance.data
        edi_obj.z_err = tf_object.impedance_error.data
    if tf_object.has_tipper():
        edi_obj.t = tf_object.tipper.data
        edi_obj.t_err = tf_object.tipper_error.data
    edi_obj.frequency = 1.0 / tf_object.period

    # fill from survey metadata
    edi_obj.survey_metadata = tf_object.survey_metadata

    # fill from station metadata
    edi_obj.station_metadata = tf_object.station_metadata

    # input data section
    edi_obj.Data.data_type = tf_object.station_metadata.data_type
    edi_obj.Data.nfreq = tf_object.period.size
    edi_obj.Data.sectid = tf_object.station
    edi_obj.Data.nchan = len(edi_obj.Measurement.channel_ids.keys())

    edi_obj.Data.maxblks = 999
    for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
        if hasattr(edi_obj.Measurement, f"meas_{comp}"):
            setattr(edi_obj.Data, comp, getattr(edi_obj.Measurement, f"meas_{comp}").id)

    new_edi_fn = edi_obj.write(new_edi_fn=fn)
    edi_obj._fn = new_edi_fn

    return edi_obj
