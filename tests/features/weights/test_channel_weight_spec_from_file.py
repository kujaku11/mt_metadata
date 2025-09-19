
import inspect
import json
import pathlib
import unittest


import mt_metadata
init_file = inspect.getfile(mt_metadata)
MT_METADATA_PATH = pathlib.Path(init_file).parent.parent
TEST_PATH = MT_METADATA_PATH.joinpath("tests")
TEST_HELPERS_PATH = MT_METADATA_PATH.joinpath("mt_metadata", "features", "test_helpers")


from mt_metadata.features.weights.channel_weight_spec import ChannelWeightSpec

class TestChannelWeightSpecFromFile(unittest.TestCase):
    def test_load_channel_weight_spec_from_json(self):
        # Path to the example JSON file
        json_path = TEST_HELPERS_PATH.joinpath("channel_weight_specs_example.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
        # If the file is a list or dict, adapt as needed
        channel_weight_specs = data.get('channel_weight_specs', data)
        for cws_dict in channel_weight_specs:
            cws = ChannelWeightSpec()
            cws.from_dict(cws_dict)
            self.assertIsInstance(cws, ChannelWeightSpec)
            self.assertTrue(hasattr(cws, 'feature_weight_specs'))
            self.assertGreaterEqual(len(cws.feature_weight_specs), 1)
        
if __name__ == "__main__":
    unittest.main()
