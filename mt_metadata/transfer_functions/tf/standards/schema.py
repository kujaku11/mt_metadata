# -*- coding: utf-8 -*-
"""
=======================
schema
=======================

Convenience Classes and Functions to deal with the base metadata standards
described by the csv file.

The hope is that only the csv files will need to be changed as the standards
are modified.  The attribute dictionaries are stored in ATTRICT

Created on Wed Apr 29 11:11:31 2020

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from copy import deepcopy
import logging

from mt_metadata.base import BaseDict
from mt_metadata.utils.exceptions import MTSchemaError
from . import SCHEMA_FN_PATHS

# =============================================================================
# Schema standards
# =============================================================================
class Standards:
    """
    Helper container to read in csv files and make the appropriate
    dictionaries used in metadata.

    The thought is that only the csv files need to be changed if there is
    a change in standards.

    """

    def __init__(self):

        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.debug("Initiating Standards")
                          
    def get_schema_fn(self, schema_element):
        """
        Get the correct file name for the given schema element from the provided
        list of valid file names
        
        :param schema_element: name of the schema element to get filename for
        :type schema_element: string
        :return: correct file name for given element
        :rtype: :class:`pathlib.Path`

        """
        for fn in SCHEMA_FN_PATHS:
            if schema_element == fn.stem:
                return fn
        msg = f"Could not find schema element {schema_element} file name."
        self.logger.error(msg)
        raise MTSchemaError(msg)
        
    def get_schema(self, schema_element):
        """
        Get a :class:`mt_metadata.schema_base.BaseDict` object of the element
        
        :param schema_element: name of the schema element to get filename for
        :type schema_element: string
        :return: return a dictionary that describes the standards for the element
        :rtype: :class:`mt_metadata.schema_base.BaseDict`

        """
        
        schema_fn = self.get_schema_fn(schema_element)
        element_dict = BaseDict()
        element_dict.from_json(schema_fn)
        
        return element_dict

    @property
    def declination_dict(self):
        return self.get_schema("declination")

    @property
    def instrument_dict(self):
        return self.get_schema("instrument")

    @property
    def fdsn_dict(self):
        return self.get_schema("fdsn")

    @property
    def rating_dict(self):
        return self.get_schema("rating")

    @property
    def data_quality_dict(self):
        dq_dict = self.get_schema("data_quality")
        dq_dict.add_dict(self.rating_dict.copy(), "rating")
        return dq_dict

    @property
    def citation_dict(self):
        return self.get_schema("citation")

    @property
    def comment_dict(self):
        return self.get_schema("comment")

    @property
    def copyright_dict(self):
        return self.get_schema("copyright")

    @property
    def person_dict(self):
        return self.get_schema("person")

    @property
    def software_dict(self):
        return self.get_schema("software")

    @property
    def diagnostic_dict(self):
        return self.get_schema("diagnostic")

    @property
    def battery_dict(self):
        return self.get_schema("battery")

    @property
    def orientation_dict(self):
        return self.get_schema("orientation")

    @property
    def timing_system_dict(self):
        return self.get_schema("timing_system")

    @property
    def time_period_dict(self):
        return self.get_schema("time_period")

    @property
    def filtered_dict(self):
        """This one is for the channel metadata to define applied or not"""
        return self.get_schema("filtered")

    @property
    def filter_dict(self):
        """This one is for the actual filter metadata"""
        return self.get_schema("filter")

    @property
    def location_dict(self):
        location_dict = self.get_schema("location")
        location_dict.add_dict(self.declination_dict.copy(), "declination")

        return location_dict

    @property
    def provenance_dict(self):
        provenance_dict = self.get_schema("provenance")
        provenance_dict.add_dict(self.software_dict.copy(), "software")
        provenance_dict.add_dict(self.person_dict.copy(), "person")
        return provenance_dict

    @property
    def datalogger_dict(self):
        dl_dict = self.instrument_dict.copy()
        dl_dict.add_dict(self.timing_system_dict.copy(), "timing_system")
        dl_dict.add_dict(self.software_dict.copy(), "firmware")
        dl_dict.add_dict(self.battery_dict.copy(), "power_source")
        return dl_dict

    @property
    def electrode_dict(self):
        elec_dict = self.get_schema("instrument")
        for key, v_dict in self.location_dict.items():
            if "declination" not in key:
                elec_dict.update({key: v_dict})
        return elec_dict

    @property
    def transfer_function_dict(self):
        tf_dict = self.get_schema("transfer_function")
        tf_dict.add_dict(self.software_dict.copy(), "software")
        tf_dict.add_dict(self.person_dict, "processed_by")
        return tf_dict

    @property
    def survey_dict(self):
        survey_dict = self.get_schema("survey")
        survey_dict.add_dict(self.fdsn_dict, "fdsn")
        survey_dict.add_dict(
            self.person_dict.copy(), "acquired_by", keys=["author", "comments"]
        )
        survey_dict.add_dict(self.citation_dict.copy(), "citation_dataset")
        survey_dict.add_dict(self.citation_dict.copy(), "citation_journal")
        survey_dict.add_dict(
            self.location_dict.copy(),
            "northwest_corner",
            keys=["latitude", "longitude"],
        )
        survey_dict.add_dict(
            self.location_dict.copy(),
            "southeast_corner",
            keys=["latitude", "longitude"],
        )
        survey_dict.add_dict(
            self.person_dict.copy(),
            "project_lead",
            keys=["author", "email", "organization"],
        )
        survey_dict.add_dict(self.copyright_dict.copy(), None)
        return survey_dict

    @property
    def station_dict(self):
        station_dict = self.get_schema("station")
        station_dict.add_dict(self.fdsn_dict, "fdsn")
        station_dict.add_dict(self.location_dict.copy(), "location")
        station_dict.add_dict(
            self.person_dict.copy(), "acquired_by", keys=["author", "comments"]
        )
        station_dict.add_dict(self.orientation_dict.copy(), "orientation")
        station_dict.add_dict(
            self.provenance_dict.copy(),
            "provenance",
            keys=["comments", "creation_time", "log"],
        )
        station_dict.add_dict(self.software_dict.copy(), "provenance.software")
        station_dict.add_dict(
            self.person_dict.copy(),
            "provenance.submitter",
            keys=["author", "email", "organization"],
        )
        station_dict.add_dict(self.time_period_dict.copy(), "time_period")
        station_dict.add_dict(self.transfer_function_dict.copy(), "transfer_function")
        return station_dict

    @property
    def run_dict(self):
        run_dict = self.get_schema("run")
        run_dict.add_dict(self.fdsn_dict, "fdsn")
        run_dict.add_dict(self.datalogger_dict.copy(), "data_logger")
        run_dict.add_dict(self.time_period_dict.copy(), "time_period")
        run_dict.add_dict(
            self.person_dict.copy(), "acquired_by", keys=["author", "comments"]
        )
        run_dict.add_dict(
            self.person_dict.copy(), "metadata_by", keys=["author", "comments"]
        )
        run_dict.add_dict(
            self.provenance_dict.copy(), "provenance", keys=["comments", "log"]
        )
        run_dict.add_dict(self.electric_dict, "ex")
        run_dict.add_dict(self.electric_dict, "ey")
        run_dict.add_dict(self.magnetic_dict, "hx")
        run_dict.add_dict(self.magnetic_dict, "hy")
        run_dict.add_dict(self.magnetic_dict, "hz")
        run_dict.add_dict(self.magnetic_dict, "rrhx")
        run_dict.add_dict(self.magnetic_dict, "rrhy")
        run_dict.add_dict(self.auxiliary_dict, "temperature")
        return run_dict

    @property
    def channel_dict(self):
        channel_dict = self.get_schema("channel")
        channel_dict.add_dict(self.data_quality_dict.copy(), "data_quality")
        channel_dict.add_dict(self.filtered_dict.copy(), "filter")
        channel_dict.add_dict(self.time_period_dict.copy(), "time_period")
        channel_dict.add_dict(self.instrument_dict.copy(), "sensor")
        channel_dict.add_dict(self.fdsn_dict, "fdsn")
        for key, v_dict in self.location_dict.items():
            if "declination" not in key:
                channel_dict.update({"{0}.{1}".format("location", key): v_dict})
        return channel_dict

    @property
    def auxiliary_dict(self):
        return self.channel_dict

    @property
    def electric_dict(self):
        electric_dict = self.get_schema("electric")
        electric_dict.add_dict(self.get_schema("channel"))
        electric_dict.add_dict(self.data_quality_dict.copy(), "data_quality")
        electric_dict.add_dict(self.filtered_dict.copy(), "filter")
        electric_dict.add_dict(self.electrode_dict.copy(), "positive")
        electric_dict.add_dict(self.electrode_dict.copy(), "negative")
        electric_dict.add_dict(self.time_period_dict.copy(), "time_period")
        return electric_dict

    @property
    def magnetic_dict(self):
        magnetic_dict = self.get_schema("magnetic")
        magnetic_dict.add_dict(self.channel_dict.copy())
        return magnetic_dict

    @property
    def xml_site(self):
        site_dict = self.get_schema("station")
        site_dict.add_dict(self.location_dict.copy(), "location")
        return site_dict

    @property
    def ATTR_DICT(self):
        keys = [fn.stem for fn in SCHEMA_FN_PATHS] + ["electrode"]
        return dict(
            [(key, deepcopy(getattr(self, "{0}_dict".format(key)))) for key in keys]
        )
        self.logger.debug("Successfully made ATTR_DICT")

    def summarize_standards(
        self, levels=["survey", "station", "run", "auxiliary", "electric", "magnetic"]
    ):
        """
        Summarize the metadata definitions
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        summary_dict = BaseDict()
        for name in levels:
            summary_dict.add_dict(getattr(self, "{0}_dict".format(name)), name)

        return summary_dict
