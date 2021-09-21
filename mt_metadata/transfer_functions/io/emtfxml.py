# -*- coding: utf-8 -*-
"""
EMTFXML
==========

This is meant to follow Anna's XML schema for transfer functions

Created on Sat Sep  4 17:59:53 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import inspect
from pathlib import Path
from collections import OrderedDict
from xml.etree import cElementTree as et

from mt_metadata.transfer_functions import emtf_xml
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.base import helpers
from mt_metadata.utils.validators import validate_attribute
from mt_metadata.transfer_functions.tf import Instrument, Survey, Station, Run
from mt_metadata.utils import mttime
meta_classes = dict(
    [
        (validate_attribute(k), v)
        for k, v in inspect.getmembers(emtf_xml, inspect.isclass)
    ]
)
meta_classes["instrument"] = Instrument
# =============================================================================
# EMTFXML
# =============================================================================


class EMTFXML(emtf_xml.EMTF):
    """
    This is meant to follow Anna's XML schema for transfer functions
    """

    def __init__(self):
        super().__init__()
        self._root_dict = None
        self.logger = setup_logger(self.__class__.__name__)
        self.external_url = emtf_xml.ExternalUrl()
        self.primary_data = emtf_xml.PrimaryData()
        self.attachment = emtf_xml.Attachment()
        self.provenance = emtf_xml.Provenance()
        self.copyright = emtf_xml.Copyright()
        self.site = emtf_xml.Site()
        self.field_notes = [emtf_xml.FieldNotes()]
        self.processing_info = emtf_xml.ProcessingInfo()
        self.statistical_estimates = emtf_xml.StatisticalEstimates()
        self.data_types = emtf_xml.DataTypes()
        self.site_layout = emtf_xml.SiteLayout()
        self.data = emtf_xml.TransferFunction()
        self.period_range = emtf_xml.PeriodRange()

        self.element_keys = [
            "description",
            "product_id",
            "sub_type",
            "notes",
            "tags",
            "external_url",
            "primary_data",
            "attachment",
            "provenance",
            "copyright",
            "site",
            "field_notes",
            "processing_info",
            "statistical_estimates",
            "data_types",
            "site_layout",
            "data",
            "period_range"
        ]

        self._reader_dict = {
            "description": self._read_description,
            "product_id": self._read_product_id,
            "sub_type": self._read_sub_type,
            "notes": self._read_notes,
            "tags": self._read_tags,
            "field_notes": self._read_field_notes,
            "statistical_estimates": self._read_statistical_estimates,
            "site_layout": self._read_site_layout,
            "data_types": self._read_data_types,
            "data": self._read_data,
        }
        
        self._writer_dict = {
            "description": self._write_single,
            "product_id": self._write_single,
            "sub_type": self._write_single,
            "notes": self._write_single,
            "tags": self._write_single,
            "provenance": self._write_provenance,
            "field_notes": self._write_field_notes,
            "statistical_estimates": self._write_statistical_estimates,
            "data_types": self._write_data_types,
            "site_layout": self._write_site_layout,
            "data": self._write_data,
        }

    def read(self, fn):
        """
        Read xml file

        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        fn = Path(fn)
        if not fn.exists():
            raise IOError(f"Cannot find: {fn}")

        root = et.parse(fn).getroot()
        root_dict = helpers.element_to_dict(root)
        root_dict = root_dict[list(root_dict.keys())[0]]
        root_dict = self._convert_keys_to_lower_case(root_dict)
        self._root_dict = root_dict

        for element in self.element_keys:
            if element in self._reader_dict.keys():
                self._reader_dict[element](root_dict)
            else:
                self._read_element(root_dict, element)
                
        self.period_range.min = self.data.period.min()
        self.period_range.max = self.data.period.max()
                
    def write(self, fn):
        """
        Write an xml 
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        emtf_element = et.Element("EM_TF")
        
        if self.site.location.x == 0 and self.site.location.x2 == 0 and \
            self.site.location.y == 0 and self.site.location.y2 == 0 and \
            self.site.location.z == 0:
            self.site.location.x = None
            self.site.location.y = None
            self.site.location.z = None
            self.site.location.x2 = None
            self.site.location.y2 = None
            
        
        for key in self.element_keys:
            value = getattr(self, key)
            if key in self._writer_dict.keys():
                self._writer_dict[key](emtf_element, key, value)
            else:
                self._write_element(emtf_element, value, )
                
        with open(fn, "w") as fid:
            fid.write(helpers.element_to_string(emtf_element))
        

    def _read_single(self, root_dict, key):
        try:
            setattr(self, key, root_dict[key])
        except KeyError:
            self.logger.debug("no description in xml")
            
    def _write_single(self, parent, key, value, attributes={}):
        element = et.SubElement(parent, self._capwords(key), attributes) 
        if value:
            element.text = str(value)
        return element

    def _read_description(self, root_dict):
        self._read_single(root_dict, "description")

    def _read_product_id(self, root_dict):
        self._read_single(root_dict, "product_id")

    def _read_sub_type(self, root_dict):
        self._read_single(root_dict, "sub_type")


    def _read_notes(self, root_dict):
        self._read_single(root_dict, "notes")
    

    def _read_tags(self, root_dict):
        self._read_single(root_dict, "tags")
    

    def _read_element(self, root_dict, element_name):
        """
        generic read an element given a name

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :param element_name: DESCRIPTION
        :type element_name: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        element_name = validate_attribute(element_name)
        if element_name in ["field_notes"]:
            self._read_field_notes(root_dict)
        elif element_name in ["statistical_estimates"]:
            self._read_statistical_estimates(root_dict)
        elif element_name in ["site_layout"]:
            self._read_site_layout(root_dict)
        else:
            try:
                value = root_dict[element_name]
                element_dict = {element_name: value}
                getattr(self, element_name).from_dict(element_dict)

            except KeyError:
                print(f"No {element_name} in EMTF XML")
                self.logger.debug(f"No {element_name} in EMTF XML")
                
    def _write_element(self, parent, value, attributes={}):
        """
        
        :param value: DESCRIPTION
        :type value: TYPE
        :param parent: DESCRIPTION
        :type parent: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        parent.append(self._convert_tag_to_capwords(value.to_xml()))
        
    def _write_provenance(self, parent, value, attributes={}):
        """
        add new creation time and creating application

        :param parent: DESCRIPTION
        :type parent: TYPE
        :param value: DESCRIPTION
        :type value: TYPE
        :param attributes: DESCRIPTION, defaults to {}
        :type attributes: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.provenance.creating_application = "mt_metadata 0.1.5"
        self.provenance.create_time = mttime.get_now_utc()
        
        self._write_element(parent, self.provenance)

    def _read_field_notes(self, root_dict):
        """
        Field notes are odd so have a special reader to do it piece by
        painstaking piece.

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.field_notes = []
        for run in root_dict["field_notes"]:
            f = meta_classes["field_notes"]()
            f.run = run["run"]
            f.instrument.from_dict({"instrument": run["instrument"]})
            f.sampling_rate = run["sampling_rate"]
            f.start = run["start"]
            f.end = run["end"]
            f.comments.from_dict({"comments": run["comments"]})
            f.errors = run["errors"]

            if isinstance(run["magnetometer"], list):
                f.magnetometer = []
                for mag in run["magnetometer"]:
                    m = meta_classes["magnetometer"]()
                    m.from_dict({"magnetometer": mag})
                    f.magnetometer.append(m)
            else:
                f.magnetometer = []
                m = meta_classes["magnetometer"]()
                m.from_dict({"magnetometer": run["magnetometer"]})
                f.magnetometer.append(m)

            if isinstance(run["dipole"], list):
                f.dipole = []
                for mag in run["dipole"]:
                    m = meta_classes["dipole"]()
                    m.from_dict({"dipole": mag})
                    f.dipole.append(m)
            else:
                m = meta_classes["dipole"]()
                m.from_dict({"dipole": run["dipole"]})
                f.dipole.append(m)

            self.field_notes.append(f)
            
    def _write_field_notes(self, parent, key, attributes={}):
        """
        """
        
        for fn in self.field_notes:
            fn_element = self._convert_tag_to_capwords(fn.to_xml())
            for dp in fn.dipole:
                dp_element = self._convert_tag_to_capwords(dp.to_xml())
                for electrode in dp.electrode:
                    self._write_element(dp_element, electrode)
                fn_element.append(dp_element)
            for mag in fn.magnetometer:
                self._write_element(fn_element, mag)
            parent.append(fn_element)
        

    def _read_statistical_estimates(self, root_dict):
        """
        Read in statistical estimate descriptions

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.statistical_estimates.estimates_list = root_dict["statistical_estimates"][
            "estimate"
        ]

    def _write_statistical_estimates(self, parent, key, attributes={}):
        section = self._write_single(parent, key, None)
        for estimate in self.statistical_estimates.estimates_list:
            self._write_element(section, estimate)

    def _read_data_types(self, root_dict):
        """
        Read in data types

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.data_types.data_types_list = root_dict["data_types"]["data_type"]

    def _write_data_types(self, parent, key, attributes={}):
        section = self._write_single(parent, key, None)
        for estimate in self.data_types.data_types_list:
            self._write_element(section, estimate)

    def _read_site_layout(self, root_dict):
        """
        read site layout into the proper input/output channels

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        # read input channels
        for ch in ["input_channels", "output_channels"]:
            ch_list = []
            try:
                c_list = root_dict["site_layout"][ch]["magnetic"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"magnetic": ch_dict} for ch_dict in c_list]

            except (KeyError):
                pass

            try:
                c_list = root_dict["site_layout"][ch]["electric"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"electric": ch_dict} for ch_dict in c_list]
            except (KeyError):
                pass

            setattr(self.site_layout, ch, ch_list)
            
    def _write_site_layout(self, parent, key, attributes={}):
        section = self._write_single(parent, key, None)
        
        ch_in = self._write_single(section, "input_channels", None)
        for ch in self.site_layout.input_channels:
            self._write_element(ch_in, ch)
    
        
        ch_out = self._write_single(section, "output_channels", None)
        for ch in self.site_layout.output_channels:
            self._write_element(ch_out, ch)  

    def _read_data(self, root_dict):
        """
        Read data use
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.data = emtf_xml.TransferFunction()
        self.data.read_data(root_dict)
        
    def _write_data(self, parent, key, attributes={}):
        """
        write data blocks
        """
        data_element = self._write_single(parent, "Data", None, {"count": str(self.data.period.size)})
        self.data.write_data(data_element)
        

    def _convert_keys_to_lower_case(self, root_dict):
        """
        Convert the key names to lower case and separated by _ if
        needed

        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        res = OrderedDict()
        if isinstance(root_dict, (dict, OrderedDict)):
            for key in root_dict.keys():
                new_key = validate_attribute(key)
                res[new_key] = root_dict[key]
                if isinstance(res[new_key], (dict, OrderedDict, list)):
                    res[new_key] = self._convert_keys_to_lower_case(res[new_key])
        elif isinstance(root_dict, list):
            res = []
            for item in root_dict:
                item = self._convert_keys_to_lower_case(item)
                res.append(item)
        return res
    
    def _capwords(self, value):
        """
        convert to capwords, could use string.capwords, but this seems
        easy enough
        
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        return value.replace("_", " ").title().replace(" ", "")
    
    def _convert_tag_to_capwords(self, element):
        """
        convert back to capwords representation for the tag
        
        :param element: DESCRIPTION
        :type element: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        for item in element.iter():
            item.tag = self._capwords(item.tag)
            
        return element


    @property
    def survey_metadata(self):
        survey_obj = Survey()
        if self._root_dict is not None:
            survey_obj.acquired_by.author = self.site.acquired_by
            survey_obj.citation_dataset.doi = self.copyright.citation.survey_d_o_i
            survey_obj.country = self.site.country
            survey_obj.datum = self.site.location.datum
            survey_obj.geographic_name = self.site.survey
            survey_obj.id = self.site.survey
            survey_obj.project = self.site.project
            survey_obj.time_period.start = self.site.start
            survey_obj.time_period.end = self.site.end

        return survey_obj

    @property
    def station_metadata(self):
        s = Station()
        if self._root_dict is not None:
            s.acquired_by.author = self.site.acquired_by
            s.channels_recorded = [d.name for d in self.site_layout.input_channels] + [
                d.name for d in self.site_layout.output_channels
            ]
            s.data_type = self.sub_type.lower().split("_")[0]
            s.geographic_name = self.site.name
            s.id = self.site.id
            s.location.from_dict(self.site.location.to_dict())
            s.orientation.angle_to_geographic_north = (
                self.site.orientation.angle_to_geographic_north
            )
            s.provenance.software.name = self.provenance.creating_application
            s.provenance.creation_time = self.provenance.create_time
            s.provenance.creator.author = self.provenance.creator.name
            s.provenance.creator.email = self.provenance.creator.email
            s.provenance.creator.organization = self.provenance.creator.org
            s.provenance.creator.url = self.provenance.creator.org_url
            s.provenance.submitter.author = self.provenance.submitter.name
            s.provenance.submitter.email = self.provenance.submitter.email
            s.provenance.submitter.organization = self.provenance.submitter.org
            s.provenance.submitter.url = self.provenance.submitter.org_url
            s.time_period.start = self.site.start
            s.time_period.end = self.site.end
            s.transfer_function.sign_convention = self.processing_info.sign_convention
            s.transfer_function.processed_by = self.processing_info.processed_by
            s.transfer_function.software.author = (
                self.processing_info.processing_software.author
            )
            s.transfer_function.software.name = (
                self.processing_info.processing_software.name
            )
            s.transfer_function.software.last_updated = (
                self.processing_info.processing_software.last_mod
            )
            s.transfer_function.remote_references = (
                self.processing_info.processing_tag.split("_")
            )
            s.transfer_function.runs_processed = self.site.run_list
            s.transfer_function.processing_parameters.append(
                {"type": self.processing_info.remote_ref.type}
            )

            for run in self.field_notes:
                r = Run()
                r.data_logger.id = run.instrument.id
                r.data_logger.name = run.instrument.name
                r.data_logger.manufacturer = run.instrument.manufacturer
                r.sample_rate = run.sampling_rate
                r.time_period.start = run.start
                r.time_period.end = run.end

                if len(run.magnetometer) == 1:
                    for comp in ["hx", "hy", "hz"]:
                        c = getattr(r, comp)
                        c.component = comp
                        c.sensor.id = run.magnetometer[0].id
                        c.sensor.name = run.magnetometer[0].name
                        c.sensor.manufacturer = run.magnetometer[0].manufacturer
                else:
                    for mag in run.magnetometer:
                        comp = mag.name().lower()
                        c = getattr(r, comp)
                        c.component = comp
                        c.sensor.id = mag.id
                        c.sensor.name = mag.name
                        c.sensor.manufacturer = mag.manufacturer
                        c.translated_azimuth = mag.azimuth

                for dp in run.dipole:
                    comp = dp.name.lower()
                    c = getattr(r, comp)
                    c.component = comp
                    c.translated_azimuth = dp.azimuth
                    c.dipole_length = dp.length
                    for pot in dp.electrode:
                        if pot.location.lower() in ["n", "e"]:
                            c.positive.id = pot.number
                            c.positive.type = pot.value
                            c.positive.manufacture = dp.manufacturer
                        elif pot.location.lower() in ["s", "w"]:
                            c.negative.id = pot.number
                            c.negative.type = pot.value
                            c.negative.manufacture = dp.manufacturer

                s.run_list.append(r)

        return s


