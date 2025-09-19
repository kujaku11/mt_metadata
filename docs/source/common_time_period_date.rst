.. role:: red
.. role:: blue
.. role:: navy

TimePeriodDate
==============


:navy:`end_date`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **end_date**                                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | End date and time of collection in UTC.       | 2020-02-04     |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime |            |                                               |                |
       | mt_metadata.common.mttime.MDate              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MDate                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`start_date`
~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **start_date**                               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Start date and time of collection in UTC.     | 2020-02-01     |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime |            |                                               |                |
       | mt_metadata.common.mttime.MDate              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MDate                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
