import pytest
from mt_metadata.features.feature import Feature

class DummyFeature:
    def from_dict(self, d):
        self.called = True

def test_from_dict_success():
    f = Feature()
    f._supported_features = {"dummy": DummyFeature}
    d = {"name": "dummy", "param": 1}
    f.from_dict(d.copy())  # Use copy to avoid mutation

def test_from_dict_missing_name():
    f = Feature()
    f._supported_features = {"dummy": DummyFeature}
    d = {"param": 1}
    with pytest.raises(KeyError):
        f.from_dict(d.copy())

def test_all_supported_features_instantiable():
    f = Feature()
    for name, cls in f._supported_features.items():
        d = {"name": name}
        f.from_dict(d.copy())