def read_emtfxml(fn):
    """
    read an EMTF XML file

    :param fn: DESCRIPTION
    :type fn: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    from mt_metadata.transfer_functions.core import TF

    obj = EMTFXML()
    obj.read(fn)

    emtf = TF()
    emtf.survey_metadata = obj.survey_metadata
    emtf.station_metadata = obj.station_metadata
    emtf.data["z"] = obj.tf.z
    emtf.data["z_var"] = obj.tf.z_var
    emtf.data["z_invsigcov"] = obj.tf.z_invsigcov
    emtf.data["z_residcov"] = obj.tf.z_residcov
    
    emtf.data["t"] = obj.tf.t
    emtf.data["t_var"] = obj.tf.t_var
    emtf.data["t_invsigcov"] = obj.tf.t_invsigcov
    emtf.data["t_residcov"] = obj.tf.t_residcov
    emtf.data["period"] = obj.tf.periods
    
    return emtf


def write_emtfxml(tf_object, fn=None):
    """
    Write an XML file from a TF object

    :param tf_obj: DESCRIPTION
    :type tf_obj: TYPE
    :param fn: DESCRIPTION, defaults to None
    :type fn: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """
    
    from mt_metadata.transfer_functions.core import TF

    if not isinstance(tf_object, TF):
        raise ValueError(
            "Input must be an mt_metadata.transfer_functions.core.TF object"
            )
        
    emtf = EMTFXML()
    emtf.description = "Magnetotelluric transfer functions"
    pass
