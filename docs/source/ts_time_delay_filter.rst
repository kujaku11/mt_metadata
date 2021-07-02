.. role:: red
.. role:: blue
.. role:: navy

Time_delay_filter
=================


:navy:`name`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **name**                                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Name of filter applied or to be applied. If   | "[counts2mv, lo|
       |                                              | more than one filter input as a comma         | wpass_magnetic]|
       | **Units**: None                              | separated list.                               | "              |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: name list                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`comments`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **comments**                                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Any comments about the filter.                | ambient air    |
       |                                              |                                               | temperature    |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`type`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **type**                                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Type of filter.                               | table          |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: controlled vocabulary             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`units_in`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **units_in**                                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Name of the input units to the filter. Should | count          |
       |                                              | be all lowercase and separated with an        |                |
       | **Units**: None                              | underscore, use 'per' if units are divided    |                |
       |                                              | and '-' if units are multiplied.              |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: alpha numeric                     |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`units_out`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **units_out**                                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Name of the output units.  Should be all      | millivolt      |
       |                                              | lowercase and separated with an underscore,   |                |
       | **Units**: None                              | use 'per' if units are divided and '-' if     |                |
       |                                              | units are multiplied.                         |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: alpha numeric                     |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`calibration_date`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **calibration_date**                         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Most recent date of filter calibration in ISO | 2020-01-01     |
       |                                              | format of YYY-MM-DD.                          |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: date                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`gain`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **gain**                                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | scalar gain of the filter across all          | 1.0            |
       |                                              | frequencies, producted with any frequency     |                |
       | **Units**: None                              | depenendent terms                             |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`delay`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **delay**                                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | The delay interval of the filter. This should | -0.201         |
       |                                              | be a single number.                           |                |
       | **Units**: second                            |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
