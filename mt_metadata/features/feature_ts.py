from mt_metadata.features.base_feature import BaseFeature

class FeatureTS(BaseFeature):
    """
    Stub feature class for time series features.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "feature_ts"
        self.add_base_attribute(
            "name",
            "feature_ts",
            {
                "type": str,
                "required": True,
                "style": "free form",
                "description": "Name of the feature (time series)",
                "units": None,
                "options": [],
                "alias": [],
                "example": "feature_ts",
                "default": "feature_ts",
            },
        )