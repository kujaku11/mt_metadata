
# =============================================================================
# Imports
# =============================================================================
import unittest

import numpy as np
from mt_metadata.timeseries.filters.filtered import Filtered
from mt_metadata.utils.exceptions import MTSchemaError
# =============================================================================


class TestFiltered(unittest.TestCase):
    # @classmethod
    # def setUpClass(self):
    #     self.filtered = Filtered
    #     self.m = MTH5()
    #     self.m.open_mth5(self.wd.joinpath("test.h5"), mode="a")

    def test_initialize(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01", "filter_02", "filter_03"]
        filtered_obj.applied = [True, False, True]
        self.assertIsInstance(filtered_obj, Filtered)

    def test_consistency_check(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01", "filter_02", "filter_03"]
        filtered_obj.applied = [True, False]
        check = filtered_obj._check_consistency()
        self.assertFalse(check)

    def test_accepts_0_for_false(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01",]
        filtered_obj.applied = 0
        filtered_obj.applied = "0"

    def test_accepts_string_list(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01","filter_02",]
        filtered_obj.applied = "[0,0]"

    def test_accepts_list_of_strings(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01","filter_02",]
        filtered_obj.applied = ["0","1"]

    def test_accepts_list_of_bool_ints(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01","filter_02",]
        filtered_obj.applied = [0,1]
        check = filtered_obj._check_consistency()
        print(f"check {check}")

    def test_accepts_numpy_array(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01","filter_02",]
        filtered_obj.applied = np.array([0,1])
        filtered_obj.applied = np.array([True, False])
        check = filtered_obj._check_consistency()
        self.assertTrue(check)

        print(f"check {check}")

    def test_empty_numpy_array_same_as_empyt_list(self):
        filtered_obj_1 = Filtered()
        filtered_obj_1.applied = []
        filtered_obj_2 = Filtered()
        filtered_obj_2.applied = np.array([])
        self.assertEquals(filtered_obj_2, filtered_obj_1)

    def test_raises_schema_error(self):
        filtered_obj = Filtered()
        filtered_obj.name = ["filter_01"]
        with self.assertRaises(MTSchemaError):
            filtered_obj.applied = {0}

    def test_none_is_same_as_default(self):
        filtered_obj_1 = Filtered()
        filtered_obj_1.name = ["filter_01", "filter_02", "filter_03"]
        filtered_obj_1.applied = [None, None, None]
        filtered_obj_2 = Filtered()
        filtered_obj_2.name = ["filter_01", "filter_02", "filter_03"]
        filtered_obj_2.applied = [True, True, True]
        self.assertEquals(filtered_obj_2, filtered_obj_1)


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
