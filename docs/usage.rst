===========
Usage
===========

.. _ref-usage:


Basic
-------------

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
    * **default**: Default value.  If **required** is True value will be set to this, otherwise a type of None is set.
    
When an attribute of :class:`mt_metadata.base.metadata.Base` is set the attribute will be validated against this standard.  The validators will try to put the attribute into the proper data type and style.  Therefore if the standards change just the JSON files should be changed.  This will hopefully make it easier to expand different standards.  

.. toctree::
    :maxdepth: 2
    :caption: Examples
    
    source/notebooks/usage_examples.ipynb
