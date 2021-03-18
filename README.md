# mt_metadata
 Standard MT metadata

[![codecov](https://codecov.io/gh/kujaku11/mt_metadata/branch/main/graph/badge.svg?token=1WYF0G1L3D)](https://codecov.io/gh/kujaku11/mt_metadata)

![example workflow name](https://github.com/kujaku11/mt_metadata/workflows/TestingInConda/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This module is being developed to standardize magnetotelluric metadata, well, at least create tools for standards that are generally accepted.  There are two different types of magnetotelluric data:

    * Time Series 
    * Transfer Functions

Most people will end up using the transfer functions, but a lot of that metadata comes from the time series metadata.  This module supports both.

The module is built such that all metadata key words are defined by a parameters:

    - Type - built-in Python type (str, float, int, bool)
    - Style - If the type is a string, how should it be styled, a date, formatted alpha-numeric, etc.
    - Options - If the string is controlled vocaulary make sure the input is acceptable. 

All input values are internally validated according to the definition providing a robust way to standardize metadata.  

Supported input/output formats are:

    - XML
    - JSON
    - python Dictionary
    - Pandas Series (coming soon)

The time series module is more mature than the transfer function module at the moment, and this is still a work in progress.

Documentation can be found at: [MT Metadata Documentation](https://mt-metadata.readthedocs.io/en/latest/)
