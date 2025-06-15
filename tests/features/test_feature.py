import pytest
from mt_metadata.features.feature import Feature

class DummyFeature:
    def from_dict(self, d):
        self.called = True

# Patch _make_supported_features_dict to use DummyFeature for testing
def test_from_dict_success(monkeypatch):
    def dummy_dict():
        return {"dummy": DummyFeature}
    monkeypatch.setattr("mt_metadata.features.feature._make_supported_features_dict", dummy_dict)
    f = Feature()
    d = {"name": "dummy", "param": 1}
    f.from_dict(d)
    # No exception means success

def test_from_dict_missing_name(monkeypatch):
    def dummy_dict():
        return {"dummy": DummyFeature}
    monkeypatch.setattr("mt_metadata.features.feature._make_supported_features_dict", dummy_dict)
    f = Feature()
    d = {"param": 1}
    with pytest.raises(KeyError):
        f.from_dict(d)
