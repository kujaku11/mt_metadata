# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 13:53:55 2021

@author: jpeacock
"""
import numpy as np
from xml.etree import cElementTree as et


class TransferFunction:
    """
    Deal with the complex XML format
    """

    def __init__(self):
        self.index_dict = {"hx": 0, "hy": 1, "ex": 0, "ey": 1, "hz": 0}
        self.dtype_dict = {
            "complex": complex,
            "real": float,
            "complex128": "complex",
            "float64": "real"}
        self.units_dict = {"z": "[mV/km]/[nT]", "t": "[]"}
        self.name_dict = {
            "exhx": "zxx",
            "exhy": "zxy",
            "eyhx": "zyx",
            "eyhy": "zyy",
            "hzhx": "tx",
            "hzhy": "ty",
            }
        

        self.periods = None
        self.z = None
        self.z_var = None
        self.z_invsigcov = None
        self.z_residcov = None
        self.t = None
        self.t_var = None
        self.t_invsigcov = None
        self.t_residcov = None

        self.array_dict = {
            "z": self.z,
            "z_var": self.z_var,
            "z_invsigcov": self.z_invsigcov,
            "z_residcov": self.z_residcov,
            "t": self.t,
            "t_var": self.t_var,
            "t_invsigcov": self.t_invsigcov,
            "t_residcov": self.t_residcov,
        }
        self.write_dict = {
            "z": {"out": {0: 'ex', 1: "ey"}, "in": {0: "hx", 1: "hy"}},
            "z_var": {"out": {0: 'ex', 1: "ey"}, "in": {0: "hx", 1: "hy"}},
            "z_invsigcov": {"out": {0: 'hx', 1: "hy"}, "in": {0: "hx", 1: "hy"}},
            "z_residcov": {"out": {0: 'ex', 1: "ey"}, "in": {0: "ex", 1: "ey"}},
            "t": {"out": {0: 'hz'}, "in": {0: "hx", 1: "hy"}},
            "t_var": {"out": {0: 'hz'}, "in": {0: "hx", 1: "hy"}},
            "t_invsigcov": {"out": {0: 'hx', 1: "hy"}, "in": {0: "hx", 1: "hy"}},
            "t_residcov": {"out": {0: 'hz'}, "in": {0: "hz"}},
        }

    def initialize_arrays(self, n_periods):
        self.periods = np.zeros(n_periods)
        self.z = np.zeros((n_periods, 2, 2), dtype=np.complex)
        self.z_var = np.zeros_like(self.z, dtype=np.float)
        self.z_invsigcov = np.zeros_like(self.z, dtype=np.complex)
        self.z_residcov = np.zeros_like(self.z, dtype=np.complex)
        self.t = np.zeros((n_periods, 1, 2), dtype=np.complex)
        self.t_var = np.zeros_like(self.t, dtype=np.float)
        self.t_invsigcov = np.zeros((n_periods, 2, 2), dtype=np.complex)
        self.t_residcov = np.zeros((n_periods, 1, 1), dtype=np.complex)

        self.array_dict = {
            "z": self.z,
            "z_var": self.z_var,
            "z_invsigcov": self.z_invsigcov,
            "z_residcov": self.z_residcov,
            "t": self.t,
            "t_var": self.t_var,
            "t_invsigcov": self.t_invsigcov,
            "t_residcov": self.t_residcov,
        }

    def get_n_periods(self, root_dict):
        self.n_periods = int(float((root_dict["data"]["count"].strip())))
        self.initialize_arrays(self.n_periods)

    def read_block(self, block, period_index):
        """
        Read a period block which is root_dict["data"]["period"][ii]

        :param block: DESCRIPTION
        :type block: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        for key in block.keys():
            comp = key.replace("_", "").replace(".", "_")
            if comp in ["value"]:
                continue
            try:
                dtype = self.dtype_dict[block[key]["type"]]
            except KeyError:
                dtype = float
            value_list = block[key]["value"]
            if not isinstance(value_list, list):
                value_list = [value_list]
            for item in value_list:
                index_0 = self.index_dict[item["output"].lower()]
                index_1 = self.index_dict[item["input"].lower()]
                if dtype is complex:
                    value = item["value"].split()
                    value = dtype(float(value[0]), float(value[1]))
                else:
                    value = dtype(item["value"])
                self.array_dict[comp][period_index, index_0, index_1] = value

    def read_data(self, root_dict):
        """
        read root_dict["data"]
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.get_n_periods(root_dict)
        for ii, block in enumerate(root_dict["data"]["period"]):
            self.periods[ii] = float(block["value"])
            self.read_block(block, ii)
            
    def write_block(self, parent, index):
        """
        Write a data block
        
        :param parent: DESCRIPTION
        :type parent: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        period_element = et.SubElement(
            parent, "Period", {"value": self.period[index], "units":"secs"})
        
        for key in self.array_dict.keys():
            arr = self.array_dict[key][index]
            attr_dict = {
                "type": self.dtype_dict[arr.dtype.name], 
                "size": str(arr.shape)[1:-1].replace(',', '')
                }
            try:
                attr_dict["units"] = self.units_dict[key]
            except KeyError:
                pass
            
            comp_element = et.SubElement(period_element, key, attr_dict)
            idx_dict = self.write_dict[key]
            for ii in arr.shape[0]:
                for jj in arr.shape[1]:
                    ch_out = idx_dict[ii]
                    ch_in = idx_dict[jj]
                    a_dict = {}
                    try:
                        a_dict["name"] = self.name_dict[ch_out + ch_in]
                    except KeyError:
                        
                    comp_element = et.SubElement(
                        comp_element,
                        "value",
                        attr_dict)
                    
                    
        
        
