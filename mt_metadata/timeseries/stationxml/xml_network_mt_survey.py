# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:18:29 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

from mt_metadata import timeseries as metadata
from mt_metadata.base.helpers import requires

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.timeseries.stationxml.fdsn_tools import release_dict
from mt_metadata.timeseries.stationxml.utils import BaseTranslator

try:
    from obspy.core import inventory
except ImportError:
    inventory = None

# =============================================================================


@requires(obspy=inventory)
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
                "start_date": "time_period.start_date",
                "end_date": "time_period.end_date",
                "restricted_status": "release_license",
                "operators": "project_lead",
                "code": "fdsn.network",
                "identifiers": "citation_dataset.doi",
                "alternate_code": "id",
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["project_lead"] = "operators"
        self.mt_translator["name"] = "alternate_code"

        self.mt_comments_list = [
            "country",
            "geographic_name",
            "citation_journal.doi",
            "id",
            "project",
            "acquired_by.author",
            "acquired_by.comments.value",
        ]

    def xml_to_mt(self, network):
        """
        Translate a StationXML Network object to MT Survey object

        :param network: StationXML network element
        :type network: :class:`obspy.core.inventory.Network`

        """

        if not isinstance(network, inventory.Network):
            msg = (
                f"Input must be obspy.core.inventory.Network object not {type(network)}"
            )
            self.logger.error(msg)
            raise ValueError(msg)
        mt_survey = metadata.Survey()

        for mt_key, xml_key in self.mt_translator.items():
            if mt_key == "project_lead":
                name = []
                email = []
                org = []
                for operator in network.operators:
                    org.append(operator.agency)
                    for person in operator.contacts:
                        name.append(", ".join(person.names))
                        email.append(", ".join(person.emails))
                if name:
                    mt_survey.update_attribute("project_lead.author", ", ".join(name))
                if email:
                    mt_survey.update_attribute("project_lead.email", ", ".join(email))
                if org:
                    mt_survey.update_attribute(
                        "project_lead.organization", ", ".join(org)
                    )
            elif mt_key in ["citation_dataset.doi"]:
                mt_survey.update_attribute(
                    mt_key, self.read_xml_identifier(network.identifiers)
                )
            elif mt_key in ["comments"]:
                for comment in network.comments:
                    key, value = self.read_xml_comment(comment)
                    if "doi" in key:
                        # need to make a doi a proper web location.
                        if not value.startswith("http"):
                            if "doi.org" not in value:
                                value = f"https://doi.org/{value}"
                            else:
                                value = f"https://{value}"
                    if "mt.survey" in key:
                        key = key.split("mt.survey.")[1]
                        if "summary" in key:
                            key = key.replace("summary", "comments")
                        if key in ["comments"]:
                            if mt_survey.comments.value:
                                mt_survey.comments.value += f", {value}"
                            else:
                                mt_survey.comments.value = value
                        else:
                            mt_survey.update_attribute(key, value)
                    else:
                        if mt_survey.comments.value:
                            if not value in mt_survey.comments:
                                mt_survey.comments.value += f", {value}"
                        else:
                            mt_survey.comments.value = value
            else:
                value = getattr(network, xml_key)
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    for k, v in zip(mt_key, value):
                        mt_survey.update_attribute(k, v)
                else:
                    if xml_key == "restricted_status":
                        value = self.flip_dict(release_dict)[value]
                mt_survey.update_attribute(mt_key, value)
        if mt_survey.id in [None, ""]:
            mt_survey.id = mt_survey.fdsn.network

        mt_survey.update_all()
        return mt_survey

    def mt_to_xml(self, survey, code="ZU"):
        """
        Convert MT Survey to Obspy Network

        .. note:: For now the default code is ZU which is an IRIS catch-all network

        """

        if not isinstance(survey, metadata.Survey):
            msg = (
                f"Input must be mt_metadata.timeseries.Survey object not {type(survey)}"
            )
            self.logger.error(msg)
            raise ValueError(msg)
        network = inventory.Network(code)
        for inv_key, mt_key in self.xml_translator.items():
            if mt_key is None:
                msg = "cannot currently map Survey to network.{0}".format(inv_key)
                self.logger.debug(msg)
                continue
            if inv_key == "operators":
                if survey.project_lead.organization:
                    operator = inventory.Operator(
                        agency=survey.project_lead.organization
                    )
                    if survey.project_lead.author:
                        person = inventory.Person(
                            names=[survey.project_lead.author],
                            emails=[survey.project_lead.email],
                        )
                        operator.contacts = [person]
                    network.operators = [operator]
            elif inv_key == "comments":
                if survey.comments is not None:
                    comment = inventory.Comment(survey.comments)
                    network.comments.append(comment)
            elif inv_key == "restricted_status":
                network.restricted_status = release_dict[
                    survey.release_license.replace("-", "_")
                    .replace(" ", "_")
                    .replace(".", "_")
                    .replace("(", "_")
                    .replace(")", "_")
                    .replace("/", "_")
                    .replace(":", "_")
                ]
            elif inv_key == "identifiers":
                doi = survey.get_attr_from_name(mt_key)
                network.identifiers.append(f"DOI:{doi}")
            else:
                setattr(network, inv_key, survey.get_attr_from_name(mt_key))
        comments = self.make_mt_comments(survey, mt_key_base="mt.survey")
        network.comments = comments

        return network
