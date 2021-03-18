=====
Usage
=====

.. contents::  :local:

**mt_metadata** is written to make read/writing magnetotelluric (MT) metadata easier.

.. hint:: mt_metadata is comprehensively logged, therefore if any problems arise you can always check the mt_metadata_debug.log and the mt_metadata_error.log, which will be written to mt_metadata/logs.

Each element or category in the metadata standards is a :class:`mt_metadata.base.metadata.Base` which controls how the metadata is validated.  The way the validation is controlled is based on standards in JSON files in each of the modules.  For example the standards for timeseries are in :mod:`mt_metadata.timeseries.stanadards`. In each JSON file is information that describes each attribute.  This includes:

	* **alias**: An alternate name that the attribute might have
	* **description**: Full description of what the attribute represents and means
	* **example**: Good example of how the attribute should be used
	* **options**: If the style is controlled vocabulary provide accepted options
	* **required**: [ True | False ] True if the attribute is required
	* **style**: If type is string, how the string should be styled, e.g. datetime
	* **type**: Python data type [ str | int | float | bool ]
	* **units**: Units of the attribute in SI full name, e.g. millivolts
	
When an attribute of :class:`mt_metadata.base.metadata.Base` is set the attribute will be validated against this standard.  The validators will try to put the attribute into the proper data type and style.  Therefore if the standards change just the JSON files should be changed.  This will hopefully make it easier to expand different standards.  
 

Examples
^^^^^^^^^^^^^^^^^

Working with Metadata
""""""""""""""""""""""

Base provides convenience filters to input and output metadata in different formats XML, JSON, Python dictionary, Pandas Series.  It also provides functions to help the user understand what's inside.    

.. code-block:: python
	
	>>> from mt_metadata.base import Base
	>>> example = Base()
	>>> example
	{
	    "base": {}
    }

Have a look at :class:`mt_metadata.timeseries.Station`
	
.. code-block:: python
	
	>>> from mt_metadata.timeseries import Station
	>>> example = Station()
	>>> example
	{
		"station": {
			"acquired_by.author": null,
			"channels_recorded": [],
			"data_type": null,
			"geographic_name": null,
			"id": null,
			"location.declination.model": null,
			"location.declination.value": null,
			"location.elevation": 0.0,
			"location.latitude": 0.0,
			"location.longitude": 0.0,
			"orientation.method": null,
			"orientation.reference_frame": "geographic",
			"provenance.creation_time": "2021-02-24T06:16:40.657280+00:00",
			"provenance.software.author": null,
			"provenance.software.name": null,
			"provenance.software.version": null,
			"provenance.submitter.author": null,
			"provenance.submitter.email": null,
			"provenance.submitter.organization": null,
			"run_list": [],
			"time_period.end": "1980-01-01T00:00:00+00:00",
			"time_period.start": "1980-01-01T00:00:00+00:00"
		}
	}
	  
	
Metadata Help
"""""""""""""""""

To get a list of attributes in the metadata class

.. code-block:: python

	>>> example.get_attribute_list()
	['acquired_by.author',
	 'acquired_by.comments',
	 'channel_layout',
	 'channels_recorded',
	 'comments',
	 'data_type',
	 'fdsn.channel_code',
	 'fdsn.id',
	 'fdsn.network',
	 'fdsn.new_epoch',
	 'geographic_name',
	 'id',
	 'location.declination.comments',
	 'location.declination.model',
	 'location.declination.value',
	 'location.elevation',
	 'location.latitude',
	 'location.longitude',
	 'orientation.method',
	 'orientation.reference_frame',
	 'provenance.comments',
	 'provenance.creation_time',
	 'provenance.log',
	 'provenance.software.author',
	 'provenance.software.name',
	 'provenance.software.version',
	 'provenance.submitter.author',
	 'provenance.submitter.email',
	 'provenance.submitter.organization',
	 'run_list',
	 'time_period.end',
	 'time_period.start']

To get help with any metadata attribute you can use

.. code-block:: python

	>>> example.metadata.attribute_information('id')
	id:
		alias: []
		description: Station ID name.  This should be an alpha numeric name that is typically 5-6 characters long.  Commonly the project name in 2 or 3 letters and the station number.
		example: MT001
		options: []
		required: True
		style: alpha numeric
		type: string
		units: None
	
If no argument is given information for all metadata attributes will be printed.

Creating New Attributes
"""""""""""""""""""""""""

If you want to add new standard attributes to the metadata you can do this through :func:`mt_metadata.base.Base.add_base_attribute method`

>>> extra = {'type': str,
...          'style': 'controlled vocabulary',
...          'required': False,
...          'units': 'celsius',
...          'description': 'local temperature',
...          'alias': ['temp'],
...          'options': [ 'ambient', 'air', 'other'],
...          'example': 'ambient'}
>>> station.add_base_attribute('temperature', 'ambient', extra)

Dictionary Input/Output
"""""""""""""""""""""""""

You can input a dictionary of attributes

.. note:: The dictionary must be of the form {'level': {'key': 'value'}}, where 'level' is the name of the metadata class. e.g. station.

