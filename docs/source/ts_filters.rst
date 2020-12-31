.. role:: red
.. role:: blue
.. role:: navy


Filters
=======

.. contents::  :local:

.. note:: This is still a work in progress.

``Filters`` is a table that holds information on any filters that need
to be applied to get physical units, and/or filters that were applied to
the data to analyze the signal. This includes calibrations, notch
filters, conversion of counts to units, etc. The actual filter will be
an array of numbers contained within an array named ``name`` and
formatted according to ``type``. The preferred format for a filter is a
look-up table which programatically can be converted to other formats.

It is important to note that filters will be identified by name and must
be consistent throughout the file. Names should be descriptive and self
evident. Examples:

-  ``coil_2284`` :math:`\longrightarrow` induction coil Number 2284

-  ``counts2mv`` :math:`\longrightarrow` conversion from counts to mV

-  ``e_gain`` :math:`\longrightarrow` electric field gain

-  ``datalogger_response_024`` :math:`\longrightarrow` data logger
   Number 24 response

-  ``notch_60hz`` :math:`\longrightarrow` notch filter for 60 Hz and
   harmonics

-  ``lowpass_10hz`` :math:`\longrightarrow` low pass filter below 10 Hz

In each channel there are keys to identify filters that can or have been
applied to the data to get an appropriate signal. This can be a list of
filter names or a single filter name. An ``applied`` key also exists for
the user to input whether that filter has been applied. A single Boolean
can be provided ``True`` if all filters have been applied, or ``False``
if none of the filters have been applied. Or ``applied`` can be a list
the same length as ``names`` identifying if the filter has been applied.
For example ``name: "[counts2mv, notch_60hz, e_gain]"`` and
``applied: "[True, False, True]`` would indicate that ``counts2mv`` and
``e_gain`` have been applied but ``noth_60hz`` has not.

Filter Attributes
------------------ 

:navy:`type`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **type**                                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Filter type. Options: [look up | lookup         |
       |                                              |  ;  poles zeros  ;  converter  |                |
       | **Units**: None                              |  ;  FIR  ;  ...]               |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`name`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **name**                                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Unique name for the filter     | counts2mv      |
       |                                              | such that it is easy to query. |                |
       | **Units**: None                              | See above for some examples.   |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Alpha Numeric                     |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`units_in`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **units_in**                                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | The input units for the        | counts         |
       |                                              | filter. Should be SI units or  |                |
       | **Units**: None                              | counts.                        |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`units_out`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **units_out**                                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | The output units for the       | millivolts     |
       |                                              | filter. Should be SI units or  |                |
       | **Units**: None                              | counts.                        |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`calibration_date`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **calibration_date**                         | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | If the filter is a calibration | 2010-01-01     |
       |                                              |                                | T00:00:00      |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date Time                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+


Example Filter JSON
-------------------

::

   {
       "filter":{
           "type": "look up",
            "name": "counts2mv",
            "units_in": "counts",
            "units_out": "mV",
            "calibration_date": "2015-07-01",
           "comments": "Accurate to 0.001 mV"
       }
   }
