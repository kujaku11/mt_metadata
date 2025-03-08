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
from mt_metadata import TF_XML_WITH_DERIVED_QUANTITIES
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML_WITH_DERIVED_QUANTITIES)
        self.tf.read()
        self.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "Freie Universitaet Berlin"),
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                (
                    "comments",
                    "description:Magnetotelluric Transfer Functions; primary_data.filename:SMG1.png; attachment.description:The original used to produce the XML; attachment.filename:SMG1.edi; site.data_quality_notes.comments.value:Unrated",
                ),
                ("data_type", "mt"),
                ("fdsn.id", "FU-BERLIN.SMG1.2003"),
                ("geographic_name", "South Chile"),
                ("id", "SMG1"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "1995.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 10.0),
                ("location.latitude", -38.41),
                ("location.longitude", -73.904722),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.name", None),
                ("provenance.creation_time", "2020-06-05T12:06:27+00:00"),
                ("provenance.creator.author", "Heinrich Brasse"),
                ("provenance.creator.email", "heinrich.brasse@fu-berlin.de"),
                ("provenance.creator.name", "Heinrich Brasse"),
                (
                    "provenance.creator.organization",
                    "Freie Universitaet Berlin",
                ),
                ("provenance.creator.url", "https://www.fu-berlin.de"),
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
                    "U.S. Geological Survey Geomagnetism Program",
                ),
                ("provenance.submitter.url", "http://geomag.usgs.gov"),
                ("release_license", "CC0-1.0"),
                ("run_list", ["SMG1a"]),
                ("time_period.end", "2003-01-02T00:00:00+00:00"),
                ("time_period.start", "2003-01-02T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 0),
                ("transfer_function.id", "SMG1"),
                ("transfer_function.processed_by.author", "Heinrich Brasse"),
                ("transfer_function.processed_by.name", "Heinrich Brasse"),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                ("transfer_function.processing_type", ""),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", [""]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
                ("transfer_function.software.author", "Randie Mackie"),
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
                ("acquired_by.author", "Freie Universitaet Berlin"),
                ("citation_dataset.authors", "Heinrich Brasse"),
                (
                    "citation_dataset.doi",
                    "doi:10.17611/DP/EMTF/FU-BERLIN/SOUTHCHILE",
                ),
                (
                    "citation_dataset.title",
                    "Magnetotelluric Transfer Functions in South Chile by Freie Universitaet, Berlin",
                ),
                ("citation_dataset.year", "2003-2005"),
                ("citation_journal.doi", None),
                (
                    "comments",
                    "copyright.conditions_of_use:All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided that this data set is cited as the reference, and that the author(s) contributions are acknowledged as detailed in the Acknowledgements. The author(s) of this survey additionally require that anyone using these data explicitly cites all publications referenced in the Selected Publications section of this data file. While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, nor IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.; copyright.release_status:Paper Citation Required; copyright.selected_publications:Brasse, H., Kapinos, G., Li, Y., Mutschard, L., Soyer, W. and Eydam, D. (2009): Structural electrical anisotropy in the crust at the South-Central Chilean continental margin as inferred from geomagnetic transfer functions, Phys. Earth Planet. Inter., 173, doi:10.1016/j.pepi.2008.10.017.; copyright.additional_info:South American MT data from Henri Brasse ---------------------------------------- On Costa Rica, Jan 2018: Please find attached our Costa Rica data, where bad data points have already been removed. They are in EDI format, because I had only the land stations in Egbert's format; the offshore data were processed with another software. On South Chile, May 2019: Please note that ob7 is an ocean bottom site, and vin does not have electric fields, just tippers. Poor data, particularly at very long periods, are discarded. On Nicaragua, May 2019: All data have been processed with Egbert's and Bookers's (1986) and Egbert's (1997) codes. I don't have the spectra here and please understand, that it's too much work to produce them again. So I just send the edi files. Poor data are discarded (in Nicaragua quite a few because that was a solar minimum). On Chile-Bolivia, May 2019: Here are the last two profiles from the Americas which I may share for the time being: 1) Chile-Bolivia at 21 S (Ancorp) 2) Chile-Bolivia at 18 S There are a few more, but my Chilean colleagues are working on them currently, so I don't want to share them right now. I was PI of those projects and actually operated about 90% of the stations myself. All other participants are listed in the publications.",
                ),
                ("country", ["Chile"]),
                ("datum", "WGS84"),
                ("geographic_name", "South Chile"),
                ("id", "South Chile"),
                ("name", None),
                ("northwest_corner.latitude", -38.41),
                ("northwest_corner.longitude", -73.904722),
                ("project", "FU-BERLIN"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", -38.41),
                ("southeast_corner.longitude", -73.904722),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2003-01-02"),
                ("time_period.start_date", "2003-01-02"),
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
                ("id", "SMG1a"),
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
            self.assertTupleEqual((20, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0].data,
                    np.array(
                        [
                            [
                                -8.089973e-03 - 0.04293998j,
                                9.217000e-01 + 0.3741j,
                            ],
                            [
                                -6.215000e-01 - 0.4342j,
                                -4.668272e-04 - 0.00064572j,
                            ],
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
                            [7.610000e-02 + 0.06188j, 1.069000e-01 + 0.1594j],
                            [
                                -6.638000e-02 - 0.05362j,
                                -4.141902e-06 + 0.004022j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((20, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0].data,
                    np.array([[0.06982 + 0.01516j, -0.1876 + 0.0135j]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1].data,
                    np.array([[1.0e32 + 1.0e32j, 1.0e32 + 1.0e32j]]),
                ).all()
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
