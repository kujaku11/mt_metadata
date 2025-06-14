# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 12:09:13 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================

from mt_metadata.base import get_schema
from mt_metadata.transfer_functions.tf import Location

from . import BirrpAngles, BirrpBlock, BirrpParameters
from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("header", SCHEMA_FN_PATHS)
attr_dict.add_dict(Location()._attr_dict.copy())
# =============================================================================


class Header(Location):
    def __init__(self, **kwargs):
        self.birrp_parameters = BirrpParameters()
        self.data_blocks = []
        self.angles = []
        super().__init__()
        super(Location, self).__init__(attr_dict=attr_dict)

        for k, v in kwargs.items():
            self.set_attr_from_name(k, v)

    def _read_header_line(self, line):
        """
        read a header line
        """
        line = " ".join(line[1:].strip().split())

        new_line = ""

        # need to restructure the string so its readable, at least the way
        # that birrp outputs the file
        e_find = 0
        for ii in range(len(line)):
            if line[ii] == "=":
                e_find = ii
                new_line += line[ii]
            elif line[ii] == " ":
                if abs(e_find - ii) == 1:
                    pass
                else:
                    new_line += ","
            else:
                new_line += line[ii]
        # now that we have a useful line, split it into its parts
        line_list = new_line.split(",")

        # try to split up the parts into a key=value setup
        # and try to make the values floats if they can be
        l_dict = {}
        key = "null"
        for ll in line_list:
            ll_list = ll.split("=")
            if len(ll_list) == 1:
                continue
            # some times there is just a list of numbers, need a way to read
            # that.
            if len(ll_list) != 2:
                if type(l_dict[key]) is not list:
                    l_dict[key] = list([l_dict[key]])
                try:
                    l_dict[key].append(float(ll))
                except ValueError:
                    l_dict[key].append(ll)
            else:
                key = ll_list[0]
                try:
                    value = float(ll_list[1])
                except ValueError:
                    value = ll_list[1]
                l_dict[key] = value
        return l_dict

    def read_header(self, j_lines):
        """
        Parsing the header lines of a j-file to extract processing information.

        Input:
        - j-file as list of lines (output of readlines())

        Output:
        - Dictionary with all parameters found

        """
        self.data_blocks = []
        self.angles = []

        header_lines = [j_line for j_line in j_lines if "#" in j_line]
        self.title = header_lines[0][1:].strip()

        fn_count = -1
        theta_count = -1
        # put the information into a dictionary
        for h_line in header_lines[1:]:
            h_dict = self._read_header_line(h_line)
            for key, value in h_dict.items():
                if key in [
                    "filnam",
                    "nskip",
                    "nread",
                    "ncomp",
                    "indices",
                    "nfil",
                ]:
                    if key in ["nfil"]:
                        fn_count += 1
                    if len(self.data_blocks) != fn_count + 1:
                        self.data_blocks.append(BirrpBlock())
                    self.data_blocks[fn_count].set_attr_from_name(key, value)
                # if its the line of angles, put them all in a list with a unique key
                elif key in ["theta1", "theta2", "phi"]:
                    if key == "theta1":
                        theta_count += 1
                    if len(self.angles) != theta_count + 1:
                        self.angles.append(BirrpAngles())
                    self.angles[theta_count].set_attr_from_name(key, value)
                else:
                    self.birrp_parameters.set_attr_from_name(key, value)

    def read_metadata(self, j_lines):
        """
        read in the metadata of the station, or information of station
        logistics like: lat, lon, elevation

        Not really needed for a birrp output since all values are nan's
        """

        metadata_lines = [j_line for j_line in j_lines if ">" in j_line]

        for m_line in metadata_lines:
            m_list = m_line.strip().split("=")
            m_key = m_list[0][1:].strip().lower()
            try:
                m_value = float(m_list[0].strip())
            except ValueError:
                m_value = 0.0
            self.set_attr_from_name(m_key, m_value)
