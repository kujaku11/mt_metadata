# from .band import Band
# from .channel import Channel
# from .channel_nomenclature import ChannelNomenclature
# from .decimation_level import DecimationLevel
# from .estimator import Estimator
# from .frequency_bands import FrequencyBands
# from .processing import Processing
# from .regression import Regression
# from .run import Run
# from .station import Station
# from .stations import Stations

# __all__ = [
#     "Band",
#     "Channel",
#     "ChannelNomenclature",
#     "Decimation",
#     "DecimationLevel",
#     "Estimator",
#     "FrequencyBands",
#     "Processing",
#     "Regression",
#     "Run",
#     "Station",
#     "Stations",
# ]

CHANNEL_NOMENCLATURES = {
    "default": {"hx": "hx", "hy": "hy", "hz": "hz", "ex": "ex", "ey": "ey"},
    "lemi12": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e1", "ey": "e2"},
    "lemi34": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e3", "ey": "e4"},
    "phoenix123": {"hx": "h1", "hy": "h2", "hz": "h3", "ex": "e1", "ey": "e2"},
    "musgraves": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "ex", "ey": "ey"},
}
