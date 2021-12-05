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

    def __init__(self):

        self.Survey_Type = "NSAMT"
        self.Survey_Array = "Tensor"
        self.Tx_Type = "Natural"
        self.MTEdit3Version = "3.001 applied on 2010-11-19"
        self.MTEdit3Auto_PhaseFlip = "No"
        self.MTEdit3PhaseSlope_Smooth = "Moderate"
        self.MTEdit3PhaseSlope_toMag = "No"
        self.MTEdit3DPlus_Use = "No"
        self.Rx_GdpStn = 4
        self.Rx_Length = 100
        self.Rx_HPR = [90, 0, 0]
        self.GPS_Lat = 0.0
        self.GPS_Lon = 0.0
        self.Unit_Length = "m"
        self.header_dict = {
            "Survey.Type": self.Survey_Type,
            "Survey.Array": self.Survey_Array,
            "Tx.Type": self.Tx_Type,
            "MTEdit:Version": self.MTEdit3Version,
            "MTEdit:Auto.PhaseFlip": self.MTEdit3Auto_PhaseFlip,
            "MTEdit:PhaseSlope.Smooth": self.MTEdit3PhaseSlope_Smooth,
            "MTEdit:PhaseSlope.toZmag": self.MTEdit3PhaseSlope_toMag,
            "MTEdit:DPlus.Use": self.MTEdit3DPlus_Use,
            "Rx.GdpStn": self.Rx_GdpStn,
            "Rx.Length": self.Rx_Length,
            "Rx.HPR": self.Rx_HPR,
            "GPS.Lat": self.GPS_Lat,
            "GPS.Lon": self.GPS_Lon,
            "Unit.Length": self.Unit_Length,
        }

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
            self.fn = fn
        self.comp = self.fn.stem[0]
        with open(self.fn, "r") as fid:
            alines = fid.readlines()

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
        for aline in alines:
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
                else:
                    akey = alst[0][1:].replace(".", "_")
                    if akey.lower().find("length"):
                        alst[1] = alst[1][0:-1]
                    try:
                        self.__dict__[akey] = float(alst[1])
                    except ValueError:
                        self.__dict__[akey] = alst[1]
                    # self.header_dict[alst[0][1:]] = al            print(aline)st[1]
            elif aline[0] == "S":
                pass
            # read the data line.
            elif len(aline) > 2:
                aline = aline.replace("*", "0.50")
                alst = [aa.strip() for aa in aline.strip().split(",")]
                for cc, ckey in enumerate(self.info_keys):
                    self.comp_dict[akey][ii][ckey.lower()] = alst[cc]
                ii += 1

        self._fill_z()
        self._fill_t()

        print("Read file {0}".format(self.fn))

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

    # def write_edi(
    #     self,
    #     avg_fn,
    #     station,
    #     survey_dict=None,
    #     survey_cfg_file=None,
    #     mtft_cfg_file=None,
    #     mtedit_cfg_file=r"c:\MinGW32-xy\Peacock\zen\bin\mtedit.cfg",
    #     save_path=None,
    #     rrstation=None,
    #     copy_path=r"d:\Peacock\MTData\EDI_Files",
    #     avg_ext=".avg",
    # ):
    #     """
    #     write an edi file from the .avg files

    #     Arguments:
    #     ----------
    #         **avg_fn** : string
    #                      full path to avg file name

    #         **survey_dict** : dictionary
    #                           dictionary containing the survey parameters
    #                           such as lat, lon, elevation, date, etc.

    #         **survey_cfg_file** : string (full path to survey file)
    #                           file contains all the important information
    #                           about the setup of the station, input file if
    #                           survey_dict is None.  This is created by
    #                           mtpy.configfile

    #         **mtft_cfg_file** : string (full path to mtft24.cfg file)
    #                            this file contains information on how the
    #                            Fourier coefficients were calculated

    #         **mtedit_cfg_file** : string (full path to MTEdit.cfg file)
    #                               this file contains information on how
    #                               the transfer functions were estimated

    #         **save_path** : string (full path or directory to where .edi file
    #                                 will be saved)

    #     Outputs:
    #     ---------
    #         **edi_fn** : string (full path to .edi file)

    #     """

    #     if save_path is None:
    #         save_dir = os.path.dirname(avg_fn)
    #         save_path = os.path.join(save_dir, station + ".edi")

    #     # create an mtedi instance
    #     self.edi = mtedi.Edi()
    #     self.edi.Z = self.Z
    #     self.edi.Tipper = self.Tipper

    #     # read in avg file
    #     if os.path.isfile(avg_fn) == True:
    #         self.read_avg_file(avg_fn)
    #         self.edi.Z = self.Z
    #         self.edi.Tipper = self.Tipper
    #     else:
    #         raise NameError("Could not find {0}".format(avg_fn))

    #     # read in survey file
    #     survey_dict = None
    #     if survey_cfg_file is not None:
    #         sdict = mtcf.read_survey_configfile(survey_cfg_file)

    #     try:
    #         survey_dict = sdict[station.upper()]
    #     except KeyError:
    #         if survey_dict is not None:
    #             try:
    #                 survey_dict["station"]
    #             except KeyError:
    #                 try:
    #                     survey_dict["station_name"]
    #                 except KeyError:
    #                     raise KeyError(
    #                         "Could not find station information in" ", check inputs"
    #                     )
    #         else:
    #             raise KeyError(
    #                 "Could not find {0} in survey file".format(station.upper())
    #             )

    #     # get remote reference information if desired
    #     if rrstation:
    #         try:
    #             rrsurvey_dict = sdict[rrstation.upper()]
    #             survey_dict["rr_station"] = rrsurvey_dict["station"]
    #             survey_dict["rr_station_elevation"] = rrsurvey_dict["elevation"]
    #             survey_dict["rr_station_latitude"] = gis_tools.assert_lat_value(
    #                 rrsurvey_dict.pop("latitude", 0.0)
    #             )
    #             survey_dict["rr_station_longitude"] = gis_tools.assert_lon_value(
    #                 rrsurvey_dict.pop("longitude", 0.0)
    #             )
    #         except KeyError:
    #             print("Could not find station information for remote reference")
    #     else:
    #         rrsurvey_dict = None

    #     # read in mtft24.cfg file
    #     if mtft_cfg_file is None:
    #         try:
    #             mtft_cfg_file = os.path.join(save_dir, "mtft24.cfg")
    #             zmtft = ZongeMTFT()
    #             zmtft.read_cfg(mtft_cfg_file)
    #             mtft_dict = zmtft.meta_dict
    #         except:
    #             mtft_dict = None
    #     else:
    #         zmtft = ZongeMTFT()
    #         zmtft.read_cfg(mtft_cfg_file)
    #         mtft_dict = zmtft.meta_dict

    #     # read in mtedit.cfg file
    #     if mtedit_cfg_file:
    #         zmtedit = ZongeMTEdit()
    #         zmtedit.read_config(mtedit_cfg_file)
    #         mtedit_dict = zmtedit.meta_dict
    #     else:
    #         mtedit_dict = None

    #     # ----------------HEAD BLOCK------------------
    #     # from survey dict get information

    #     # --> data id
    #     try:
    #         self.edi.Header.dataid = survey_dict["station"]
    #     except KeyError:
    #         self.edi.Header.dataid = station

    #     # --> acquired by
    #     self.edi.Header.acqby = survey_dict.pop("network", "USGS")

    #     # --> file by
    #     self.edi.Header.fileby = survey_dict.pop("network", "MTpy")

    #     # --> acquired date
    #     self.edi.Header.acqdate = survey_dict.pop(
    #         "date", time.strftime("%Y-%m-%d", time.localtime())
    #     )

    #     # --> prospect
    #     self.edi.Header.loc = survey_dict.pop("location", "Earth")

    #     # --> latitude
    #     self.edi.Header.lat = survey_dict.pop("latitude", 0.0)

    #     # --> longitude
    #     self.edi.Header.lon = survey_dict.pop("longitude", 0.0)

    #     # --> elevation
    #     self.edi.Header.elev = survey_dict.pop("elevation", 0)

    #     # -----------------INFO BLOCK---------------------------
    #     self.edi.Info.info_list = []
    #     self.edi.Info.info_list.append("MAX LINES: 999")

    #     # --> put the rest of the survey parameters in the info block
    #     for skey in sorted(survey_dict.keys()):
    #         self.edi.Info.info_list.append("{0}: {1}".format(skey, survey_dict[skey]))

    #     # --> put parameters about how fourier coefficients were found
    #     if mtft_dict is not None:
    #         for mkey in sorted(mtft_dict.keys()):
    #             if mkey == "setup_lst" or mkey.lower() == "mtft.tsplot.chnrange":
    #                 pass
    #             else:
    #                 self.edi.Info.info_list.append(
    #                     "{0}: {1}".format(mkey, mtft_dict[mkey])
    #                 )

    #     # --> put parameters about how transfer function was found
    #     if mtedit_dict is not None:
    #         for mkey in list(mtedit_dict.keys()):
    #             self.edi.Info.info_list.append(
    #                 "{0}: {1}".format(mkey, mtedit_dict[mkey])
    #             )

    #     # ----------------DEFINE MEASUREMENT BLOCK------------------
    #     self.edi.Define_measurement.maxchan = 5
    #     self.edi.Define_measurement.maxrun = 999
    #     self.edi.Define_measurement.maxmeas = 99999

    #     try:
    #         self.edi.Define_measurement.units = mtedit_dict["unit.length"]
    #     except (TypeError, KeyError):
    #         self.edi.Define_measurement.units = "m"

    #     self.edi.Define_measurement.reftype = "cartesian"
    #     self.edi.Define_measurement.reflat = self.edi.Header.lat
    #     self.edi.Define_measurement.reflon = self.edi.Header.lon
    #     self.edi.Define_measurement.refelev = self.edi.Header.elev

    #     # ------------------HMEAS_EMEAS BLOCK--------------------------
    #     if mtft_dict:
    #         chn_lst = mtft_dict["setup_lst"][0]["Chn.Cmp"]
    #         chn_id = mtft_dict["setup_lst"][0]["Chn.ID"]
    #         chn_len_lst = mtft_dict["setup_lst"][0]["Chn.Length"]

    #     else:
    #         chn_lst = ["hx", "hy", "hz", "ex", "ey"]
    #         chn_id = [1, 2, 3, 4, 5]
    #         chn_len_lst = [100] * 5

    #     chn_id_dict = dict(
    #         [
    #             (comp.lower(), (comp.lower(), cid, clen))
    #             for comp, cid, clen in zip(chn_lst, chn_id, chn_len_lst)
    #         ]
    #     )

    #     # --> hx component
    #     try:
    #         hxazm = survey_dict["b_xaxis_azimuth"]
    #     except KeyError:
    #         hxazm = 0
    #     try:
    #         hdict = {
    #             "id": chn_id_dict["hx"][1],
    #             "chtype": "{0}".format(chn_id_dict["hx"][0].upper()),
    #             "x": 0,
    #             "y": 0,
    #             "azm": hxazm,
    #             "acqchan": "{0}".format(chn_id_dict["hx"][0].upper()),
    #         }
    #     except KeyError:
    #         hdict = {
    #             "id": 1,
    #             "chtype": "{0}".format("hx"),
    #             "x": 0,
    #             "y": 0,
    #             "azm": hxazm,
    #             "acqchan": "hx",
    #         }
    #     self.edi.Define_measurement.meas_hx = mtedi.HMeasurement(**hdict)

    #     # --> hy component
    #     try:
    #         hyazm = survey_dict["b_yaxis_azimuth"]
    #     except KeyError:
    #         hyazm = 90
    #     try:
    #         hdict = {
    #             "id": chn_id_dict["hy"][1],
    #             "chtype": "{0}".format(chn_id_dict["hy"][0].upper()),
    #             "x": 0,
    #             "y": 0,
    #             "azm": hyazm,
    #             "acqchan": "{0}".format(chn_id_dict["hy"][0].upper()),
    #         }

    #     except KeyError:
    #         hdict = {
    #             "id": 2,
    #             "chtype": "hy",
    #             "x": 0,
    #             "y": 0,
    #             "azm": hyazm,
    #             "acqchan": "hy",
    #         }
    #     self.edi.Define_measurement.meas_hy = mtedi.HMeasurement(**hdict)

    #     # --> hz component
    #     try:
    #         hdict = {
    #             "id": chn_id_dict["hz"][1],
    #             "chtype": "{0}".format(chn_id_dict["hz"][0].upper()),
    #             "x": 0,
    #             "y": 0,
    #             "azm": 0,
    #             "acqchan": "{0}".format(chn_id_dict["hz"][0].upper()),
    #         }

    #     except KeyError:
    #         hdict = {"id": 3, "chtype": "hz", "x": 0, "y": 0, "azm": 0}
    #     self.edi.Define_measurement.meas_hz = mtedi.HMeasurement(**hdict)

    #     # --> ex component
    #     try:
    #         edict = {
    #             "id": chn_id_dict["ex"][1],
    #             "chtype": "{0}".format(chn_id_dict["ex"][0].upper()),
    #             "x": 0,
    #             "y": 0,
    #             "x2": chn_id_dict["ex"][2],
    #             "y2": 0,
    #         }
    #     except KeyError:
    #         edict = {"id": 4, "chtype": "ex", "x": 0, "Y": 0, "x2": 100, "y2": 0}
    #     self.edi.Define_measurement.meas_ex = mtedi.EMeasurement(**edict)

    #     # --> ey component
    #     try:
    #         edict = {
    #             "id": chn_id_dict["ey"][1],
    #             "chtype": "{0}".format(chn_id_dict["ey"][0].upper()),
    #             "x": 0,
    #             "y": 0,
    #             "x2": 0,
    #             "y2": chn_id_dict["ey"][2],
    #         }
    #     except KeyError:
    #         edict = {"id": 5, "chtype": "ey", "x": 0, "Y": 0, "x2": 0, "y2": 100}
    #     self.edi.Define_measurement.meas_ey = mtedi.EMeasurement(**edict)

    #     # --> remote reference
    #     if rrsurvey_dict:
    #         hxid = rrsurvey_dict.pop("hx", 6)
    #         hyid = rrsurvey_dict.pop("hy", 7)
    #         hxazm = rrsurvey_dict.pop("b_xaxis_azimuth", 0)
    #         hyazm = rrsurvey_dict.pop("b_xaxis_azimuth", 90)
    #     else:
    #         hxid = 6
    #         hyid = 7
    #         hxazm = 0
    #         hyazm = 90

    #     # --> rhx component
    #     hdict = {
    #         "id": hxid,
    #         "chtype": "rhx",
    #         "x": 0,
    #         "y": 0,
    #         "azm": hxazm,
    #         "acqchan": "rhx",
    #     }
    #     self.edi.Define_measurement.meas_rhx = mtedi.HMeasurement(**hdict)

    #     # --> rhy component
    #     hdict = {
    #         "id": hyid,
    #         "chtype": "rhy",
    #         "x": 0,
    #         "y": 0,
    #         "azm": hyazm,
    #         "acqchan": "rhy",
    #     }
    #     self.edi.Define_measurement.meas_rhy = mtedi.HMeasurement(**hdict)

    #     # ----------------------MTSECT-----------------------------------------
    #     self.edi.Data_sect.nfreq = len(self.Z.freq)
    #     self.edi.Data_sect.sectid = station
    #     self.edi.Data_sect.nchan = len(chn_lst)
    #     for chn, chnid in zip(chn_lst, chn_id):
    #         setattr(self.edi.Data_sect, chn, chnid)

    #     # ----------------------ZROT BLOCK--------------------------------------
    #     self.edi.zrot = np.zeros(len(self.edi.Z.z))

    #     # ----------------------FREQUENCY BLOCK---------------------------------
    #     self.edi.freq = self.Z.freq

    #     # ============ WRITE EDI FILE ==========================================
    #     edi_fn = self.edi.write_edi_file(new_edi_fn=save_path)

    #     print("Wrote .edi file to {0}".format(edi_fn))

    #     if copy_path is not None:
    #         copy_edi_fn = os.path.join(copy_path, os.path.basename(edi_fn))
    #         if not os.path.exists(copy_path):
    #             os.mkdir(copy_path)
    #         shutil.copy(edi_fn, copy_edi_fn)
    #         print("Copied {0} to {1}".format(edi_fn, copy_edi_fn))

    #     return edi_fn

    # def plot_mt_response(self, avg_fn, **kwargs):
    #     """
    #     plot an mtv file
    #     """

    #     if os.path.isfile(avg_fn) is False:
    #         raise IOError("Could not find {0}, check path".format(avg_fn))

    #     self.read_avg_file(avg_fn)

    #     plot_resp = plotresponse.PlotResponse(
    #         z_object=self.Z, tipper_object=self.Tipper, plot_tipper="yri", **kwargs
    #     )

    #     return plot_resp

    # def write_edi_from_avg(
    #     self,
    #     avg_fn,
    #     station,
    #     survey_dict=None,
    #     survey_cfg_file=None,
    #     mtft_cfg_file=None,
    #     mtedit_cfg_file=r"c:\MinGW32-xy\Peacock\zen\bin\mtedit.cfg",
    #     save_path=None,
    #     rrstation=None,
    #     copy_path=r"d:\Peacock\MTData\EDI_Files",
    #     avg_ext=".avg",
    # ):
    #     """
    #     write an edi file from the .avg files

    #     Arguments:
    #     ----------
    #         **fnx** : string (full path to electric north file)
    #                   file for Zxx, Zxy

    #         **fny** : string (full path to electric east file)
    #                   file for Zyx, Zyy

    #         **survey_dict** : dictionary
    #                           dictionary containing the survey parameters
    #                           such as lat, lon, elevation, date, etc.

    #         **survey_cfg_file** : string (full path to survey file)
    #                           file contains all the important information
    #                           about the setup of the station, input file if
    #                           survey_dict is None.  This is created by
    #                           mtpy.configfile

    #         **mtft_cfg_file** : string (full path to mtft24.cfg file)
    #                            this file contains information on how the
    #                            Fourier coefficients were calculated

    #         **mtedit_cfg_file** : string (full path to MTEdit.cfg file)
    #                               this file contains information on how
    #                               the transfer functions were estimated

    #         **save_path** : string (full path or directory to where .edi file
    #                                 will be saved)

    #     Outputs:
    #     ---------
    #         **edi_fn** : string (full path to .edi file)

    #     """

    #     if save_path is None:
    #         save_dir = os.path.dirname(avg_fn)
    #         save_path = os.path.join(save_dir, station + ".edi")

    #     # create an mtedi instance
    #     self.edi = mtedi.Edi()
    #     self.edi.Z = self.Z
    #     self.edi.Tipper = self.Tipper

    #     if os.path.isfile(avg_fn) == True:
    #         self.read_avg_file(avg_fn)
    #         self.edi.Z = self.Z
    #         self.edi.Tipper = self.Tipper

    #     # read in survey file
    #     survey_dict = {}
    #     survey_dict["latitude"] = gis_tools.assert_lat_value(self.GPS_Lat)
    #     survey_dict["longitude"] = gis_tools.assert_lon_value(self.GPS_Lon)
    #     survey_dict["elevation"] = gis_tools.assert_elevation_value(self.Rx_Length)
    #     survey_dict["station"] = station
    #     if survey_cfg_file is not None:
    #         sdict = mtcf.read_survey_configfile(survey_cfg_file)

    #         try:
    #             survey_dict = sdict[station.upper()]
    #         except KeyError:
    #             if survey_dict is not None:
    #                 try:
    #                     survey_dict["station"]
    #                 except KeyError:
    #                     try:
    #                         survey_dict["station_name"]
    #                     except KeyError:
    #                         print(
    #                             "Could not find station information in" ", check inputs"
    #                         )

    #     # get remote reference information if desired
    #     if rrstation:
    #         try:
    #             rrsurvey_dict = sdict[rrstation.upper()]
    #             survey_dict["rr_station"] = rrsurvey_dict["station"]
    #             survey_dict["rr_station_elevation"] = rrsurvey_dict["elevation"]
    #             survey_dict["rr_station_latitude"] = gis_tools.assert_lat_value(
    #                 rrsurvey_dict.pop("latitude", 0.0)
    #             )
    #             survey_dict["rr_station_longitude"] = gis_tools.assert_lon_value(
    #                 rrsurvey_dict.pop("longitude", 0.0)
    #             )
    #         except KeyError:
    #             print("Could not find station information for remote reference")
    #     else:
    #         rrsurvey_dict = None

    #     # read in mtft24.cfg file
    #     if mtft_cfg_file is None:
    #         try:
    #             mtft_cfg_file = os.path.join(save_dir, "mtft24.cfg")
    #             zmtft = ZongeMTFT()
    #             zmtft.read_cfg(mtft_cfg_file)
    #             mtft_dict = zmtft.meta_dict
    #         except:
    #             mtft_dict = None
    #     else:
    #         zmtft = ZongeMTFT()
    #         zmtft.read_cfg(mtft_cfg_file)
    #         mtft_dict = zmtft.meta_dict

    #     # read in mtedit.cfg file
    #     if mtedit_cfg_file:
    #         zmtedit = ZongeMTEdit()
    #         zmtedit.read_config(mtedit_cfg_file)
    #         mtedit_dict = zmtedit.meta_dict
    #     else:
    #         mtedit_dict = None

    #     # ----------------HEAD BLOCK------------------
    #     # from survey dict get information
    #     head_dict = {}

    #     # --> data id
    #     try:
    #         head_dict["dataid"] = survey_dict["station"]
    #     except KeyError:
    #         head_dict["dataid"] = station

    #     # --> acquired by
    #     head_dict["acqby"] = survey_dict.pop("network", "")

    #     # --> file by
    #     head_dict["fileby"] = survey_dict.pop("network", "")

    #     # --> acquired date
    #     head_dict["acqdate"] = survey_dict.pop(
    #         "date", time.strftime("%Y-%m-%d", time.localtime())
    #     )

    #     # --> prospect
    #     head_dict["loc"] = survey_dict.pop("location", "")

    #     # --> latitude
    #     head_dict["lat"] = gis_tools.assert_lat_value(survey_dict.pop("latitude", 0.0))

    #     # --> longitude
    #     head_dict["long"] = gis_tools.assert_lon_value(
    #         survey_dict.pop("longitude", 0.0)
    #     )

    #     # --> elevation
    #     head_dict["elev"] = survey_dict.pop("elevation", 0.0)

    #     # --> set header dict as attribute of edi
    #     self.edi.head = head_dict

    #     # -----------------INFO BLOCK---------------------------
    #     info_dict = {}
    #     info_dict["max lines"] = 1000

    #     # --> put the rest of the survey parameters in the info block
    #     for skey in list(survey_dict.keys()):
    #         info_dict[skey] = survey_dict[skey]

    #     # --> put parameters about how fourier coefficients were found
    #     if mtft_dict:
    #         for mkey in list(mtft_dict.keys()):
    #             if mkey == "setup_lst" or mkey.lower() == "mtft.tsplot.chnrange":
    #                 pass
    #             else:
    #                 info_dict[mkey] = mtft_dict[mkey]

    #     # --> put parameters about how transfer function was found
    #     if mtedit_dict:
    #         for mkey in list(mtedit_dict.keys()):
    #             info_dict[mkey] = mtedit_dict[mkey]

    #     # --> set info dict as attribute of edi
    #     self.edi.info_dict = info_dict

    #     # ----------------DEFINE MEASUREMENT BLOCK------------------
    #     definemeas_dict = {}

    #     definemeas_dict["maxchan"] = 5
    #     definemeas_dict["maxrun"] = 999
    #     definemeas_dict["maxmeas"] = 99999
    #     try:
    #         definemeas_dict["units"] = mtedit_dict["unit.length"]
    #     except (TypeError, KeyError):
    #         definemeas_dict["units"] = "m"
    #     definemeas_dict["reftypy"] = "cartesian"
    #     definemeas_dict["reflat"] = head_dict["lat"]
    #     definemeas_dict["reflon"] = head_dict["long"]
    #     definemeas_dict["refelev"] = head_dict["elev"]

    #     # --> set definemeas as attribure of edi
    #     self.edi.definemeas = definemeas_dict

    #     # ------------------HMEAS_EMEAS BLOCK--------------------------
    #     hemeas_lst = []
    #     if mtft_dict:
    #         chn_lst = mtft_dict["setup_lst"][0]["Chn.Cmp"]
    #         chn_id = mtft_dict["setup_lst"][0]["Chn.ID"]
    #         chn_len_lst = mtft_dict["setup_lst"][0]["Chn.Length"]

    #     else:
    #         chn_lst = ["hx", "hy", "hz", "ex", "ey"]
    #         chn_id = [1, 2, 3, 4, 5]
    #         chn_len_lst = [100] * 5

    #     chn_id_dict = dict(
    #         [
    #             (comp.lower(), (comp.lower(), cid, clen))
    #             for comp, cid, clen in zip(chn_lst, chn_id, chn_len_lst)
    #         ]
    #     )

    #     # --> hx component
    #     try:
    #         hxazm = survey_dict["b_xaxis_azimuth"]
    #     except KeyError:
    #         hxazm = 0
    #     try:
    #         hemeas_lst.append(
    #             [
    #                 "HMEAS",
    #                 "ID={0}".format(chn_id_dict["hx"][1]),
    #                 "CHTYPE={0}".format(chn_id_dict["hx"][0].upper()),
    #                 "X=0",
    #                 "Y=0",
    #                 "AZM={0}".format(hxazm),
    #                 "",
    #             ]
    #         )
    #     except KeyError:
    #         hemeas_lst.append(
    #             [
    #                 "HMEAS",
    #                 "ID={0}".format(1),
    #                 "CHTYPE={0}".format("HX"),
    #                 "X=0",
    #                 "Y=0",
    #                 "AZM={0}".format(hxazm),
    #                 "",
    #             ]
    #         )

    #     # --> hy component
    #     try:
    #         hyazm = survey_dict["b_yaxis_azimuth"]
    #     except KeyError:
    #         hyazm = 90
    #     try:
    #         hemeas_lst.append(
    #             [
    #                 "HMEAS",
    #                 "ID={0}".format(chn_id_dict["hy"][1]),
    #                 "CHTYPE={0}".format(chn_id_dict["hy"][0].upper()),
    #                 "X=0",
    #                 "Y=0",
    #                 "AZM={0}".format(hxazm),
    #                 "",
    #             ]
    #         )
    #     except KeyError:
    #         hemeas_lst.append(
    #             [
    #                 "HMEAS",
    #                 "ID={0}".format(1),
    #                 "CHTYPE={0}".format("HY"),
    #                 "X=0",
    #                 "Y=0",
    #                 "AZM={0}".format(hxazm),
    #                 "",
    #             ]
    #         )
    #     # --> ex component
    #     try:
    #         hemeas_lst.append(
    #             [
    #                 "EMEAS",
    #                 "ID={0}".format(chn_id_dict["ex"][1]),
    #                 "CHTYPE={0}".format(chn_id_dict["ex"][0].upper()),
    #                 "X=0",
    #                 "Y=0",
    #                 "X2={0}".format(chn_id_dict["ex"][2]),
    #                 "Y2=0",
    #             ]
    #         )
    #     except KeyError:
    #         hemeas_lst.append(
    #             [
    #                 "EMEAS",
    #                 "ID={0}".format(1),
    #                 "CHTYPE={0}".format("EX"),
    #                 "X=0",
    #                 "Y=0",
    #                 "X2={0}".format(100),
    #                 "Y2=0",
    #             ]
    #         )

    #     # --> ey component
    #     try:
    #         hemeas_lst.append(
    #             [
    #                 "EMEAS",
    #                 "ID={0}".format(chn_id_dict["ey"][1]),
    #                 "CHTYPE={0}".format(chn_id_dict["ey"][0].upper()),
    #                 "X=0",
    #                 "Y=0",
    #                 "X2=0",
    #                 "Y2={0}".format(chn_id_dict["ey"][2]),
    #             ]
    #         )
    #     except KeyError:
    #         hemeas_lst.append(
    #             [
    #                 "EMEAS",
    #                 "ID={0}".format(1),
    #                 "CHTYPE={0}".format("EY"),
    #                 "X=0",
    #                 "Y=0",
    #                 "X2=0",
    #                 "Y2={0}".format(100),
    #             ]
    #         )

    #     # --> remote reference
    #     if rrsurvey_dict:
    #         hxid = rrsurvey_dict.pop("hx", 6)
    #         hyid = rrsurvey_dict.pop("hy", 7)
    #         hxazm = rrsurvey_dict.pop("b_xaxis_azimuth", 0)
    #         hyazm = rrsurvey_dict.pop("b_xaxis_azimuth", 90)
    #     else:
    #         hxid = 6
    #         hyid = 7
    #         hxazm = 0
    #         hyazm = 90

    #     # --> rhx component
    #     hemeas_lst.append(
    #         [
    #             "HMEAS",
    #             "ID={0}".format(hxid),
    #             "CHTYPE={0}".format("rhx".upper()),
    #             "X=0",
    #             "Y=0",
    #             "AZM={0}".format(hxazm),
    #             "",
    #         ]
    #     )
    #     # --> rhy component
    #     hemeas_lst.append(
    #         [
    #             "HMEAS",
    #             "ID={0}".format(hyid),
    #             "CHTYPE={0}".format("rhy".upper()),
    #             "X=0",
    #             "Y=0",
    #             "AZM={0}".format(hyazm),
    #             "",
    #         ]
    #     )
    #     hmstring_lst = []
    #     for hm in hemeas_lst:
    #         hmstring_lst.append(" ".join(hm))
    #     # --> set hemeas as attribute of edi
    #     self.edi.hmeas_emeas = hmstring_lst

    #     # ----------------------MTSECT-----------------------------------------
    #     mtsect_dict = {}
    #     mtsect_dict["sectid"] = station
    #     mtsect_dict["nfreq"] = len(self.Z.freq)
    #     for chn, chnid in zip(chn_lst, chn_id):
    #         mtsect_dict[chn] = chnid

    #     # --> set mtsect as attribure of edi
    #     self.edi.mtsect = mtsect_dict

    #     # ----------------------ZROT BLOCK--------------------------------------
    #     self.edi.zrot = np.zeros(len(self.edi.Z.z))

    #     # ----------------------FREQUENCY BLOCK---------------------------------
    #     self.edi.freq = self.Z.freq

    #     # ============ WRITE EDI FILE ==========================================
    #     edi_fn = self.edi.write_edi_file(save_path)

    #     print("Wrote .edi file to {0}".format(edi_fn))

    #     if copy_path is not None:
    #         copy_edi_fn = os.path.join(copy_path, os.path.basename(edi_fn))
    #         if not os.path.exists(copy_path):
    #             os.mkdir(copy_path)
    #         shutil.copy(edi_fn, copy_edi_fn)
    #         print("Copied {0} to {1}".format(edi_fn, copy_edi_fn))

    #     return edi_fn
