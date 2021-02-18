"""

When about to make commits, try ~/software/irismt/mt_metadata/tests/pytest test*

2021-02-14
Test to instantite some filters based in StationXML inputs.

Notes:
    1. In this example I have we are receiving a Network level XML and we need to iterate
    through it to get the stations, channels and stages.   In general we will need a 
    methods that work with these XMLs and iterate through them.
    
    It looks like obspy's Inventory() chunks the StationXML stages up nicely.
    Moreover we can use instance checks (eg isinstance() as way to confirm we are 
    getting what we think we are getting, 
    
    2. It looks like stage.__dict__ is pretty comprehensive, but I dont like how it passes 
    poles as _poles and zeros as _zeros.   
    Actually, here's the thing, our filter class looks like it could just wrap the stage

    3. Obspy contributions?  Do we want to contribute fap table readers for StationXML to obspy?


ToDo: 
-test ZerosPolesGainContinuous vs ZerosPolesGainDiscrete
(in one case we add a 'dt' as a kwarg)

20210216:
1. Revisit base class
2. continue on implementation
3. Set a call With Anna


"""
import datetime
import numpy as np
import obspy
import path

import scipy.signal as signal

from mt_metadata.filters.pole_zero_filter import PoleZeroFilter
from mt_metadata.filters.obspy_stages import create_filter_from_stage
from mth5.utils.pathing import DATA_DIR

from plotting_helpers import plot_response



def load_sample_network_inventory():
    """
    """
    iris_dir = DATA_DIR.joinpath('iris')
    xml_file_path = iris_dir.joinpath('ZU.xml')
    inventory = obspy.read_inventory(xml_file_path.__str__())
    return inventory




def create_filter_for_channel():
    #this combines all stages in channel to a single filter.
    pass

def test_filter_generation():
    """
    we probably want to
    Returns
    -------

    """
    networks = load_sample_network_inventory()
    for network in networks:
        if not isinstance(network, obspy.core.inventory.network.Network):
            print("Expected a Network, got a {}".format(type(network)))
            raise Exception
        for station in network:
            for channel in station:
                response = channel.response
                stages = response.response_stages
                info = '{}-{}-{} {}-stage response'.format(network.code, station.code, channel.code, len(stages))
                print(info)
                filters_list = []
                for stage in stages:
                    # pass
                    print('stage {}'.format(stage))
                    filter = create_filter_from_stage(stage)
                    filters_list.append(filter)

            print(network)
    print('ok')
#        if not isinstance(network, obspy.core.)

def main():
    """
    """
    test_filter_generation()
    print("finito {}".format(datetime.datetime.now()))

if __name__ == "__main__":
    main()

