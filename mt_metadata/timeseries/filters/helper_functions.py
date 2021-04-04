import obspy

from mth5.utils.pathing import DATA_DIR


def load_sample_network_inventory(xml_file_handle, verbose=False):
    """
    """
    iris_dir = DATA_DIR.joinpath("iris")
    xml_file_path = iris_dir.joinpath(xml_file_handle)
    xml_file_path_str = xml_file_path.__str__()
    if verbose:
        print(f"Loading {xml_file_path_str}")
    inventory = obspy.read_inventory(xml_file_path_str)
    # inventory = obspy.read_inventory(xml_file_path.__str__())
    return inventory


def decimation_info_is_degenerate(obspy_stage):
    """
    Check a few condtions that may apply to an obspy stage which if true
    imply that the decimation information can be stripped out as it bears
    no information about aany data transformation;
    Case 1: All these attrs are None decimation has no information:
    {'decimation_input_sample_rate', 'decimation_factor',
    'decimation_offset', 'decimation_delay', 'decimation_correction'}
    Case 2:

    """
    cond1 = stage.stage_gain in [1.0, None]
    cond2 = stage.decimation_factor in [1, None]

    if cond1 & cond2:
        return True
    else:
        return False


def decimation_info_is_pure_delay(stage):
    cond1 = stage.stage_gain == 1.0
    cond2 = stage.decimation_factor == 1
    cond3 = stage.decimation_delay != 0.0
    cond4 = stage.decimation_correction == 0.0

    if cond1 & cond2 & cond3 & cond4:
        return True
    else:
        return False


def stage_gain_is_degenerate():
    # if gain is 1.0 ignore it
    pass
