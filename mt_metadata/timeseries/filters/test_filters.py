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

from mt_metadata.timeseries.filters.channel_response_filter import ChannelResponseFilter
from mt_metadata.timeseries.filters.helper_functions import load_sample_network_inventory
from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage


def create_filter_for_channel():
    #this combines all stages in channel to a single filter.
    pass

def test_filter_generation_from_xml_via_obspy(inventory):
    """
    inventory: obspy.core.inventory.network.Network


    Returns
    -------

    """
    networks = inventory
    for network in networks:
        if not isinstance(network, obspy.core.inventory.network.Network):
            print("Expected a Network, got a {}".format(type(network)))
            raise Exception
        for station in network:
            for channel in station:
                response = channel.response
                print(type(response))
                stages = response.response_stages
                info = '{}-{}-{} {}-stage response'.format(network.code, station.code, channel.code, len(stages))
                print(info)
                filters_list = []
                for i_stage, stage in enumerate(stages):
                    print('Stage {} \n\n {}'.format(i_stage, stage))
                    i_filter = create_filter_from_stage(stage)
                    filters_list.append(i_filter)

                for fltr in filters_list:
                    print(fltr.type)
                    frequencies = np.logspace(-3,3,200)
                    #fltr.plot_complex_response(frequencies)
                    #fltr.plot_response(None, x_units='frequency')
                channel_response = ChannelResponseFilter(filters_list=filters_list)
                print('ok')
            print(network)

    print('ok')

def main():
    """
    """
    station_xml_filehandle = 'ZU_20210212.xml'
    station_xml_filehandle = 'fdsn-station_2021-03-09T04_44_51.xml'
    inventory = load_sample_network_inventory(station_xml_filehandle, verbose=True)
    test_filter_generation_from_xml_via_obspy(inventory)
    print("finito {}".format(datetime.datetime.now()))

if __name__ == "__main__":
    main()

