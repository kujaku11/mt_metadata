from mt_metadata.features.feature import Feature

class FeatureFC(Feature):
    """
    Stub feature class for feature_fc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "feature_fc"
        self.add_base_attribute(
            "name",
            "feature_fc",
            {
                "type": str,
                "required": True,
                "style": "free form",
                "description": "Name of the feature (feature_fc)",
                "units": None,
                "options": [],
                "alias": [],
                "example": "feature_fc",
                "default": "feature_fc",
            },
        )
