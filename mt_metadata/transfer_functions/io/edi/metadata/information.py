# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 14:13:37 2021

@author: jpeacock
"""

from mt_metadata.utils.mt_logger import setup_logger

# ==============================================================================
# Info object
# ==============================================================================
class Information(object):
    """
    Contain, read, and write info section of .edi file

    not much to really do here, but just keep it in the same format that it is
    read in as, except if it is in phoenix format then split the two paragraphs
    up so they are sequential.

    """

    def __init__(self, fn=None, edi_lines=None):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")

        self.info_list = []
        self.info_dict = {}
        self._phoenix_col_width = 38
        self._phoenix_file = False
        
        
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
            "operator": "station.acquired_by.author",
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
            "rotmaxe": "processing_parameter"}
        
        

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
                if line.lower().find("run information") >= 0 and line.lower().find("station") >= 0:
                    self._phoenix_file = True
                if self._phoenix_file and len(line) > self._phoenix_col_width:
                    info_list.append(line[0 : self._phoenix_col_width].strip())
                    phoenix_list_02.append(line[self._phoenix_col_width :].strip())
                else:
                    line = line.strip()
                    if len(line) > 1:
                        if len(line) <=3 and not line.isalnum():
                            continue
                        info_list.append(line)

        info_list += phoenix_list_02
        # validate the information list
        info_list = self._validate_info_list(info_list)

        return info_list

    def read_info(self, edi_lines):
        """
        read information section of the .edi file
        """

        self.info_dict = {}
        self.info_list = self.get_info_list(edi_lines)
        # make info items attributes of Information
        for ll in self.info_list:
            l_list = [None, ""]
            # phoenix has lat an lon information in the notes but separated by
            # a space instead of an = or :
            if "lat" in ll.lower() or "lon" in ll.lower() or "lng" in ll.lower():
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
            sep = None
            if ll.count(":") > 0 and ll.count("=") > 0:
                if ll.find(":") < ll.find("="):
                    sep = ":"
                else:
                    sep = "="

            elif ll.count(":") >= 1:
                sep = ":"
                # colon_find = ll.find(":")
            elif ll.count("=") >= 1:
                sep = "="
                
            if sep:
                l_list = ll.split(sep, 1)
                if len(l_list) == 2:
                    l_key = l_list[0].strip()
                    l_value = l_list[1].strip().replace('"', "")
                    self.info_dict[l_key] = l_value

            else:
                self.info_dict[l_list[0]] = None
                
        self.parse_info()

        if self.info_list is None:
            self.logger.info("Could not read information")
            return

    def write_info(self, info_list=None):
        """
        write out information
        """

        if info_list is not None:
            self.info_list = self._validate_info_list(info_list)

        info_lines = [">INFO\n"]
        for line in self.info_list:
            info_lines.append(f"{' '*4}{line}\n")

        return info_lines

    def _validate_info_list(self, info_list):
        """
        check to make sure the info list input is valid, really just checking
        for Phoenix format where they put two columns in the file and remove
        any blank lines and the >info line
        """

        new_info_list = []
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
                    values = value.split(',')
                    if len(values) == len(new_key):
                        for vkey, item in zip(new_key, values):
                            item_value = item.lower().split("=")[1].replace("mv", "")
                            new_dict[vkey] = item_value
                    else:
                        self.logger.warngin("could not parse line %s", value)
                        raise KeyError
                else:        
                    if new_key == "processing_parameter":
                        processing_parameters.append(f"{key}={value}")
                    else:
                        if "pot resist" in key.lower():
                            new_dict[new_key] = value.split()[0]
                        else:
                            new_dict[new_key] = value
                        
                    
                        
                for item in self.info_list:
                    if key.lower() in item.lower():
                        self.info_list.remove(item)
                        break
                    
            except KeyError:
                new_dict[key] = value
        
        if processing_parameters != []:
            new_dict["transfer_function.processing_parameters"] = processing_parameters
                
        self.info_dict = new_dict
                    
                
            
            
        
        
