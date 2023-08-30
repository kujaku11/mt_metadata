# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 14:13:37 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base import Base
from mt_metadata.base.helpers import validate_name

# ==============================================================================
# Info object
# ==============================================================================
class Information(Base):
    """
    Contain, read, and write info section of .edi file

    not much to really do here, but just keep it in the same format that it is
    read in as, except if it is in phoenix format then split the two paragraphs
    up so they are sequential.

    """

    def __init__(self, fn=None, edi_lines=None):

        self.info_list = []
        self.info_dict = {}
        self._phoenix_col_width = 38
        self._phoenix_file = False
        self._empower_file = False

        self.phoenix_translation_dict = {
            "survey": "survey.id",
            "company": "station.acquired_by.organization",
            "job": "survey.project",
            "hardware": "run.data_logger.model",
            "mtuprog version": "run.data_logger.firmware.version",
            "xpr weighting": "processing_parameter",
            "hx sen": "run.hx.sensor.id",
            "hy sen": "run.hy.sensor.id",
            "hz sen": "run.hz.sensor.id",
            "rx sen": "run.rrhx.sensor.id",
            "ry sen": "run.rrhy.sensor.id",
            "stn number": "station.id",
            "mtu-box serial number": "run.data_logger.id",
            "ex pot resist": "run.ex.contact_resistance.start",
            "ey pot resist": "run.ey.contact_resistance.start",
            "ex voltage": ["run.ex.ac.start", "run.ex.dc.start"],
            "ey voltage": ["run.ey.ac.start", "run.ey.dc.start"],
            "start-up": "station.time_period.start",
            "end-time": "station.time_period.end",
        }

        self.translation_dict = {
            "operator": "run.acquired_by.author",
            "adu_serial": "run.data_logger.id",
            "e_azimuth": "run.ex.measurement_azimuth",
            "ex_len": "run.ex.dipole_length",
            "ey_len": "run.ey.dipole_length",
            "ex_resistance": "run.ex.contact_resistance.start",
            "ey_resistance": "run.ey.contact_resistance.start",
            "h_azimuth": "run.hx.measurement_azimuth",
            "hx": "run.hx.sensor.id",
            "hy": "run.hy.sensor.id",
            "hz": "run.hz.sensor.id",
            "hx_resistance": "run.hx.h_field_max.start",
            "hy_resistance": "run.hy.h_field_max.start",
            "hz_resistance": "run.hz.h_field_max.start",
            "algorithmname": "transfer_function.software.name",
            "ndec": "processing_parameter",
            "nfft": "processing_parameter",
            "ntype": "processing_parameter",
            "rrtype": "processing_parameter",
            "removelargelines": "processing_parameter",
            "rotmaxe": "processing_parameter",
            "project": "survey.project",
            "processedby": "transfer_function.processed_by.name",
            "processingsoftware": "transfer_function.software.name",
            "processingtag": "transfer_function.id",
            "signconvention": "transfer_function.sign_convention",
            "sitename": "station.geographic_name",
            "survey": "survey.id",
            "year": "survey.time_period.start_date",
            "runlist": "transfer_function.runs_processed",
            "remotesite": "transfer_function.remote_references",
            "remoteref": "transfer_function.processing_parameters",
        }

        self.empower_translation_dict = {
            "processingsoftware": "processing.software",
            "sitename": "station.geographic_name",
            "year": "survey.time_period.start_date",
            "process_date": "transfer_function.processed_date",
            "declination": "station.location.declination.value",
            "tag": "component",
            "length": "dipole_length",
            "ac": "ac.end",
            "dc": "dc.end",
            "negative_res": "contact_resistance.start",
            "positive_res": "contact_resistance.end",
            "sensor_type": "sensor.model",
            "azimuth": "measured_azimuth",
            "sensor_serial": "sensor.id",
            "cal_name": "comments",
            "saturation": "comments",
            "instrument_type": "model",
        }

        super().__init__(attr_dict={})

    def __str__(self):
        return "".join(self.write_info())

    def __repr__(self):
        return self.__str__()

    def get_info_list(self, edi_lines):
        """
        get a list of lines from the info section

        :param edi_lines: DESCRIPTION
        :type edi_lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        info_list = []
        info_find = False
        phoenix_list_02 = []

        for line in edi_lines:
            if ">info" in line.lower():
                info_find = True
                if len(line.strip().split()) > 1:
                    info_list.append(line.strip().split()[1])

            elif ">" in line[0:2]:
                # need to check for xml type formating
                if "<" in line:
                    pass
                else:
                    if info_find is True:
                        break
                    else:
                        pass

            elif info_find:
                if "maxinfo" in line.lower():
                    continue
                if (
                    line.lower().find("run information") >= 0
                    and line.lower().find("station") >= 0
                ):
                    self._phoenix_file = True
                elif "empower" in line.lower():
                    self._empower_file = True
                if self._phoenix_file and len(line) > self._phoenix_col_width:
                    info_list.append(line[0 : self._phoenix_col_width].strip())
                    phoenix_list_02.append(
                        line[self._phoenix_col_width :].strip()
                    )
                else:
                    line = line.strip()
                    if len(line) > 1:
                        if len(line) <= 3 and not line.isalnum():
                            continue
                        info_list.append(line)

        info_list += phoenix_list_02
        # validate the information list
        # empower has a specific format that cannot be sorted.
        if self._empower_file:
            info_list = self._validate_info_list(info_list, sort=False)

        else:
            info_list = self._validate_info_list(info_list, sort=True)
        return info_list

    def read_info(self, edi_lines):
        """
        read information section of the .edi file
        """

        self.info_dict = {}
        self.info_list = self.get_info_list(edi_lines)
        if self._empower_file:
            self.info_dict, self.info_list = self._read_empower_info(
                self.info_list
            )
        else:
            # make info items attributes of Information
            for ll in self.info_list:
                l_list = [None, ""]
                # phoenix has lat an lon information in the notes but separated by
                # a space instead of an = or :
                if (
                    "lat" in ll.lower()
                    or "lon" in ll.lower()
                    or "lng" in ll.lower()
                ):
                    l_list = ll.split()
                    if len(l_list) == 2:
                        self.info_dict[l_list[0]] = l_list[1]
                        continue
                    elif len(l_list) == 4:
                        self.info_dict[l_list[0]] = l_list[1]
                        self.info_dict[l_list[2]] = l_list[3]
                        continue
                    elif len(l_list) == 6:
                        self.info_dict[l_list[0]] = l_list[1] + l_list[2]
                        self.info_dict[l_list[3]] = l_list[4] + l_list[5]
                        continue

                # need to check if there is an = or : seperator, which ever
                # comes first is assumed to be the delimiter
                l_key, l_value = self._read_line(ll)
                if l_key:
                    self.info_dict[l_key] = l_value

        if not self._empower_file:
            self.parse_info()

        if self.info_list is None:
            self.logger.info("Could not read information")
            return

    def _read_empower_info(self, info_list):
        """
        read empower style information block.  Structured as

        Stations
         Electrics
          EX
          EY
         Magnetics
          HX
          HY
          HZ

        :param info_list: DESCRIPTION
        :type info_list: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        ch_key = {
            "e1": "ex",
            "e2": "ey",
            "h1": "hx",
            "h2": "hy",
            "h3": "hz",
        }

        info_dict = {}
        comp = None
        new_list = []
        for line in info_list:
            og_key, l_value = self._read_line(line)
            l_key = validate_name(og_key.lower())
            if l_value in [None]:
                comp = l_key
                if comp == "electrics":
                    comp = "data_logger"
                elif comp in ["ex", "ey", "hx", "hy", "hz"]:
                    comp = f"run.{comp}"
                continue
            elif l_value in [""]:
                continue
            else:
                if l_key in [
                    "station_name",
                    "min_value",
                    "max_value",
                    "detected_sensor_type",
                    "coordinates",
                    "gps_(min_-_max)",
                    "temperature_(min_-_max)",
                    "recording_id",
                ]:
                    continue
                try:
                    l_key = self.empower_translation_dict[l_key]
                except KeyError:
                    new_list.append(f"{l_key} = {l_value}")

                l_value = l_value.encode("ascii", "ignore").decode().lower()
                if l_value.count("[") >= 1 and l_value.count("]") >= 1:
                    l_value = l_value.split("[")[0].strip()
                if l_value.count("%") >= 0:
                    l_value = l_value.replace("%", "")
                if l_key in ["component"]:
                    l_value = ch_key[l_value]

                if comp:
                    if comp in ["run.hx", "run.hy", "run.hz"]:
                        if "ac" in l_key or "dc" in l_key:
                            continue

                    if "comments" in l_key:
                        og_key = validate_name(og_key.lower())
                        try:
                            info_dict[
                                f"{comp}.{l_key}"
                            ] += f",{og_key}={l_value}"
                        except KeyError:
                            info_dict[
                                f"{comp}.{l_key}"
                            ] = f"{og_key}={l_value}"

                    else:
                        info_dict[f"{comp}.{l_key}"] = l_value
                else:
                    info_dict[l_key.lower()] = l_value

        return info_dict, new_list

    def _get_separator(self, line):
        """
        get separator to split line

        :param line: DESCRIPTION
        :type line: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        sep = None
        if line.count(":") > 0 and line.count("=") > 0:
            if line.find(":") < line.find("="):
                sep = ":"
            else:
                sep = "="

        elif line.count(":") >= 1:
            sep = ":"
            # colon_find = line.find(":")
        elif line.count("=") >= 1:
            sep = "="

        return sep

    def _read_line(self, line):
        sep = self._get_separator(line)
        if sep:
            l_list = line.split(sep, 1)
            if len(l_list) == 2:
                l_key = l_list[0].strip()
                l_value = l_list[1].strip().replace('"', "")
                if l_value.find("[") > 0 and l_value.find("]") > 0:
                    if l_value.count(",") >= 1:
                        l_sep = ","
                    elif l_value.count(";") >= 1:
                        l_sep = ";"
                    elif l_value.count(":") >= 1:
                        l_sep = ":"
                    else:
                        l_sep = None
                    if l_sep:
                        l_value = (
                            l_value.replace("[", "")
                            .replace("[", "")
                            .split(l_sep)
                        )
                return l_key, l_value
            else:
                return l_key, ""
        else:
            return line, None

    def write_info(self, info_list=None):
        """
        write out information
        """

        if info_list is not None:
            self.info_list = self._validate_info_list(info_list)

        info_lines = [">INFO\n"]
        for line in sorted(list(set(self.info_list))):
            info_lines.append(f"{' '*4}{line}\n")

        return info_lines

    def _validate_info_list(self, info_list, sort=True):
        """
        check to make sure the info list input is valid, really just checking
        for Phoenix format where they put two columns in the file and remove
        any blank lines and the >info line
        """

        new_info_list = []
        # try to remove repeating lines
        if sort:
            info_list = sorted(list(set(info_list)))
        else:
            info_list = info_list
        for line in info_list:
            # get rid of empty lines
            lt = str(line).strip()
            if len(lt) > 1:
                if ">" in line:
                    pass
                else:
                    new_info_list.append(line.strip())

        return new_info_list

    def parse_info(self):
        """
        Try to parse the info section into useful information.
        :return: DESCRIPTION
        :rtype: TYPE

        """
        new_dict = {}
        processing_parameters = []
        for key, value in self.info_dict.items():
            if key is None:
                continue
            try:
                if self._phoenix_file:
                    new_key = self.phoenix_translation_dict[key.lower()]
                else:
                    new_key = self.translation_dict[key.lower()]

                if isinstance(new_key, list):
                    values = value.split(",")
                    if len(values) == len(new_key):
                        for vkey, item in zip(new_key, values):
                            item_value = (
                                item.lower().split("=")[1].replace("mv", "")
                            )
                            new_dict[vkey] = item_value
                    else:
                        self.logger.warning(f"Could not parse line {value}")
                        raise KeyError
                else:
                    if new_key == "processing_parameter":
                        processing_parameters.append(f"{key}={value}")
                    else:
                        if "pot resist" in key.lower():
                            new_dict[new_key] = value.split()[0]
                        elif key.lower().endswith("sen"):
                            comp = key.lower().split()[0]
                            new_dict[
                                f"{comp}.sensor.manufacturer"
                            ] = "Phoenix Geophysics"
                            new_dict[f"{comp}.sensor.type"] = "Induction Coil"
                            new_dict[new_key] = value
                        else:
                            new_dict[new_key] = value

                for item in self.info_list:
                    if key.lower() in item.lower():
                        self.info_list.remove(item)
                        break

            except KeyError:
                new_dict[key] = value

        if processing_parameters != []:
            new_dict[
                "transfer_function.processing_parameters"
            ] = processing_parameters

        self.info_dict = new_dict
