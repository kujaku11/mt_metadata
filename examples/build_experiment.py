# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:47:21 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

from mt_metadata.timeseries import (
    Auxiliary, Electric, Magnetic, Run, Station, Survey, Experiment)

experiment = Experiment()

for survey in ["One", "Two"]:
    survey_obj = Survey(survey_id=survey)
    for station in ["mt01", "mt02"]:
        station_obj = Station(id=station)
        for run in ["mt01a", "mt01b"]:
            run_obj = Run(id=run)
            for ch in ["ex", "ey"]:
                ch_obj = Electric(component=ch)
                run_obj.channels.append(ch_obj)
            for ch in ["hx", "hy", "hz"]:
                ch_obj = Magnetic(component=ch)
                run_obj.channels.append(ch_obj)
            for ch in ["temperature", "voltage"]:
                ch_obj = Auxiliary(component=ch)
                run_obj.channels.append(ch_obj)

            station_obj.runs.append(run_obj)
        survey_obj.stations.append(station_obj)

    experiment.surveys.append(survey_obj)

experiment_xml = experiment.to_xml(fn=r"c:\Users\jpeacock\test_experiment.xml")