# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:18:29 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from copy import deepcopy

from mt_metadata.timeseries.stationxml.fdsn_tools import (
    make_channel_code, get_location_code, release_dict)

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml.utils import BaseTranslator

from obspy.core import inventory
# =============================================================================


class XMLNetworkMTSurvey(BaseTranslator):
    """
    translate back and forth between StationXML Network and MT Survey
    """

    def __init__(self):
        super().__init__()

        self.xml_translator.update(
            {
                "description": "summary",
                "comments": "comments",
                "start_date": "time_period.start",
                "end_date": "time_period.end",
                "restricted_status": "release_license",
                "operators": "special",
                "code": "fdsn.network",
                "alternate_code": "project",
                "identifiers": "citation_dataset.doi",
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["project_lead"] = "operator"
        self.mt_translator["name"] = "alternate_code"

    def network_to_survey(self, network):
        """
        Translate a StationXML Network object to MT Survey object

        :param network: StationXML network element
        :type network: :class:`obspy.core.inventory.Network`

        """

        if not isinstance(network, inventory.Network):
            msg = f"Input must be obspy.core.inventory.Network object not {type(network)}"
            self.logger.error(msg)
            raise ValueError(msg)

        mt_survey = metadata.Survey()

        for mt_key, sxml_key in self.mt_translator.items():
            if mt_key == "project_lead":
                author = []
                email = []
                org = []
                for operator in network.operators:
                    org.append(operator.agency)
                    for person in operator.contacts:
                        author.append(', '.join(person.names))
                        email.append(', '.join(person.emails))
                if author:
                    mt_survey.set_attr_from_name(
                        "project_lead.author", ', '.join(author))
                if email:
                    mt_survey.set_attr_from_name(
                        "project_lead.email", ', '.join(email))
                if org:
                    mt_survey.set_attr_from_name(
                        "project_lead.organization", ', '.join(org))
            elif mt_key in ["citation_dataset.doi"]:
                 mt_survey.set_attr_from_name(
                        mt_key, self.read_xml_identifier(network.identifiers)
                    )
                 
            elif mt_key in ["comments"]:
                for comment in network.comments:
                    key, value = self.read_xml_comment(comment)
                    key = key.split('mt.survey.')[1]
                    if 'summary' in key:
                        key = key.replace("summary", "comments")
                    if key in ["comments"]:
                        if mt_survey.comments:
                            mt_survey.comments += value
                        else:
                            mt_survey.comments = value
                    else:
                        mt_survey.set_attr_from_name(key, value)

            else:
                value = getattr(network, sxml_key)
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    for k, v in zip(mt_key, value):
                        mt_survey.set_attr_from_name(k, v)
                else:
                    if sxml_key == "restricted_status":
                        value = self.flip_dict(release_dict)[value]
                    if sxml_key in ["start_date", "end_date"]:
                        value = value.isoformat()

                mt_survey.set_attr_from_name(mt_key, value)
            

        return mt_survey
