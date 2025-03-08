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
from mt_metadata import TF_POOR_XML
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_POOR_XML)
        self.tf.read()
        self.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                (
                    "comments",
                    "description:Magnetotelluric Transfer Functions; primary_data.filename:CAS04-CAS04bcd_REV06-CAS04bcd_NVR08.png; attachment.description:The original used to produce the XML; attachment.filename:CAS04-CAS04bcd_REV06-CAS04bcd_NVR08.zmm; site.data_quality_notes.comments.author:Jade Crosbie, Paul Bedrosian and Anna Kelbert; site.data_quality_notes.comments.value:good TF from 10 to 10000 secs; site.data_quality_warnings.flag:0; site.data_quality_warnings.comments.author:Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("data_type", "mt"),
                ("fdsn.id", "USMTArray.CAS04.2020"),
                ("geographic_name", "Corral Hollow, CA, USA"),
                ("id", "CAS04"),
                ("location.declination.epoch", "2020.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 13.175),
                ("location.elevation", 329.387),
                ("location.latitude", 37.63335),
                ("location.longitude", -121.46838),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.comments", "IRIS DMC MetaData"),
                ("provenance.archive.name", None),
                ("provenance.archive.url", "http://www.iris.edu/mda/8P/CAS04"),
                ("provenance.creation_time", "2021-09-23T19:45:02+00:00"),
                (
                    "provenance.creator.author",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("provenance.creator.email", "pbedrosian@usgs.gov"),
                (
                    "provenance.creator.name",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("provenance.creator.organization", "U.S. Geological Survey"),
                (
                    "provenance.creator.url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
                ("provenance.software.author", None),
                (
                    "provenance.software.name",
                    "EMTF File Conversion Utilities 4.0",
                ),
                ("provenance.software.version", None),
                ("provenance.submitter.author", "Anna Kelbert"),
                ("provenance.submitter.email", "akelbert@usgs.gov"),
                ("provenance.submitter.name", "Anna Kelbert"),
                (
                    "provenance.submitter.organization",
                    "U.S. Geological Survey, Geomagnetism Program",
                ),
                (
                    "provenance.submitter.url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
                ("release_license", "CC0-1.0"),
                ("run_list", ["CAS04a"]),
                ("time_period.end", "2020-07-13T21:46:12+00:00"),
                ("time_period.start", "2020-06-02T18:41:43+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 4),
                ("transfer_function.id", "CAS04"),
                ("transfer_function.processed_by.name", None),
                ("transfer_function.processed_date", "1980-01-01"),
                (
                    "transfer_function.processing_parameters",
                    [
                        "remote_info.site.id = REV06",
                        "remote_info.site.name = Poso Creek, CA, USA",
                        "remote_info.site.location.latitude = 35.71262",
                        "remote_info.site.location.longitude = -119.466415",
                        "remote_info.site.location.elevation = 61.05",
                        "remote_info.site.orientation.angle_to_geographic_north = 0.0",
                        "remote_info.site.orientation.layout = orthogonal",
                    ],
                ),
                (
                    "transfer_function.processing_type",
                    "Robust Remote Reference",
                ),
                ("transfer_function.remote_references", ["REV06"]),
                (
                    "transfer_function.runs_processed",
                    ["CAS04a", "CAS04b", "CAS04c", "CAS04d"],
                ),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
                ("transfer_function.software.author", None),
                ("transfer_function.software.last_updated", "2015-08-26"),
                ("transfer_function.software.name", "EMTF"),
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
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                (
                    "citation_dataset.authors",
                    "Schultz, A., Pellerin, L., Bedrosian, P., Kelbert, A., Crosbie, J.",
                ),
                (
                    "citation_dataset.doi",
                    "doi:10.17611/DP/EMTF/USMTARRAY/SOUTH",
                ),
                (
                    "citation_dataset.title",
                    "USMTArray South Magnetotelluric Transfer Functions",
                ),
                ("citation_dataset.year", "2020-2023"),
                ("citation_journal.doi", None),
                (
                    "comments",
                    "copyright.acknowledgement:The USMTArray-CONUS South "
                    "campaign was carried out through a cooperative agreement "
                    "between\nthe U.S. Geological Survey (USGS) and Oregon "
                    "State University (OSU). A subset of 40 stations\nin the "
                    "SW US were funded through NASA grant 80NSSC19K0232."
                    "\nLand permitting, data acquisition, quality control and "
                    "field processing were\ncarried out by Green Geophysics "
                    "with project management and instrument/engineering"
                    "\nsupport from OSU and Chaytus Engineering, respectively."
                    "\nProgram oversight, definitive data processing and data "
                    "archiving were provided\nby the USGS Geomagnetism Program "
                    "and the Geology, Geophysics and Geochemistry Science "
                    "Centers.\nWe thank the U.S. Forest Service, the Bureau "
                    "of Land Management, the National Park Service,\nthe "
                    "Department of Defense, numerous state land offices and "
                    "the many private landowners\nwho permitted land access "
                    "to acquire the USMTArray data.; "
                    "copyright.conditions_of_use:All data and metadata for "
                    "this survey are available free of charge and may be "
                    "copied freely, duplicated and further distributed "
                    "provided that this data set is cited as the reference, "
                    "and that the author(s) contributions are acknowledged "
                    "as detailed in the Acknowledgements. Any papers cited in "
                    "this file are only for reference. There is no requirement "
                    "to cite these papers when the data are used. Whenever "
                    "possible, we ask that the author(s) are notified prior "
                    "to any publication that makes use of these data.\n While "
                    "the author(s) strive to provide data and metadata of best "
                    "possible quality, neither the author(s) of this data set, "
                    "nor IRIS make any claims, promises, or guarantees about "
                    "the accuracy, completeness, or adequacy of this "
                    "information, and expressly disclaim liability for errors "
                    "and omissions in the contents of this file. Guidelines "
                    "about the quality or limitations of the data and metadata, "
                    "as obtained from the author(s), are included for "
                    "informational purposes only.; "
                    "copyright.release_status:Unrestricted Release",
                ),
                ("datum", "WGS84"),
                ("geographic_name", "CONUS South"),
                ("id", "CONUS South"),
                ("name", None),
                ("northwest_corner.latitude", 37.63335),
                ("northwest_corner.longitude", -121.46838),
                ("project", "USMTArray"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 37.63335),
                ("southeast_corner.longitude", -121.46838),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2020-07-13"),
                ("time_period.start_date", "2020-06-02"),
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
                ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
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
                ("id", "CAS04a"),
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
            self.assertTupleEqual((33, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [0.05218971 - 0.493787j, 1.004782 + 1.873659j],
                            [-0.8261183 + 1.226159j, 1.36161 - 1.376113j],
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
                            [
                                0.03680307 + 0.00131353j,
                                0.06559774 + 0.00177508j,
                            ],
                            [
                                -0.05877226 - 0.02631392j,
                                -0.01419307 - 0.03934453j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_sip(self):
        self.assertEqual(None, self.tf.inverse_signal_power)

    def test_residual(self):
        self.assertEqual(None, self.tf.residual_covariance)

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array([[-0.5953611 - 1.984346j, -1.313187 + 1.159378j]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array(
                        [[-0.02102757 - 0.06664169j, 0.5568553 + 0.1630035j]]
                    ),
                ).all()
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
