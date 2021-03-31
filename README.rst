============
MT Metadata
============


.. image:: https://img.shields.io/pypi/v/mt_metadata.svg
        :target: https://pypi.python.org/pypi/mt_metadata

.. image:: https://img.shields.io/travis/kujaku11/mt_metadata.svg
        :target: https://travis-ci.com/kujaku11/mt_metadata

.. image:: https://readthedocs.org/projects/mt_metadata/badge/?version=latest
        :target: https://mt_metadata.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Archivable and exchangeable format for magnetotelluric data


* Free software: MIT license
* Documentation: https://mt_metadata.readthedocs.io.


Features
--------

This module is being developed to standardize magnetotelluric metadata, well, at least create tools for standards that are generally accepted.  There are two different types of magnetotelluric data:

    * Time Series 
    * Transfer Functions

Most people will end up using the transfer functions, but a lot of that metadata comes from the time series metadata.  This module supports both.

The module is built such that all metadata key words are defined by a parameters:

    - **Type** - built-in Python type (str, float, int, bool)
    - **Style** - If the type is a string, how should it be styled, a date, formatted alpha-numeric, etc.
    - **Options** - If the string is controlled vocaulary make sure the input is acceptable. 

All input values are internally validated according to the definition providing a robust way to standardize metadata.  

Supported input/output formats are:

    - XML
    - JSON
    - python Dictionary
    - Pandas Series (coming soon)

The time series module is more mature than the transfer function module at the moment, and this is still a work in progress.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
