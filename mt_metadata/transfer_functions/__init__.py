from .core import TF

__all__ = ["TF"]

# Define allowed sets of channel labellings
STANDARD_INPUT_CHANNELS = [
    "hx",
    "hy",
]
STANDARD_OUTPUT_CHANNELS = [
    "ex",
    "ey",
    "hz",
]

channel_maps = {
    "default": {"hx": "hx", "hy": "hy", "hz": "hz", "ex": "ex", "ey": "ey"},
    "lemi12": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e1", "ey": "e2"},
    "lemi34": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e3", "ey": "e4"},
    "phoenix123": {"hx": "h1", "hy": "h2", "hz": "h3", "ex": "e1", "ey": "e2"},
    "musgraves": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "ex", "ey": "ey"},
}


def load_channel_maps():
    """
    :return: Keys are the channel_nomenclature schema keywords.
     Values are dictionaries which map the STANDARD_INPUT_NAMES, \
     STANDARD_OUTPUT_NAMES to the channel names associated with a given
     channel nomenclature
    :rtype: dict
    """
    import json
    import pathlib

    fn = pathlib.Path(__file__).parent.joinpath(
        "standards", "channel_nomenclatures.json"
    )
    with open(fn) as f:
        channel_maps = json.loads(f.read())
    return channel_maps


CHANNEL_MAPS = load_channel_maps()


def get_allowed_channel_names(standard_names):
    """
    :param standard_names: one of STANDARD_INPUT_NAMES, or STANDARD_OUTPUT_NAMES
    :type standard_names: list
    :return: allowed_names: list of channel names that are supported
    :rtype: list
    """
    allowed_names = []
    for ch in standard_names:
        for _, channel_map in CHANNEL_MAPS.items():
            allowed_names.append(channel_map[ch])
    allowed_names = list(set(allowed_names))
    return allowed_names


ALLOWED_INPUT_CHANNELS = get_allowed_channel_names(STANDARD_INPUT_CHANNELS)
ALLOWED_OUTPUT_CHANNELS = get_allowed_channel_names(STANDARD_OUTPUT_CHANNELS)
