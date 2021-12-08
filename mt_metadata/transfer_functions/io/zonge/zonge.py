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

# ==============================================================================
# deal with avg files output from mtedit
# ==============================================================================
class ZongeMTAvg():
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

    def __init__(self):

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
            np.int,
            np.float,
            np.float,
            np.float,
            np.float,
            np.float,
            np.float,
            np.float,
            np.float,
            np.float,
            np.int,
            np.int,
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
        self.avg_dict = {"ex": "4", "ey": "5"}
        self.z_coordinate = "down"

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
        # check to see if all 4 components are in the .avg file
        if len(lines) > 140:
            comp_dict = dict(
                [
                    (ckey, np.zeros(int(len(lines) / 4), dtype=self.info_dtype))
                    for ckey in list(self.comp_flag.keys())
                ]
            )
        # if there are only 2
        else:
            comp_dict = dict(
                [
                    (ckey, np.zeros(int(len(lines) / 2), dtype=self.info_dtype))
                    for ckey in list(self.comp_flag.keys())
                ]
            )
        return comp_dict

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

    def convert2complex(self, zmag, zphase):
        """
        outputs of mtedit are magnitude and phase of z, convert to real and
        imaginary parts, phase is in milliradians

        """

        if type(zmag) is np.ndarray:
            assert len(zmag) == len(zphase)

        if self.z_coordinate == "up":
            zreal = zmag * np.cos((zphase / 1000) % np.pi)
            zimag = zmag * np.sin((zphase / 1000) % np.pi)
        else:
            zreal = zmag * np.cos((zphase / 1000))
            zimag = zmag * np.sin((zphase / 1000))

        return zreal, zimag

    def _match_freq(self, freq_list1, freq_list2):
        """
        fill the frequency dictionary where keys are freqeuency and
        values are index of where that frequency should be in the array of z
        and tipper
        """
        #
        #        if set(freq_list1).issubset(freq_list2) == True:
        #            return dict([(freq, ff) for ff, freq in enumerate(freq_list1)])
        #        else:
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
            self.z = np.zeros((new_nz, 2, 2), dtype="complex")
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

                zr, zi = self.convert2complex(
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

                zr, zi = self.convert2complex(
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
            print("No Tipper found")
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
            self.tipper = np.zeros((new_nz, 1, 2), dtype="complex")
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

                tr, ti = self.convert2complex(
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

                tzr, tzi = self.convert2complex(
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
