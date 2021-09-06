# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 13:53:55 2021

@author: jpeacock
"""
import numpy as np

class TransferFunction:
    """
    Deal with the complex XML format
    """
    
    def __init__(self):
        self.index_dict = {"hx": 0, "hy": 1, "ex": 0, "ey": 1, "hz": 0}
        self.dtype_dict = {"complex": complex, "real": float}
        
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
            "t_residcov": self.t_residcov}
    
    def initialize_arrays(self, n_periods):
        self.periods = np.zeros(n_periods)
        self.z = np.zeros((n_periods, 2, 2), dtype=np.complex)
        self.z_var = np.zeros_like(self.z, dtype=np.float)
        self.z_invsigcov = np.zeros_like(self.z, dtype=np.complex)
        self.z_residcov =  np.zeros_like(self.z, dtype=np.complex)
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
            "t_residcov": self.t_residcov}
        
    def get_n_periods(self, root_dict):
        self.n_periods = int(root_dict["data"]["count"])
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
            
            
                    
                
            
        
        
        
        