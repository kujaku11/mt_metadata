# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:25:11 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.tf import Location
from mt_metadata.transfer_functions.io.tools import _validate_str_with_equals
from . import HMeasurement, EMeasurement

# =============================================================================
attr_dict = get_schema("define_measurement", SCHEMA_FN_PATHS)
# =============================================================================


# ==============================================================================
#  Define measurement class
# ==============================================================================
class DefineMeasurement(Base):
    """
    DefineMeasurement class holds information about the measurement.  This
    includes how each channel was setup.  The main block contains information
    on the reference location for the station.  This is a bit of an archaic
    part and was meant for a multiple station .edi file.  This section is also
    important if you did any forward modeling with Winglink cause it only gives
    the station location in this section.  The other parts are how each channel
    was collected.  An example define measurement section looks like::

        >=DEFINEMEAS

            MAXCHAN=7
            MAXRUN=999
            MAXMEAS=9999
            UNITS=M
            REFTYPE=CART
            REFLAT=-30:12:49.4693
            REFLONG=139:47:50.87
            REFELEV=0

        >HMEAS ID=1001.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1002.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0
        >HMEAS ID=1003.001 CHTYPE=HZ X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >EMEAS ID=1004.001 CHTYPE=EX X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >EMEAS ID=1005.001 CHTYPE=EY X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >HMEAS ID=1006.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1007.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0

    :param fn: full path to .edi file to read in.
    :type fn: string

    ================= ==================================== ======== ===========
    Attributes        Description                          Default  In .edi
    ================= ==================================== ======== ===========
    fn                Full path to edi file read in        None     no
    maxchan           Maximum number of channels measured  None     yes
    maxmeas           Maximum number of measurements       9999     yes
    maxrun            Maximum number of measurement runs   999      yes
    meas_####         HMeasurement or EMEasurment object   None     yes
                      defining the measurement made [1]__
    refelev           Reference elevation (m)              None     yes
    reflat            Reference latitude [2]_              None     yes
    refloc            Reference location                   None     yes
    reflon            Reference longituted [2]__           None     yes
    reftype           Reference coordinate system          'cart'   yes
    units             Units of length                      m        yes
    _define_meas_keys Keys to include in define_measurment [3]__     no
                      section.
    ================= ==================================== ======== ===========

    .. [1] Each channel with have its own define measurement and depending on
           whether it is an E or H channel the metadata will be different.
           the #### correspond to the channel number.
    .. [2] Internally everything is converted to decimal degrees.  Output is
          written as HH:MM:SS.ss so Winglink can read them in.
    .. [3] If you want to change what metadata is written into the .edi file
           change the items in _header_keys.  Default attributes are:
               * maxchan
               * maxrun
               * maxmeas
               * reflat
               * reflon
               * refelev
               * reftype
               * units

    """

    def __init__(self, **kwargs):
        self.measurement_list = None
        self._location = Location()
        self.maxmeas = 7
        self.maxrun = 999
        self.refelev = 0
        self.reflat = 0
        self.reflon = 0
        self.reftype = "cartesian"
        self.units = "m"
        self.refloc = None

        self._define_meas_keys = [
            "maxchan",
            "maxrun",
            "maxmeas",
            "refloc",
            "reflat",
            "reflon",
            "refelev",
            "reftype",
            "units",
        ]

        super().__init__(attr_dict=attr_dict, **kwargs)
        if self.reftype is None:
            self.reftype = "cartesian"
        if self.units is None:
            self.units = "m"
        if self.maxmeas == 0:
            self.maxmeas = 7
        if self.maxrun == 0:
            self.maxrun = 999

    def __str__(self):
        return "".join(self.write_measurement())

    def __repr__(self):
        return self.__str__()

    @property
    def reflat(self):
        return self._location.latitude

    @reflat.setter
    def reflat(self, value):
        self._location.latitude = value

    @property
    def reflon(self):
        return self._location.longitude

    @reflon.setter
    def reflon(self, value):
        self._location.longitude = value

    @property
    def reflong(self):
        return self._location.longitude

    @reflong.setter
    def reflong(self, value):
        self._location.longitude = value

    @property
    def refelev(self):
        return self._location.elevation

    @refelev.setter
    def refelev(self, value):
        self._location.elevation = value

    @property
    def channel_ids(self):
        ch_ids = {}
        for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
            try:
                m = getattr(self, f"meas_{comp}")
                # if there are remote references that are the same as the
                # h channels skip them.
                ch_ids[m.chtype] = m.id
            except AttributeError:
                continue

        return ch_ids

    def get_measurement_lists(self, edi_lines):
        """
        get measurement list including measurement setup
        """

        self.measurement_list = []
        meas_find = False
        count = 0

        for line in edi_lines:
            if ">=" in line and "definemeas" in line.lower():
                meas_find = True
            elif ">=" in line:
                if meas_find is True:
                    return
            elif meas_find is True and ">" not in line:
                line = line.strip()
                if len(line) > 2:
                    if count > 0:
                        line_list = _validate_str_with_equals(line)
                        for ll in line_list:
                            ll_list = ll.split("=")
                            key = ll_list[0].lower()
                            value = ll_list[1]
                            self.measurement_list[-1][key] = value
                    else:
                        self.measurement_list.append(line.strip())

            # look for the >XMEAS parts
            elif ">" in line and meas_find:
                if line.find("!") > 0:
                    pass
                elif "meas" in line.lower():
                    count += 1
                    line_list = _validate_str_with_equals(line)
                    m_dict = {}
                    for ll in line_list:
                        ll_list = ll.split("=")
                        key = ll_list[0].lower()
                        value = ll_list[1]
                        m_dict[key] = value
                    self.measurement_list.append(m_dict)
                else:
                    return

    def read_measurement(self, edi_lines):
        """
        read the define measurment section of the edi file

        should be a list with lines for:

            - maxchan
            - maxmeas
            - maxrun
            - refelev
            - reflat
            - reflon
            - reftype
            - units
            - dictionaries for >XMEAS with keys:

                - id
                - chtype
                - x
                - y
                - axm
                - acqchn

        """
        self.get_measurement_lists(edi_lines)

        for line in self.measurement_list:
            if isinstance(line, str):
                line_list = line.split("=")
                key = line_list[0].lower()
                value = line_list[1].strip()
                if key in "reflatitude":
                    key = "reflat"
                    value = value
                elif key in "reflongitude":
                    key = "reflon"
                    value = value
                elif key in "refelevation":
                    key = "refelev"
                    value = value
                elif key in "maxchannels":
                    key = "maxchan"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                elif key in "maxmeasurements":
                    key = "maxmeas"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                elif key in "maxruns":
                    key = "maxrun"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                setattr(self, key, value)

            elif isinstance(line, dict):
                ch_type = line["chtype"].lower()
                key = f"meas_{ch_type}"
                if ch_type.find("h") >= 0:
                    value = HMeasurement(**line)
                elif ch_type.find("e") >= 0:
                    value = EMeasurement(**line)
                    if value.azm == 0:
                        value.azm = value.azimuth
                if hasattr(self, key):
                    existing_ch = getattr(self, key)
                    existing_line = existing_ch.write_meas_line()
                    value_line = value.write_meas_line()
                    if existing_line != value_line:
                        value.chtype = f"rr{ch_type}".upper()
                        key = f"meas_rr{ch_type}"
                    else:
                        continue
                setattr(self, key, value)

    def write_measurement(
        self, measurement_list=None, longitude_format="LON", latlon_format="dd"
    ):
        """
        write the define measurement block as a list of strings
        """

        measurement_lines = ["\n>=DEFINEMEAS\n"]
        for key in self._define_meas_keys:
            value = getattr(self, key)
            if key in ["reflat", "reflon", "reflong"]:
                if latlon_format.lower() == "dd":
                    value = f"{float(value):.6f}"
                else:
                    value = self._location._convert_position_float2str(value)
            elif key == "refelev":
                value = value
            if key.upper() == "REFLON":
                if longitude_format == "LONG":
                    key += "G"
            if value is not None:
                measurement_lines.append(f"{' '*4}{key.upper()}={value}\n")
        measurement_lines.append("\n")

        # need to write the >XMEAS type, but sort by channel number
        m_key_list = []
        count = 1.0
        for kk in list(self.__dict__.keys()):
            if kk.find("meas_") == 0:
                key = kk.strip()
                value = self.__dict__[kk].id
                if value is None:
                    value = count
                    count += 1
                elif isinstance(value, str):
                    try:
                        value = float(value)

                    except TypeError:
                        self.logger.warning(
                            f"{key}.id cannot be converted to float"
                        )
                        value = count
                        count += 1
                elif isinstance(value, (float, int)):
                    value = float(value)

                else:
                    raise ValueError(f"Could not convert {key}.id to float")

                m_key_list.append((key, value))

        if len(m_key_list) == 0:
            self.logger.warning("No XMEAS information.")
        else:
            # need to sort the dictionary by chanel id
            for meas in sorted(m_key_list, key=lambda x: x[1]):
                x_key = meas[0]
                m_obj = getattr(self, x_key)
                if m_obj.id is None:
                    m_obj.id = meas[1]
                if m_obj.acqchan == "0":
                    m_obj.acqchan = meas[1]

                measurement_lines.append(m_obj.write_meas_line())

        return measurement_lines

    def get_measurement_dict(self):
        """
        get a dictionary for the xmeas parts
        """
        meas_dict = {}
        for key in list(self.__dict__.keys()):
            if key.find("meas_") == 0:
                meas_attr = getattr(self, key)
                meas_key = meas_attr.chtype
                meas_dict[meas_key] = meas_attr

        return meas_dict

    def from_metadata(self, channel):
        """
        create a measurement class from metadata

        :param channel: DESCRIPTION
        :type channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if channel.component is None:
            return

        azm = channel.measurement_azimuth
        if azm != channel.translated_azimuth:
            azm = channel.translated_azimuth
        if azm is None:
            azm = 0.0
        if "e" in channel.component:
            for attr in [
                "negative.x",
                "negative.y",
                "positive.x2",
                "positive.y2",
                "measurement_azimuth",
                "translated_azimuth",
            ]:
                if channel.get_attr_from_name(attr) is None:
                    channel.set_attr_from_name(attr, 0)
            meas = EMeasurement(
                **{
                    "x": channel.negative.x,
                    "x2": channel.positive.x2,
                    "y": channel.negative.y,
                    "y2": channel.positive.y2,
                    "chtype": channel.component,
                    "id": channel.channel_id,
                    "azm": azm,
                    "acqchan": channel.channel_number,
                }
            )

            setattr(self, f"meas_{channel.component.lower()}", meas)

        elif "h" in channel.component:
            for attr in ["location.x", "location.y", "location.z"]:
                if channel.get_attr_from_name(attr) is None:
                    channel.set_attr_from_name(attr, 0)
            meas = HMeasurement(
                **{
                    "x": channel.location.x,
                    "y": channel.location.y,
                    "azm": azm,
                    "chtype": channel.component,
                    "id": channel.channel_id,
                    "acqchan": channel.channel_number,
                    "dip": channel.measurement_tilt,
                }
            )
            setattr(self, f"meas_{channel.component.lower()}", meas)

    @property
    def channels_recorded(self):
        """Get the channels recorded"""

        return [cc.lower() for cc in self.get_measurement_dict().keys()]