.. code-block:: python

	>>> meta_dict = {'station': {'id': 'MT010'}}
	>>> station.from_dict(meta_dict)
	>>> exiting_station.metadata.to_dict()
	{'station': OrderedDict([('acquired_by.author', None),
              ('channels_recorded', []),
              ('data_type', None),
              ('geographic_name', None),
              ('id', 'MT010'),
              ('location.declination.model', None),
              ('location.declination.value', None),
              ('location.elevation', 0.0),
              ('location.latitude', 0.0),
              ('location.longitude', 0.0),
              ('orientation.method', None),
              ('orientation.reference_frame', 'geographic'),
              ('provenance.creation_time', '2021-02-24T06:21:49.078957+00:00'),
              ('provenance.software.author', None),
              ('provenance.software.name', None),
              ('provenance.software.version', None),
              ('provenance.submitter.author', None),
              ('provenance.submitter.email', None),
              ('provenance.submitter.organization', None),
              ('run_list', []),
              ('time_period.end', '1980-01-01T00:00:00+00:00'),
              ('time_period.start', '1980-01-01T00:00:00+00:00')])}


JSON Input/Output
"""""""""""""""""""""""""""

JSON input is as a string, therefore you will need to read the file first.

.. code-block:: python

	>>> json_string = '{"station": {"archive_id": "MT010"}}
	>>> existing_station.metadata.from_json(json_string)
	>>> print(existing_station.metadata.to_json(nested=True))	
	{
		"station": {
			"acquired_by": {
				"author": null,
				"comments": null
			},
			"archive_id": "FL001",
			"channel_layout": "X",
			"channels_recorded": [
				"Hx",
				"Hy",
				"Hz",
				"Ex",
				"Ey"
			],
			"comments": null,
			"data_type": "BB, LP",
			"geographic_name": "Beachy Keen, FL, USA",
			"hdf5_reference": "<HDF5 object reference>",
			"id": "MT010",
			"location": {
				"latitude": 29.7203555,
				"longitude": -83.4854715,
				"elevation": 0.0,
				"declination": {
					"comments": "Declination obtained from the instrument GNSS NMEA sequence",
					"model": "Unknown",
					"value": -4.1
				}
			},
			"mth5_type": "Station",
			"orientation": {
				"method": "compass",
				"reference_frame": "geographic"
			},
			"provenance": {
				"creation_time": "2020-05-29T21:08:40+00:00",
				"comments": null,
				"log": null,
				"software": {
					"author": "Anna Kelbert, USGS",
					"version": "2020-05-29",
					"name": "mth5_metadata.m"
				},
				"submitter": {
					"author": "Anna Kelbert, USGS",
					"organization": "USGS Geomagnetism Program",
					"email": "akelbert@usgs.gov"
				}
			},
			"time_period": {
				"end": "2015-01-29T16:18:14+00:00",
				"start": "2015-01-08T19:49:15+00:00"
			}
		}
	}

XML Input/Output
"""""""""""""""""""""""""""

You can input as a XML element following the form previously mentioned.  If you store your metadata in XML files you will need to read the and input the appropriate element into the metadata.

.. code-block:: python

	>>> from xml.etree import cElementTree as et
	>>> root = et.Element('station')
	>>> et.SubElement(root, 'archive_id', {'text': 'MT010'})
	>>> existing_station.from_xml(root)
	>>> print(existing_station.to_xml(string=True)
	<?xml version="1.0" ?>
	<station>
		<acquired_by>
			<author>None</author>
			<comments>None</comments>
		</acquired_by>
		<archive_id>MT010</archive_id>
		<channel_layout>X</channel_layout>
		<channels_recorded>
			<item>Hx</item>
			<item>Hy</item>
			<item>Hz</item>
			<item>Ex</item>
			<item>Ey</item>
		</channels_recorded>
		<comments>None</comments>
		<data_type>BB, LP</data_type>
		<geographic_name>Beachy Keen, FL, USA</geographic_name>
		<hdf5_reference type="h5py_reference">&lt;HDF5 object reference&gt;</hdf5_reference>
		<id>FL001</id>
		<location>
			<latitude type="float" units="degrees">29.7203555</latitude>
			<longitude type="float" units="degrees">-83.4854715</longitude>
			<elevation type="float" units="degrees">0.0</elevation>
			<declination>
				<comments>Declination obtained from the instrument GNSS NMEA sequence</comments>
				<model>Unknown</model>
				<value type="float" units="degrees">-4.1</value>
			</declination>
		</location>
		<mth5_type>Station</mth5_type>
		<orientation>
			<method>compass</method>
			<reference_frame>geographic</reference_frame>
		</orientation>
		<provenance>
			<creation_time>2020-05-29T21:08:40+00:00</creation_time>
			<comments>None</comments>
			<log>None</log>
			<software>
				<author>Anna Kelbert, USGS</author>
				<version>2020-05-29</version>
				<name>mth5_metadata.m</name>
			</software>
			<submitter>
				<author>Anna Kelbert, USGS</author>
				<organization>USGS Geomagnetism Program</organization>
				<email>akelbert@usgs.gov</email>
			</submitter>
		</provenance>
		<time_period>
			<end>2015-01-29T16:18:14+00:00</end>
			<start>2015-01-08T19:49:15+00:00</start>
		</time_period>
	</station>
		
