# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest
from collections import OrderedDict

import numpy as np

from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF


# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tf = TF(fn=TF_XML)
        cls.tf.read()
        cls.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                (
                    "comments",
                    "description:Magnetotelluric Transfer Functions; primary_data.filename:NMX20b_NMX20_NMW20_COR21_NMY21-NMX20b_NMX20_UTS18.png; attachment.description:The original used to produce the XML; attachment.filename:NMX20b_NMX20_NMW20_COR21_NMY21-NMX20b_NMX20_UTS18.zmm; site.data_quality_notes.comments.author:Jade Crosbie, Paul Bedrosian and Anna Kelbert; site.data_quality_notes.comments.value:great TF from 10 to 10000 secs (or longer)",
                ),
                ("data_type", "mt"),
                ("fdsn.id", "USMTArray.NMX20.2020"),
                ("geographic_name", "Nations Draw, NM, USA"),
                ("id", "NMX20"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "2020.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 9.09),
                ("location.elevation", 1940.05),
                ("location.latitude", 34.470528),
                ("location.longitude", -108.712288),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.comments", "IRIS DMC MetaData"),
                ("provenance.archive.url", "http://www.iris.edu/mda/ZU/NMX20"),
                ("provenance.creation_time", "2021-03-17T14:47:44+00:00"),
                (
                    "provenance.creator.author",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("provenance.creator.email", "pbedrosian@usgs.gov"),
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
                (
                    "provenance.submitter.organization",
                    "U.S. Geological Survey, Geomagnetism Program",
                ),
                (
                    "provenance.submitter.url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
                ("release_license", "CC0-1.0"),
                ("run_list", ["NMX20a", "NMX20b"]),
                ("time_period.end", "2020-10-07T20:28:00+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.good_from_period", 5.0),
                ("transfer_function.data_quality.good_to_period", 29127.0),
                ("transfer_function.data_quality.rating.value", 5),
                ("transfer_function.id", "NMX20"),
                (
                    "transfer_function.processed_by.author",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                (
                    "transfer_function.processing_type",
                    "Robust Multi-Station Reference",
                ),
                (
                    "transfer_function.remote_references",
                    ["NMW20", "COR21", "UTS18"],
                ),
                ("transfer_function.runs_processed", ["NMX20a", "NMX20b"]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
                ("transfer_function.software.author", "Gary Egbert"),
                ("transfer_function.software.last_updated", "2015-08-26"),
                ("transfer_function.software.name", "EMTF"),
                ("transfer_function.software.version", None),
                ("transfer_function.units", None),
            ]
        )

        self.assertDictEqual(meta_dict, self.tf.station_metadata.to_dict(single=True))

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                (
                    "citation_dataset.authors",
                    (
                        "Schultz, A., Pellerin, L., Bedrosian, P., Kelbert, A., "
                        "Crosbie, J."
                    ),
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
                    (
                        "copyright.acknowledgement:The USMTArray-CONUS South "
                        "campaign was carried out through a cooperative "
                        "agreement between\nthe U.S. Geological Survey (USGS) "
                        "and Oregon State University (OSU). A subset of 40 "
                        "stations\nin the SW US were funded through NASA grant "
                        "80NSSC19K0232.\nLand permitting, data acquisition, "
                        "quality control and field processing were\ncarried out "
                        "by Green Geophysics with project management and "
                        "instrument/engineering\nsupport from OSU and Chaytus "
                        "Engineering, respectively.\nProgram oversight, "
                        "definitive data processing and data archiving were "
                        "provided\nby the USGS Geomagnetism Program and the "
                        "Geology, Geophysics and Geochemistry Science Centers."
                        "\nWe thank the U.S. Forest Service, the Bureau of Land "
                        "Management, the National Park Service,\nthe Department "
                        "of Defense, numerous state land offices and the many "
                        "private landowners\nwho permitted land access to "
                        "acquire the USMTArray data.; "
                        "copyright.conditions_of_use:All data and metadata for "
                        "this survey are available free of charge and may be "
                        "copied freely, duplicated and further distributed "
                        "provided that this data set is cited as the reference, "
                        "and that the author(s) contributions are acknowledged "
                        "as detailed in the Acknowledgements. Any papers cited "
                        "in this file are only for reference. There is no "
                        "requirement to cite these papers when the data are "
                        "used. Whenever possible, we ask that the author(s) are"
                        " notified prior to any publication that makes use of "
                        "these data.\n While the author(s) strive to provide "
                        "data and metadata of best possible quality, neither "
                        "the author(s) of this data set, nor IRIS make any "
                        "claims, promises, or guarantees about the accuracy, "
                        "completeness, or adequacy of this information, and "
                        "expressly disclaim liability for errors and omissions "
                        "in the contents of this file. Guidelines about the "
                        "quality or limitations of the data and metadata, as "
                        "obtained from the author(s), are included for "
                        "informational purposes only.; "
                        "copyright.release_status:Unrestricted Release"
                    ),
                ),
                ("country", ["USA"]),
                ("datum", "WGS84"),
                ("geographic_name", "CONUS South"),
                ("id", "CONUS South"),
                ("name", None),
                ("northwest_corner.latitude", 34.470528),
                ("northwest_corner.longitude", -108.712288),
                ("project", "USMTArray"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 34.470528),
                ("southeast_corner.longitude", -108.712288),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2020-10-07"),
                ("time_period.start_date", "2020-09-20"),
            ]
        )
        self.assertDictEqual(meta_dict, self.tf.survey_metadata.to_dict(single=True))

    def test_run_a(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", ["ex", "ey"]),
                ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                (
                    "comments",
                    "comments.author:Isaac Sageman; comments.value:X array at 0 deg rotation. All e-lines 50m. Soft sandy dirt. Water tank ~400m NE. County Rd 601 ~200m SE. Warm sunny day.",
                ),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", "2612-01"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", "NIMS"),
                ("data_type", "BBMT"),
                ("id", "NMX20a"),
                ("sample_rate", 1.0),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_run_b(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", ["ex", "ey"]),
                ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                (
                    "comments",
                    "comments.author:Isaac Sageman; comments.value:X array at 0 deg rotation. All e-lines 50m. Soft sandy dirt. Water tank ~400m NE. County Rd 601 ~200m SE. Warm sunny day.; errors:Found data gaps (2). Gaps of unknown length: 1 [1469160].]",
                ),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", "2612-01"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", "NIMS"),
                ("data_type", "BBMT"),
                ("id", "NMX20b"),
                ("sample_rate", 1.0),
                ("time_period.end", "2020-10-07T20:28:00+00:00"),
                ("time_period.start", "2020-09-20T20:12:29+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[1].to_dict(single=True)
        )

    def test_run_a_ex(self):
        meta_dict = OrderedDict(
            [
                ("channel_number", 0),
                ("component", "ex"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 9.1),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", "40201037"),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", "Oregon State University"),
                ("negative.type", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                ("negative.x", -50.0),
                ("negative.y", 0.0),
                ("negative.z", 0.0),
                ("positive.elevation", 0.0),
                ("positive.id", "40201038"),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", "Oregon State University"),
                ("positive.type", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                ("positive.x2", 50.0),
                ("positive.y2", 0.0),
                ("positive.z2", 0.0),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("translated_azimuth", 9.1),
                ("type", "electric"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels["ex"].to_dict(single=True),
        )

    def test_run_a_ey(self):
        meta_dict = OrderedDict(
            [
                ("channel_number", 0),
                ("component", "ey"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 99.1),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", "40201031"),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", "Oregon State University"),
                ("negative.type", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                ("negative.x", 0.0),
                ("negative.y", -50.0),
                ("negative.z", 0.0),
                ("positive.elevation", 0.0),
                ("positive.id", "40201032"),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", "Oregon State University"),
                ("positive.type", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                ("positive.x2", 0.0),
                ("positive.y2", 50.0),
                ("positive.z2", 0.0),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("translated_azimuth", 99.1),
                ("type", "electric"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels["ey"].to_dict(single=True),
        )

    def test_run_a_hx(self):
        meta_dict = OrderedDict(
            [
                ("channel_number", 0),
                ("component", "hx"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("location.x", 0.0),
                ("location.y", 0.0),
                ("location.z", 0.0),
                ("measurement_azimuth", 9.1),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2509-23"),
                ("sensor.manufacturer", "Barry Narod"),
                ("sensor.name", "NIMS"),
                ("sensor.type", "fluxgate"),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("translated_azimuth", 9.1),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels["hx"].to_dict(single=True),
        )

    def test_run_a_hy(self):
        meta_dict = OrderedDict(
            [
                ("channel_number", 0),
                ("component", "hy"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("location.x", 0.0),
                ("location.y", 0.0),
                ("location.z", 0.0),
                ("measurement_azimuth", 99.1),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2509-23"),
                ("sensor.manufacturer", "Barry Narod"),
                ("sensor.name", "NIMS"),
                ("sensor.type", "fluxgate"),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("translated_azimuth", 99.1),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels["hy"].to_dict(single=True),
        )

    def test_run_a_hz(self):
        meta_dict = OrderedDict(
            [
                ("channel_number", 0),
                ("component", "hz"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("location.x", 0.0),
                ("location.y", 0.0),
                ("location.z", 0.0),
                ("measurement_azimuth", 9.1),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2509-23"),
                ("sensor.manufacturer", "Barry Narod"),
                ("sensor.name", "NIMS"),
                ("sensor.type", "fluxgate"),
                ("time_period.end", "2020-09-20T19:29:28+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("translated_azimuth", 9.1),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels["hz"].to_dict(single=True),
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
                            [-0.1160949 - 0.2708645j, 3.143284 + 1.101737j],
                            [-2.470717 - 0.7784633j, -0.1057851 + 0.1022045j],
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
                                0.00483462 + 0.00983358j,
                                0.02643963 + 0.05098311j,
                            ],
                            [
                                -0.02203037 - 0.03744689j,
                                -0.00295362 - 0.01293358j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.tf.inverse_signal_power.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[0],
                    np.array(
                        [
                            [
                                0.8745101 - 2.905133e-08j,
                                -0.4293981 + 1.663000e-01j,
                            ],
                            [
                                -0.4293981 - 1.663000e-01j,
                                1.39159 - 7.486698e-10j,
                            ],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[-1],
                    np.array(
                        [
                            [
                                9.120293e-08 - 2.13634e-16j,
                                5.066908e-08 + 2.26600e-08j,
                            ],
                            [
                                5.066908e-08 - 2.26600e-08j,
                                1.086271e-07 + 1.02634e-16j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 3, 3), self.tf.residual_covariance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[0],
                    np.array(
                        [
                            [
                                1.28646000e-03 + 8.47032900e-22j,
                                -5.81671100e-05 + 3.34700000e-05j,
                                0.00000000e00 + 0.00000000e00j,
                            ],
                            [
                                -5.81671100e-05 - 3.34700000e-05j,
                                1.03754000e-03 + 0.00000000e00j,
                                0.00000000e00 + 0.00000000e00j,
                            ],
                            [
                                0.00000000e00 + 0.00000000e00j,
                                0.00000000e00 + 0.00000000e00j,
                                9.62300000e-05 + 0.00000000e00j,
                            ],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[-1],
                    np.array(
                        [
                            [
                                86.38148 + 0.00000000e00j,
                                -31.70986 + 1.28100000e00j,
                                0.00000 + 0.00000000e00j,
                            ],
                            [
                                -31.70986 - 1.28100000e00j,
                                45.52852 - 2.77555800e-17j,
                                0.00000 + 0.00000000e00j,
                            ],
                            [
                                0.00000 + 0.00000000e00j,
                                0.00000 + 0.00000000e00j,
                                29820.00000 + 0.00000000e00j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array([[-0.09386985 + 0.00620671j, 0.04601304 + 0.03035755j]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array([[-0.03648688 + 0.08738894j, 0.1750294 + 0.1666582j]]),
                ).all()
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
