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

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Survey, Tx, Rx, MTEdit, Unit, GPS, GDP, CH, STN, Line, MTFT24
from mt_metadata.utils.validators import validate_attribute

# =============================================================================
attr_dict = get_schema("header", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("survey", SCHEMA_FN_PATHS), name="survey")
attr_dict.add_dict(get_schema("tx", SCHEMA_FN_PATHS), name="tx")
attr_dict.add_dict(get_schema("rx", SCHEMA_FN_PATHS), name="rx")
attr_dict.add_dict(MTEdit()._attr_dict, name="m_t_edit")
attr_dict.add_dict(MTFT24()._attr_dict, name="m_t_f_t24")
attr_dict.add_dict(get_schema("gps", SCHEMA_FN_PATHS), name="g_p_s")
attr_dict.add_dict(get_schema("gdp", SCHEMA_FN_PATHS), name="g_d_p")
attr_dict.add_dict(get_schema("ch", SCHEMA_FN_PATHS), name="ch")
attr_dict.add_dict(get_schema("stn", SCHEMA_FN_PATHS), name="stn")
attr_dict.add_dict(get_schema("line", SCHEMA_FN_PATHS), name="line")
attr_dict.add_dict(get_schema("unit", SCHEMA_FN_PATHS), name="unit")


# =============================================================================


class Header(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.survey = Survey()
        self.tx = Tx()
        self.rx = Rx()
        self.m_t_edit = MTEdit()
        self.m_t_f_t24 = MTFT24()
        self.ch = CH()
        self.g_p_s = GPS()
        self.g_d_p = GDP()
        self.stn = STN()
        self.line = Line()
        self.unit = Unit()
        super().__init__(attr_dict=attr_dict, **kwargs)

        self._comp_dict = {}

        self._header_keys = [
            "survey.type",
            "survey.array",
            "tx.type",
            "m_t_edit.version",
            "m_t_edit.auto.phase_flip",
            "m_t_edit.phase_slope.smooth",
            "m_t_edit.phase_slope.to_z_mag",
            "m_t_edit.d_plus.use",
            "rx.gdp_stn",
            "rx.length",
            "rx.h_p_r",
            "g_p_s.lat",
            "g_p_s.lon",
            "unit.length",
        ]

    def read_header(self, lines):
        """
        Read the header of an AVG file and fill attributes accordingly

        :param lines: list of lines to read
        :type lines: list of strings

        """

        comp = None
        data_lines = []
        for ii, line in enumerate(lines):
            if line.find("=") > 0 and line.find("$") == 0:
                key, value = line[1:].split("=")
                key = ".".join(
                    [
                        validate_attribute(k)
                        for k in key.replace(":", ".").split(".")
                    ]
                )

                value = value.lower().strip()
                if "," in value:
                    value = [v.strip() for v in value.split(",")]
                if "length" in key:
                    value = value.split()
                    if len(value) > 1:
                        value = value[0]
                    else:
                        value = value[0].strip()

                if "rx.cmp" in key:
                    comp = value
                    data_lines.append(line)
                    self._comp_dict[comp] = {"rx": Rx(), "ch": CH()}
                if comp is not None:
                    comp_key, comp_attr = key.split(".")

                    self._comp_dict[comp][comp_key].set_attr_from_name(
                        comp_attr, value
                    )
                else:
                    self.set_attr_from_name(key, value)
            else:
                if len(line) > 2:
                    data_lines.append(line)

        return data_lines

    @property
    def latitude(self):
        return self.g_p_s.lat

    @latitude.setter
    def latitude(self, value):
        self.g_p_s.lat = value

    @property
    def longitude(self):
        return self.g_p_s.lon

    @longitude.setter
    def longitude(self, value):
        self.g_p_s.lon = value

    @property
    def elevation(self):
        if self.center_location is not None:
            return self.center_location[-1]

    @property
    def easting(self):
        if self.center_location is not None:
            return self.center_location[0]

    @property
    def northing(self):
        if self.center_location is not None:
            return self.center_location[1]

    @property
    def center_location(self):
        if self._comp_dict != {}:
            try:
                location_str = self._comp_dict["zxx"]["rx"].center
                return [
                    float(ss.strip().split()[0])
                    for ss in location_str.split(":")
                ]

            except KeyError:
                return None

    @property
    def datum(self):
        return self.g_p_s.datum

    @property
    def utm_zone(self):
        return self.g_p_s.u_t_m_zone

    @property
    def station(self):
        return self.rx.gdp_stn

    @station.setter
    def station(self, value):
        self.rx.gdp_stn = value

    def write_header(self):
        """
        Write .avg header lines

        :return: DESCRIPTION
        :rtype: TYPE

        """
        lines = [""]

        for key in self._header_keys:
            value = self.get_attr_from_name(key)
            if isinstance(value, list):
                value = ",".join([f"{v:.1f}" for v in value])
            elif isinstance(value, (float)):
                value = f"{value:.7f}"
            elif isinstance(value, (int)):
                value = f"{value:.0f}"

            key = (
                key.replace("_", " ")
                .title()
                .replace(" ", "")
                .replace("MTEdit.", "MTEdit:")
            )

            lines.append(f"${key}={value.capitalize()}")

        return lines
