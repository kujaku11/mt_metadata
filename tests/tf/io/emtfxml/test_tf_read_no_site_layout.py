# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest

import numpy as np
from collections import OrderedDict
from mt_metadata import TF_XML_NO_SITE_LAYOUT
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML_NO_SITE_LAYOUT)
        self.tf.read()
        self.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                (
                    "acquired_by.author",
                    "Kent Inverarity / David Pedler-Jones / UofA",
                ),
                ("channels_recorded", ["ex", "ey", "hx", "hy"]),
                (
                    "comments",
                    "description:Magnetotelluric Transfer Functions; primary_data.filename:500fdfilNB207.png; attachment.description:The original used to produce the XML; attachment.filename:500fdfilNB207.edi; site.data_quality_notes.comments.author:Lars Krieger; site.data_quality_notes.comments.value:poor",
                ),
                ("data_type", "mt"),
                ("fdsn.id", "UofAdelaide.500fdfilNB207.2010"),
                ("geographic_name", "Northern Flinders Ranges, Australia"),
                ("id", "500fdfilNB207"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "1995.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 534.0),
                ("location.latitude", -30.587969),
                ("location.longitude", 138.959969),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.name", None),
                ("provenance.creation_time", "2018-01-05T09:55:25+00:00"),
                ("provenance.creator.author", "Lars Krieger"),
                ("provenance.creator.email", "zu.spaet@web.de"),
                ("provenance.creator.name", "Lars Krieger"),
                (
                    "provenance.creator.organization",
                    "Institude of Mineral and Energy Resources, University of Adelaide",
                ),
                ("provenance.creator.url", "https://www.adelaide.edu.au/imer/"),
                ("provenance.software.author", None),
                (
                    "provenance.software.name",
                    "EMTF File Conversion Utilities 4.0",
                ),
                ("provenance.software.version", None),
                ("provenance.submitter.author", "Lana Erofeeva"),
                ("provenance.submitter.email", "serofeev@coas.oregonstate.edu"),
                ("provenance.submitter.name", "Lana Erofeeva"),
                (
                    "provenance.submitter.organization",
                    "Oregon State University",
                ),
                ("provenance.submitter.url", "http://oregonstate.edu"),
                ("release_license", "CC0-1.0"),
                ("run_list", ["500fdfilNB207a"]),
                ("time_period.end", "2011-01-01T00:00:00+00:00"),
                ("time_period.start", "2011-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.good_from_period", 0.0),
                ("transfer_function.data_quality.good_to_period", 0.0),
                ("transfer_function.data_quality.rating.value", 2),
                ("transfer_function.id", "500fdfilNB207"),
                (
                    "transfer_function.processed_by.author",
                    "Kent Inverarity / David Pedler-Jones / UofA",
                ),
                (
                    "transfer_function.processed_by.name",
                    "Kent Inverarity / David Pedler-Jones / UofA",
                ),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                ("transfer_function.processing_type", ""),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", [""]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
                ("transfer_function.software.author", None),
                ("transfer_function.software.last_updated", "2002-04-23"),
                ("transfer_function.software.name", "WINGLINK EDI 1.0.22"),
                ("transfer_function.software.version", None),
                ("transfer_function.units", None),
            ]
        )
        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.to_dict(single=True)
        )

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                (
                    "acquired_by.author",
                    "Kent Inverarity / David Pedler-Jones / UofA",
                ),
                (
                    "citation_dataset.authors",
                    "Kent Inverarity, James Wilson, Graham Heinson, Michael Hatch and Stephan Thiel",
                ),
                (
                    "citation_dataset.doi",
                    "doi:10.17611/DP/EMTF/UOFADELAIDE/GW",
                ),
                (
                    "citation_dataset.title",
                    "Groundwater Magnetotelluric Transfer Functions in the Great Artesian Basin, Australia",
                ),
                ("citation_dataset.year", "2010-2013"),
                ("citation_journal.doi", None),
                (
                    "comments",
                    "copyright.acknowledgement:Funding was provided by the National Water Commission and Geoscientists Without Borders (Society of Exploration Geophysicists Foundation). The surveys instruments were provided by and Zonge Engineering (Australia).; copyright.conditions_of_use:All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided that this data set is cited as the reference, and that the author(s) contributions are acknowledged as detailed in the Acknowledgements. Any papers cited in this file are only for reference. There is no requirement to cite these papers when the data are used. Whenever possible, we ask that the author(s) are notified prior to any publication that makes use of these data. While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, nor IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.; copyright.release_status:Unrestricted Release",
                ),
                ("country", ["Australia"]),
                ("datum", "WGS84"),
                ("geographic_name", "Nepabunna 2010"),
                ("id", "Nepabunna 2010"),
                ("name", None),
                ("northwest_corner.latitude", 0.0),
                ("northwest_corner.longitude", 0.0),
                ("project", "UofAdelaide"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 0.0),
                ("southeast_corner.longitude", 0.0),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2011-01-01"),
                ("time_period.start_date", "2011-01-01"),
            ]
        )
        self.assertDictEqual(
            meta_dict, self.tf.survey_metadata.to_dict(single=True)
        )

    def test_run_a(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", ["ex", "ey"]),
                ("channels_recorded_magnetic", ["hx", "hy"]),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", None),
                ("data_logger.manufacturer", None),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", None),
                ("data_type", "BBMT"),
                ("id", "500fdfilNB207a"),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((26, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [272.2 + 193.33j, 267.26 + 219.7401j],
                            [-277.68 - 191.25j, -47.289 - 57.75299j],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[-1],
                    np.array(
                        [
                            [1.6235 + 6.6321j, 3.2061 + 3.132j],
                            [-4.6372 - 11.512j, -3.433599 + 0.7264208j],
                        ]
                    ),
                ).all()
            )

    def test_sip(self):
        self.assertEqual(None, self.tf.inverse_signal_power)

    def test_residual(self):
        self.assertEqual(None, self.tf.residual_covariance)

    def test_t(self):
        self.assertEqual(None, self.tf.tipper)


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
