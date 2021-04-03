# mt_metadata
 Standard MT metadata

[![codecov](https://codecov.io/gh/kujaku11/mt_metadata/branch/main/graph/badge.svg?token=1WYF0G1L3D)](https://codecov.io/gh/kujaku11/mt_metadata)

![example workflow name](https://github.com/kujaku11/mt_metadata/workflows/TestingInConda/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MT Metadata has been and is being developed to standardize magnetotelluric metadata, well, at least create tools for standards that are generally accepted.  This include the two main types of magnetotelluric data:

    * Time Series 
    * Transfer Functions

Most people will be using the transfer functions, but a lot of that metadata comes from the time series metadata.  This module supports both and has tried to make them more or less seamless to reduce complication.

Each metadata keyword has an associated standard that goes with it.  These are stored internally in JSON file.  The JSON files are read in when the package is loaded to initialize the standards.  Each keyword is described by:  

    * **type** - How the value should be represented based on very basic types
	
		- *string*
		- *number* (float or integer)
		- *boolean*
		
	* **required** -  A boolean (True or False) denoting whether the metadata key word required to represent the data.
	* **style** - How the value should be represented within the type.  For instance is the value a controlled string where there are only a few options, or is the value a controlled naming convention where only a 5 character alpha-numeric string is allowed.  The styles are
	
		- *Alpha Numeric* a string with alphabetic and numberic characters
		- *Free Form* a free form string
		- *Controlled Vocabulary* only certain values are allowed according to **options**
		- *Date* a date and/or time string in ISO format
		- *Number* a float or integer
		- *Boolean* the value can only be True or False 
		
	* **units** - Units of the value
	* **description** - Full description of what the metadata key is meant to convey.
	* **options** - Any options of a **Controlled Vocabulary** style.
	* **alias** - Any aliases that may represent the same metadata key.
	* **example** - An example value to inform the user.

All input values are internally validated according to the definition providing a robust way to standardize metadata.  

Supported input/output formats are:

    - XML
    - JSON
    - python Dictionary
    - Pandas Series (coming soon)

The time series module is more mature than the transfer function module at the moment, and this is still a work in progress.

Documentation can be found at: [MT Metadata Documentation](https://mt-metadata.readthedocs.io/en/latest/)
