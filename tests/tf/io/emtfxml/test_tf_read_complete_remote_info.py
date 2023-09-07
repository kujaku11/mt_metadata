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
from mt_metadata import TF_XML_COMPLETE_REMOTE_INFO
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML_COMPLETE_REMOTE_INFO)
        self.tf.read()
        self.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                (
                    "comments",
                    "description:Magnetotelluric Transfer Functions; primary_data.filename:GAA54b_A53coh.png; attachment.description:The original used to produce the XML; attachment.filename:GAA54b_A53coh.zrr; site.data_quality_notes.comments.author:Gary Egbert, Lana Erofeev and Anna Kelbert; site.data_quality_notes.comments.value:great TF from 10 to 10000 secs (or longer); site.data_quality_warnings.flag:0; site.data_quality_warnings.comments.author:Gary Egbert, Lana Erofeev and Anna Kelbert",
                ),
                ("data_type", "mt"),
                ("fdsn.id", "USArray.GAA54.2015"),
                ("geographic_name", "Gator Slide, GA, USA"),
                ("id", "GAA54"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "1995.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", -4.6),
                ("location.elevation", 77.025),
                ("location.latitude", 31.888699),
                ("location.longitude", -83.281681),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.comments", "IRIS DMC MetaData"),
                ("provenance.archive.name", None),
                ("provenance.archive.url", "http://www.iris.edu/mda/EM/GAA54"),
                ("provenance.creation_time", "2018-01-03T12:46:46+00:00"),
                (
                    "provenance.creator.author",
                    "Gary Egbert, Lana Erofeev and Anna Kelbert",
                ),
                ("provenance.creator.email", "egbert@coas.oregonstate.edu"),
                (
                    "provenance.creator.name",
                    "Gary Egbert, Lana Erofeev and Anna Kelbert",
                ),
                ("provenance.creator.organization", "Oregon State University"),
                ("provenance.creator.url", "http://oregonstate.edu"),
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
                    "U.S. Geological Survey",
                ),
                ("provenance.submitter.url", "http://geomag.usgs.gov"),
                ("release_license", "CC0-1.0"),
                ("run_list", ["GAA54b"]),
                ("time_period.end", "2015-09-28T14:05:14+00:00"),
                ("time_period.start", "2015-09-11T17:45:44+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.good_from_period", 10.0),
                ("transfer_function.data_quality.good_to_period", 10000.0),
                ("transfer_function.data_quality.rating.value", 5),
                ("transfer_function.id", "GAA54"),
                (
                    "transfer_function.processed_by.author",
                    "Gary Egbert, Lana Erofeev and Anna Kelbert",
                ),
                (
                    "transfer_function.processed_by.name",
                    "Gary Egbert, Lana Erofeev and Anna Kelbert",
                ),
                ("transfer_function.processed_date", "1980-01-01"),
                (
                    "transfer_function.processing_parameters",
                    [
                        "remote_info.site.project = USArray",
                        "remote_info.site.survey = Transportable Array",
                        "remote_info.site.year_collected = 2015",
                        "remote_info.site.country = USA",
                        "remote_info.site.id = GAA53",
                        "remote_info.site.name = WHEATLEY FOREST, GA, USA",
                        "remote_info.site.location.latitude = 31.904132",
                        "remote_info.site.location.longitude = -83.946993",
                        "remote_info.site.location.elevation = 86.5",
                        "remote_info.site.location.datum = WGS84",
                        "remote_info.site.orientation.angle_to_geographic_north = 0.0",
                        "remote_info.site.orientation.layout = orthogonal",
                    ],
                ),
                (
                    "transfer_function.processing_type",
                    "Robust Remote Reference",
                ),
                ("transfer_function.remote_references", ["GAA53"]),
                ("transfer_function.runs_processed", ["GAA54b"]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
                ("transfer_function.software.author", "Gary Egbert"),
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
                    "Schultz, A., G. D. Egbert, A. Kelbert, T. Peery, V. Clote, B. Fry, S. Erofeeva and staff of the National Geoelectromagnetic Facility and their contractors",
                ),
                ("citation_dataset.doi", "doi:10.17611/DP/EMTF/USARRAY/TA"),
                (
                    "citation_dataset.title",
                    "USArray TA Magnetotelluric Transfer Functions",
                ),
                ("citation_dataset.year", "2006-2018"),
                ("citation_journal.doi", None),
                (
                    "comments",
                    "copyright.acknowledgement:USArray MT TA project was led by PI Adam Schultz and Gary Egbert. They would like to thank the Oregon State University MT team and their contractors, lab and field personnel over the years for assistance with data collection, quality control, processing and archiving. They also thank numerous districts of the U.S. Forest Service, Bureau of Land Management, the U.S. National Parks, the collected State land offices, and the many private landowners who permitted access to acquire the MT TA data. USArray TA was funded through NSF grants EAR-0323311, IRIS Subaward 478 and 489 under NSF Cooperative Agreement EAR-0350030 and EAR-0323309, IRIS Subaward 75-MT under NSF Cooperative Agreement EAR-0733069 under CFDA No. 47.050, and IRIS Subaward 05-OSU-SAGE under NSF Cooperative Agreement EAR-1261681 under CFDA No. 47.050.; copyright.conditions_of_use:All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided that this data set is cited as the reference, and that the author(s) contributions are acknowledged as detailed in the Acknowledgements. Any papers cited in this file are only for reference. There is no requirement to cite these papers when the data are used. Whenever possible, we ask that the author(s) are notified prior to any publication that makes use of these data. While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, nor IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.; copyright.release_status:Unrestricted Release",
                ),
                ("country", ["USA"]),
                ("datum", "WGS84"),
                ("geographic_name", "Transportable Array"),
                ("id", "Transportable Array"),
                ("name", None),
                ("northwest_corner.latitude", 0.0),
                ("northwest_corner.longitude", 0.0),
                ("project", "USArray"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 0.0),
                ("southeast_corner.longitude", 0.0),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2015-09-28"),
                ("time_period.start_date", "2015-09-11"),
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
                (
                    "comments",
                    "comments.author:Alen Hooper; comments.value:Open field, sandy soil, dry conditions, private landlN; errors:Found data gaps (6). Of these, 5 duplicate blocks [deleted].] ]G]P]S] ]u]s]e]d] ]t]o] ]c]o]m]p]u]t]e] ]l]e]n]g]t]h] ]o]f] ]1] ]g]a]p]s] ][]5]3]1]0]1]2]].]] ]]",
                ),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", "2612-18"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", "NIMS"),
                ("data_type", "BBMT"),
                ("id", "GAA54b"),
                ("sample_rate", 1.0),
                ("time_period.end", "2015-09-28T14:05:14+00:00"),
                ("time_period.start", "2015-09-11T18:25:47+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((30, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0].data,
                    np.array(
                        [
                            [-0.3689028 - 0.04832953j, 2.904443 + 1.030588j],
                            [-3.734557 - 2.555411j, 0.7417028 - 0.5187305j],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[-1].data,
                    np.array(
                        [
                            [
                                -0.08651634 - 0.1364866j,
                                0.02648226 + 0.1238585j,
                            ],
                            [
                                -0.2994978 - 0.4915415j,
                                -0.01323366 + 0.08021657j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((30, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0].data,
                    np.array(
                        [[-0.1511052 - 0.1205783j, 0.08954691 + 0.1148402j]]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1].data,
                    np.array(
                        [[0.07471948 + 0.3349745j, 0.1931297 + 0.2555586j]]
                    ),
                ).all()
            )

    def test_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual(
                (30, 2, 2), self.tf.inverse_signal_power.shape
            )

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[0].data,
                    np.array(
                        [
                            [
                                4.258637e-05 + 4.588496e-16j,
                                1.635847e-05 + 1.850000e-05j,
                            ],
                            [
                                1.635847e-05 - 1.850000e-05j,
                                3.155363e-05 + 7.088115e-14j,
                            ],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[-1].data,
                    np.array(
                        [
                            [
                                2.804339e-13 - 3.305735e-21j,
                                7.882486e-14 + 7.368000e-14j,
                            ],
                            [
                                7.882486e-14 - 7.368000e-14j,
                                2.755661e-13 - 2.344265e-21j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual(
                (30, 3, 3), self.tf.residual_covariance.shape
            )

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[0].data,
                    np.array(
                        [
                            [
                                11996.37 + 0.000000e00j,
                                7413.954 + 1.642000e02j,
                                0.0 + 0.000000e00j,
                            ],
                            [
                                7413.954 - 1.642000e02j,
                                72473.63 + 1.776357e-15j,
                                0.0 + 0.000000e00j,
                            ],
                            [
                                0.0 + 0.000000e00j,
                                0.0 + 0.000000e00j,
                                1320.0 + 0.000000e00j,
                            ],
                        ]
                    ),
                ).all(),
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[-1].data,
                    np.array(
                        [
                            [
                                3.956800e10 + 0.000000e00j,
                                -6.222869e09 + 5.282000e09j,
                                0.000000e00 + 0.000000e00j,
                            ],
                            [
                                -6.222869e09 - 5.282000e09j,
                                9.572996e09 + 5.960464e-08j,
                                0.000000e00 + 0.000000e00j,
                            ],
                            [
                                0.000000e00 + 0.000000e00j,
                                0.000000e00 + 0.000000e00j,
                                2.304000e10 + 0.000000e00j,
                            ],
                        ]
                    ),
                ).all(),
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
