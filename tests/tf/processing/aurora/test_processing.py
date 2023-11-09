# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:46:46 2022

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import pandas as pd
import unittest

from mt_metadata.transfer_functions.processing.aurora import Processing

# =============================================================================


class TestProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        starts = ["2020-01-01T00:00:00", "2020-02-02T00:00:00"]
        ends = ["2020-01-31T12:00:00", "2020-02-28T12:00:00"]

        data_list = []
        for ii in range(3):
            for start, end in zip(starts, ends):
                entry = {
                    "station_id": "mt01",
                    "run_id": f"{ii:03}",
                    "start": start,
                    "end": end,
                    "mth5_path": r"/home/mth5_path.h5",
                    "sample_rate": 10,
                    "input_channels": ["hx", "hy"],
                    "output_channels": ["hz", "ex", "ey"],
                    "remote": False
                }

                data_list.append(entry)

                rr_entry_01 = {
                    "station_id": "rr01",
                    "run_id": f"{ii:03}",
                    "start": start,
                    "end": end,
                    "mth5_path": r"/home/mth5_path.h5",
                    "sample_rate": 10,
                    "input_channels": ["hx", "hy"],
                    "output_channels": ["hz", "ex", "ey"],
                    "remote": True
                }
                data_list.append(rr_entry_01)

                rr_entry_02 = {
                    "station_id": "rr02",
                    "run_id": f"{ii:03}",
                    "start": start,
                    "end": end,
                    "mth5_path": r"/home/mth5_path.h5",
                    "sample_rate": 10,
                    "input_channels": ["hx", "hy"],
                    "output_channels": ["hz", "ex", "ey"],
                    "remote": True
                }
                data_list.append(rr_entry_02)
        data_list = data_list
        df = pd.DataFrame(data_list)
        df.start = pd.to_datetime(df.start)
        df.end = pd.to_datetime(df.end)
        self.df = df


    def test_stations_to_dataframe(self):
        """ This could be moved under test_statons.py"""
        p = Processing()
        p.stations.from_dataset_dataframe(self.df)
        df = p.stations.to_dataset_dataframe()
        assert len(df) == len(self.df)


if __name__ == "__main__":
    unittest.main()
