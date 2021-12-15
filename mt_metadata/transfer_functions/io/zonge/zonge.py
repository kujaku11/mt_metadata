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

from .metadata import Header
from mt_metadata.transfer_functions.tf import Survey, Station, Run

# ==============================================================================
# deal with avg files output from mtedit
# ==============================================================================
class ZongeMTAvg:
    """
    deal with avg files output from mtedit and makes an .edi file.
    
    
    =============================== ===========================================
    Attributes                       Description     
    =============================== ===========================================
     MTEdit3Auto_PhaseFlip          [ yes | no ] flip phase automatically
     MTEdit3DPlus_Use               [ yes | no ] use D+ smoothing
     MTEdit3PhaseSlope_Smooth       [ yes | no ] smooth data using phase
     MTEdit3PhaseSlope_toMag        [ yes | no ] use phase to predict mag
     MTEdit3Version                 version of mtedit
     Rx_GdpStn                      station name
     Rx_HPR                         station rotation (N, E, Z)
     Rx_Length                      dipole lenghts
     Survey_Array                   survey array
     Survey_Type                    survey type (MT)
     Tipper                         mtpy.core.z.Tipper object
     Tx_Type                        Transmitter type
     Unit_Length                    units of length (m) 
     Z                              mtpy.core.z.Z object
     avg_dict                       dictionary of all meta data for MTAvg 
     comp                           components
     comp_dict                      dictionary of components
     comp_flag                      component flag
     comp_index                     index of component
     comp_lst_tip                   list of tipper information
     comp_lst_z                     list of z information
     freq_dict                      dictionary of frequencies
     freq_dict_x                    dictionary of frequencies in x direction
     freq_dict_y                    dictionary of frequencies in y direction
     header_dict                    dictionary of header information
     info_dtype                     numpy.dtype for information 
     info_keys                      keys for information
     info_type                      keys type
     nfreq                          number of frequencies
     nfreq_tipper                   number of frequencies for tipper
     z_coordinate                   coordinate of z
    =============================== ===========================================
    
    =============================== ===========================================
    Methods                         Description
    =============================== ===========================================
    convert2complex                 convert res/phase to Z          
    fill_Tipper                     fill tipper data in to Tipper             
    fill_Z                          fill z data to Z
    read_avg_file                   read in .avg file output by MTEdit 
    write_edi                       write .edi from .avg file   
    =============================== ===========================================
    
    
    :Example: ::
        
        >>> import mtpy.usgs.zonge as zonge
        >>> zm = zonge.ZongeMTAvg(r"/home/mt01/Merged"\
                                  'mt01', \
                                  survey_cfg_file=r"/home/mt/survey.cfg",\
                                  mtft_cfg_file=r"/home/mt/mt01/Merged/mtft24.cfg"\,
                                  mtedit_cfg_file=r"/home/bin/mtedit.cfg",\
                                  copy_path=r"/home/mt/edi_files")
    """

    def __init__(self, fn=None):

        self.header = Header()

        self.info_keys = [
            "Skp",
            "Freq",
            "E.mag",
            "B.mag",
            "Z.mag",
            "Z.phz",
            "ARes.mag",
            "ARes.%err",
            "Z.perr",
            "Coher",
            "FC.NUse",
            "FC.NTry",
        ]
        self.info_type = [
            int,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            int,
            int,
        ]

        self.info_fmt = [
            "<1.0f",
            "<.4g",
            "<.4e",
            "<.4e",
            "<.4e",
            "<.1f",
            "<.4e",
            "<.1f",
            "<.1f",
            "<.3f",
            "<.0f",
            "<.0f",
        ]

        self.info_dtype = np.dtype(
            [(kk.lower(), tt) for kk, tt in zip(self.info_keys, self.info_type)]
        )

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.comp_lst_z = ["zxx", "zxy", "zyx", "zyy"]
        self.comp_lst_tip = ["tzx", "tzy"]
        self.comp_index = {
            "zxx": (0, 0),
            "zxy": (0, 1),
            "zyx": (1, 0),
            "zyy": (1, 1),
            "tzx": (0, 0),
            "tzy": (0, 1),
        }
        self.comp_flag = {
            "zxx": False,
            "zxy": False,
            "zyx": False,
            "zyy": False,
            "tzx": False,
            "tzy": False,
        }
        self.comp_dict = None
        self.comp = None
        self.nfreq = None
        self.nfreq_tipper = None
        self.freq_dict = None
        self.freq_dict_x = None
        self.freq_dict_y = None
        self.z_coordinate = "down"

        self.fn = fn

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, value):
        if value is not None:
            self._fn = Path(value)
            if self._fn.exists():
                self.read_avg_file()
        else:
            self._fn = None

    def get_comp_dict(self, lines):
        """
        Get the component dictionary from the file

        :param lines: DESCRIPTION
        :type lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        avg_str = "".join(lines)

        index_0 = avg_str.find("$")
        index_1 = avg_str.find("$", index_0 + 1)

        n_values = int(round((index_1 - index_0) / index_0))

        return self._make_comp_dict(n_values)

    def _make_comp_dict(self, n_values):
        """ """

        return dict(
            [
                (ckey, np.zeros(n_values, dtype=self.info_dtype))
                for ckey in list(self.comp_flag.keys())
            ]
        )

    def read_avg_file(self, fn=None):
        """
        read in average file
        """

        if fn is not None:
            self._fn = Path(fn)
        self.comp = self.fn.stem[0]
        with open(self.fn, "r") as fid:
            alines = fid.readlines()

        # read header
        alines = self.header.read_header(alines)

        self.comp_flag = {
            "zxx": False,
            "zxy": False,
            "zyx": False,
            "zyy": False,
            "tzx": False,
            "tzy": False,
        }

        if not self.comp_dict:
            self.comp_dict = self.get_comp_dict(alines)

        self.comp_lst_z = []
        self.comp_lst_tip = []
        ii = 0
        for aline in alines[1:]:
            if aline.find("=") > 0 and aline.find("$") == 0:
                alst = [aa.strip() for aa in aline.strip().split("=")]
                if alst[1].lower() in list(self.comp_flag.keys()):
                    akey = alst[1].lower()
                    self.comp_flag[akey] = True
                    if akey[0] == "z":
                        self.comp_lst_z.append(akey)
                    elif akey[0] == "t":
                        self.comp_lst_tip.append(akey)
                    ii = 0

            # read the data line.
            elif len(aline) > 2:
                aline = aline.replace("*", "0.50")
                alst = [aa.strip() for aa in aline.strip().split(",")]
                for cc, ckey in enumerate(self.info_keys):
                    self.comp_dict[akey][ii][ckey.lower()] = alst[cc]
                ii += 1

        self._fill_z()
        self._fill_t()

        self.header.logger.info("Read file {0}".format(self.fn))

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
        zmag = np.sqrt(zreal ** 2 + zimag ** 2)

        return zmag, zphase

    def _match_freq(self, freq_list1, freq_list2):
        """
        fill the frequency dictionary where keys are freqeuency and
        values are index of where that frequency should be in the array of z
        and tipper
        """

        comb_freq_list = list(set(freq_list1).intersection(freq_list2)) + list(
            set(freq_list1).symmetric_difference(freq_list2)
        )
        comb_freq_list.sort()

        return dict([(freq, ff) for ff, freq in enumerate(comb_freq_list)])

    def _fill_z(self):
        """
        create Z array with data
        """
        flst = np.array(
            [
                len(np.nonzero(self.comp_dict[comp]["freq"])[0])
                for comp in self.comp_lst_z
            ]
        )

        nz = flst.max()
        freq = self.comp_dict[self.comp_lst_z[np.where(flst == nz)[0][0]]]["freq"]
        freq = freq[np.nonzero(freq)]

        if self.nfreq:
            self.freq_dict_y = dict([(ff, nn) for nn, ff in enumerate(freq)])
            # get new frequency dictionary to match index values
            new_freq_dict = self._match_freq(sorted(self.freq_dict_x.keys()), freq)

            new_nz = len(list(new_freq_dict.keys()))
            self.freq_dict = new_freq_dict
            # fill z according to index values
            self.frequency = sorted(new_freq_dict.keys())
            self.z = np.zeros((new_nz, 2, 2), dtype=complex)
            self.z_err = np.ones((new_nz, 2, 2))
            nzx, nzy, nzz = self.z.shape

            # need to fill the new array with the old values, but they
            # need to be stored in the correct position
            clst = ["zxx", "zxy", "zyx", "zyy"]
            for cc in self.comp_lst_z:
                clst.remove(cc)
            for ikey in clst:
                for kk, zz in enumerate(self.Z.z):
                    ii, jj = self.comp_index[ikey]
                    if zz[ii, jj].real != 0.0:
                        # index for new Z array
                        ll = self.freq_dict[self.comp_dict[ikey]["freq"][kk]]

                        # index for old Z array
                        try:
                            mm = self.freq_dict_x[self.comp_dict[ikey]["freq"][kk]]

                            self.z[ll] = self.z[mm]
                            self.z_err[ll] = self.z_err[mm]
                        except KeyError:
                            pass

            # fill z with values from comp_dict
            for ikey in self.comp_lst_z:
                ii, jj = self.comp_index[ikey]

                zr, zi = self.to_complex(
                    self.comp_dict[ikey]["z.mag"][:nz].copy(),
                    self.comp_dict[ikey]["z.phz"][:nz].copy(),
                )
                for kk, zzr, zzi in zip(list(range(len(zr))), zr, zi):
                    ll = self.freq_dict[self.comp_dict[ikey]["freq"][kk]]
                    if ikey.find("yx") > 0 and self.z_coordinate == "up":
                        self.z[ll, ii, jj] = -1 * (zzr + zzi * 1j)
                    else:
                        self.z[ll, ii, jj] = zzr + zzi * 1j
                    self.z_err[ll, ii, jj] = (
                        self.comp_dict[ikey]["ares.%err"][kk] * 0.005
                    )

        # fill for the first time
        else:
            self.nfreq = nz
            self.freq_dict_x = dict([(ff, nn) for nn, ff in enumerate(freq)])
            # fill z with values
            z = np.zeros((nz, 2, 2), dtype="complex")
            z_err = np.ones((nz, 2, 2))

            for ikey in self.comp_lst_z:
                ii, jj = self.comp_index[ikey]

                zr, zi = self.to_complex(
                    self.comp_dict[ikey]["z.mag"][:nz].copy(),
                    self.comp_dict[ikey]["z.phz"][:nz].copy(),
                )

                if ikey.find("yx") > 0 and self.z_coordinate == "up":
                    z[:, ii, jj] = -1 * (zr + zi * 1j)
                else:
                    z[:, ii, jj] = zr + zi * 1j

                z_err[:, ii, jj] = self.comp_dict[ikey]["ares.%err"][:nz] * 0.005

            self.frequency = freq
            self.z = z
            self.z_err = z_err

        self.z = np.nan_to_num(self.z)
        self.z_err = np.nan_to_num(self.z_err)

    def _fill_t(self):
        """
        fill tipper values
        """

        if self.comp_flag["tzy"] == False and self.comp_flag["tzx"] == False:
            self.header.logger.debug("No Tipper found in %s", self.fn.name)
            return

        flst = np.array(
            [
                len(np.nonzero(self.comp_dict[comp]["freq"])[0])
                for comp in self.comp_lst_tip
            ]
        )
        nz = flst.max()
        freq = self.comp_dict[self.comp_lst_tip[np.where(flst == nz)[0][0]]]["freq"]
        freq = freq[np.nonzero(freq)]
        if self.nfreq_tipper and self.Tipper.tipper is not None:
            # get new frequency dictionary to match index values
            new_freq_dict = self._match_freq(sorted(self.freq_dict.keys()), freq)

            new_nz = len(list(new_freq_dict.keys()))
            # fill z according to index values
            self.tipper = np.zeros((new_nz, 1, 2), dtype=complex)
            self.tipper_err = np.ones((new_nz, 1, 2))

            self.freq_dict = new_freq_dict

            # need to fill the new array with the old values, but they
            # need to be stored in the correct position
            for ikey in ["tzx", "tzy"]:
                for kk, tt in enumerate(self.Tipper.tipper):
                    ii, jj = self.comp_index[ikey]
                    if tt[ii, jj].real != 0.0:
                        # index for new tipper array
                        ll = self.freq_dict[self.comp_dict[ikey]["freq"][kk]]

                        # index for old tipper array
                        try:
                            mm = self.freq_dict_x[self.comp_dict[ikey]["freq"][kk]]

                            self.tipper[ll] = self.tipper[mm]
                            self.tipper_err[ll] = self.tipper_err[mm]
                        except KeyError:
                            pass

            # fill z with values from comp_dict
            for ikey in self.comp_lst_tip:
                ii, jj = self.comp_index[ikey]

                tr, ti = self.to_complex(
                    self.comp_dict[ikey]["z.mag"][:nz],
                    self.comp_dict[ikey]["z.phz"][:nz],
                )
                for kk, tzr, tzi in zip(list(range(len(tr))), tr, ti):
                    ll = self.freq_dict[self.comp_dict[ikey]["freq"][kk]]

                    if self.z_coordinate == "up":
                        self.tipper[ll, ii, jj] = -1 * (tzr + tzi * 1j)
                    else:
                        self.tipper[ll, ii, jj] = tzr + tzi * 1j
                    # error estimation
                    self.tipper_err[ll, ii, jj] += (
                        self.comp_dict[ikey]["ares.%err"][kk]
                        * 0.05
                        * np.sqrt(tzr ** 2 + tzi ** 2)
                    )

        else:
            self.nfreq_tipper = nz
            self.freq_dict_x = dict([(ff, nn) for nn, ff in enumerate(freq)])
            # fill z with values
            tipper = np.zeros((nz, 1, 2), dtype="complex")
            tipper_err = np.ones((nz, 1, 2))

            for ikey in self.comp_lst_tip:
                ii, jj = self.comp_index[ikey]

                tzr, tzi = self.to_complex(
                    self.comp_dict[ikey]["z.mag"][:nz],
                    self.comp_dict[ikey]["z.phz"][:nz],
                )

                if self.z_coordinate == "up":
                    tipper[:, ii, jj] = -1 * (tzr + tzi * 1j)
                else:
                    tipper[:, ii, jj] = tzr + tzi * 1j
                tipper_err[:, ii, jj] = (
                    self.comp_dict[ikey]["ares.%err"][:nz]
                    * 0.05
                    * np.sqrt(tzr ** 2 + tzi ** 2)
                )

            self.frequency = sorted(self.freq_dict_x.keys())
            self.tipper = tipper
            self.tipper_err = tipper_err

        self.tipper = np.nan_to_num(self.tipper)
        self.tipper_err = np.nan_to_num(self.tipper_err)

    @property
    def station_metadata(self):
        sm = Station()

        sm.id = self.header.station
        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude

        sm.transfer_function.software.author = "Zonge International"
        sm.transfer_function.software.name = "MTEdit"
        sm.transfer_function.software.version = self.header.m_t_edit.version.split()[0]
        sm.transfer_function.software.last_updated = (
            self.header.m_t_edit.version.split()[-1]
        )

        for key, value in self.header.m_t_edit.to_dict(single=True).items():
            if "version" in key:
                continue
            sm.transfer_function.processing_parameters.append(f"mtedit.{key}={value}")

        sm.data_type = self.header.survey.type
        sm.runs.append(Run(id="001"))
        for comp in self.comp_lst_z + self.comp_lst_tip:
            if "zx" in comp:
                sm.runs[0]._ex.component = "ex"
                sm.runs[0]._ex.dipole_length = self.header.rx.length
                sm.runs[0]._ex.measurement_azimuth = self.header.rx.h_p_r[0]
                sm.runs[0]._ex.translated_azimuth = self.header.rx.h_p_r[0]
                sm.runs[0]._ex.channel_id = 1

            elif "zy" in comp:
                sm.runs[0]._ey.component = "ey"
                sm.runs[0]._ey.dipole_length = self.header.rx.length
                sm.runs[0]._ey.measurement_azimuth = self.header.rx.h_p_r[0] + 90
                sm.runs[0]._ey.translated_azimuth = self.header.rx.h_p_r[0] + 90
                sm.runs[0]._ey.channel_id = 2
            if comp[-1] == "x":
                sm.runs[0]._hx.component = "hx"
                sm.runs[0]._hx.measurement_azimuth = self.header.rx.h_p_r[0]
                sm.runs[0]._hx.translated_azimuth = self.header.rx.h_p_r[0]
                sm.runs[0]._hx.channel_id = 3

            elif comp[-1] == "y":
                sm.runs[0]._hy.component = "hy"
                sm.runs[0]._hy.measurement_azimuth = self.header.rx.h_p_r[0] + 90
                sm.runs[0]._hy.translated_azimuth = self.header.rx.h_p_r[0] + 90
                sm.runs[0]._hy.channel_id = 4

            if comp[1] == "z":
                sm.runs[0]._hz.component = "hz"
                sm.runs[0]._hz.measurement_tilt = self.header.rx.h_p_r[-1]
                sm.runs[0]._hz.translated_tilt = self.header.rx.h_p_r[-1]
                sm.runs[0]._hz.translated_azimuth = self.header.rx.h_p_r[0]
                sm.runs[0]._hz.channel_id = 5

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
