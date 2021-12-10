# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:44:51 2021

@author: jpeacock
"""

def _validate_str_with_equals(input_string):
    """
    make sure an input string is of the format {0}={1} {2}={3} {4}={5} ...
    Some software programs put spaces after the equals sign and that's not
    cool.  So we make the string into a readable format

    :param input_string: input string from an edi file
    :type input_string: string

    :returns line_list: list of lines as ['key_00=value_00',
                                          'key_01=value_01']
    :rtype line_list: list
    """
    input_string = input_string.strip()
    # remove the first >XXXXX
    if ">" in input_string:
        input_string = input_string[input_string.find(" ") :]

    # check if there is a // at the end of the line
    if input_string.find("//") > 0:
        input_string = input_string[0 : input_string.find("//")]

    # split the line by =
    l_list = input_string.strip().split("=")

    # split the remaining strings
    str_list = []
    for line in l_list:
        s_list = line.strip().split()
        for l_str in s_list:
            str_list.append(l_str.strip())

    # probably not a good return
    if len(str_list) % 2 != 0:
        # _logger.info(
        #     'The number of entries in {0} is not even'.format(str_list))
        return str_list

    line_list = [
        "{0}={1}".format(str_list[ii], str_list[ii + 1])
        for ii in range(0, len(str_list), 2)
    ]

    return line_list

# ==============================================================================
# Index finder
# ==============================================================================
class index_locator(object):
    def __init__(self, component_list):
        self.ex = None
        self.ey = None
        self.hx = None
        self.hy = None
        self.hz = None
        self.rhx = None
        self.rhy = None
        self.rhz = None
        for ii, comp in enumerate(component_list):
            setattr(self, comp, ii)
        if self.rhx is None:
            self.rhx = self.hx
        if self.rhy is None:
            self.rhy = self.hy
            
    def __str__(self):
        lines = ["Index Values"]
        for k, v in self.__dict__.items():
            if v is not None:
                lines.append(f"\t{k} = {v}")
        return "\n".join(lines)
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def n_channels(self):
        count = 0
        for k, v in self.__dict__.items():
            if v is not None:
                count += 1
                
        return count
            
def _validate_edi_lines(edi_lines):
    """
    check for carriage returns or hard returns

    :param edi_lines: list of edi lines
    :type edi_lines: list

    :returns: list of edi lines
    :rtype: list
    """

    if len(edi_lines) == 1:
        edi_lines = edi_lines[0].replace("\r", "\n").split("\n")
        if len(edi_lines) > 1:
            return edi_lines
        else:
            raise ValueError("*** EDI format not correct check file ***")
    else:
        return edi_lines


