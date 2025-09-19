.. role:: red
.. role:: blue
.. role:: navy

ChannelBase
===========


:navy:`channel_number`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **channel_number**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Channel number on the data logger.            | 1              |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'int'>                      |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 0                               |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`channel_id`
~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **channel_id**                               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | channel id given by the user or data logger   | 1001.11        |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`comments.author`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **comments.author**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | person who authored the comment               | J. Pedantic    |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`comments.time_stamp`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **comments.time_stamp**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Date and time of in UTC of when comment was   | 2020-02-       |
       |                                              | made.                                         | 01T09:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime |            |                                               |                |
       | None                                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`comments.value`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **comments.value**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | comment string                                | failure at     |
       |                                              |                                               | midnight.      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | list | None                  |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`component`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **component**                                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Name of the component measured, can be        | ex             |
       |                                              | uppercase and/or lowercase.  For now electric |                |
       | **Units**: None                              | channels should start with an 'e' and         |                |
       |                                              | magnetic channels start with an 'h', followed |                |
       | **Type**: <class 'str'>                      | by the component. If there are multiples of   |                |
       |                                              | the same channel the name could include an    |                |
       |                                              | integer.  {type}{component}{number} --> Ex01. |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: ""                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`measurement_azimuth`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **measurement_azimuth**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Horizontal azimuth of the channel in          | 0.0            |
       |                                              | measurement coordinate system spcified in     |                |
       | **Units**: degrees                           | station.orientation.reference_frame.  Default |                |
       |                                              | reference frame is a geographic right-handed  |                |
       | **Type**: <class 'float'>                    | coordinate system with north=0, east=90,      |                |
       |                                              | vertical=+ downward.                          |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 0.0                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`measurement_tilt`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **measurement_tilt**                         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Vertical tilt of the channel in measurement   | 0              |
       |                                              | coordinate system specified in                |                |
       | **Units**: degrees                           | station.orientation.reference_frame.  Default |                |
       |                                              | reference frame is a geographic right-handed  |                |
       | **Type**: <class 'float'>                    | coordinate system with north=0, east=90,      |                |
       |                                              | vertical=+ downward.                          |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 0.0                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`sample_rate`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **sample_rate**                              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Digital sample rate                           | 8.0            |
       |                                              |                                               |                |
       | **Units**: samples per second                |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'float'>                    |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 0.0                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`translated_azimuth`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **translated_azimuth**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Horizontal azimuth of the channel in          | 0.0            |
       |                                              | translated coordinate system, this should     |                |
       | **Units**: degrees                           | only be used for derived product.  For        |                |
       |                                              | instance if you collected your data in        |                |
       | **Type**: float | None                       | geomagnetic coordinates and then translated   |                |
       |                                              | them to geographic coordinates you would set  |                |
       |                                              | measurement_azimuth=0,                        |                |
       |                                              | translated_azimuth=-12.5 for a declination    |                |
       |                                              | angle of N12.5E.                              |                |
       |                                              |                                               |                |
       |                                              | angle of N12.5E.                              |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`translated_tilt`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **translated_tilt**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Tilt of channel in translated coordinate      | 0.0            |
       |                                              | system, this should only be used for derived  |                |
       | **Units**: degrees                           | product.  For instance if you collected your  |                |
       |                                              | data using a tripod you would set             |                |
       | **Type**: float | None                       | measurement_tilt=45, translated_tilt=0 for a  |                |
       |                                              | vertical component.                           |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
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
       | **Required**: :red:`True`                    | Data type for the channel, should be a        | temperature    |
       |                                              | descriptive word that a user can understand.  |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'str'>                      |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: base                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`units`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **units**                                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Units of the data, should be in SI units and  | celsius        |
       |                                              | represented as the full name of the unit all  |                |
       | **Units**: None                              | lowercase.  If a complex unit use 'per' and   |                |
       |                                              | '-'.                                          |                |
       | **Type**: <class 'str'>                      |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: ""                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.warnings`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.warnings**                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | any warnings about the data that should be    | periodic       |
       |                                              | noted                                         | pipeline noise |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.good_from_period`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.good_from_period**            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Data are good for periods larger than this    | 0.01           |
       |                                              | number                                        |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.good_to_period`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.good_to_period**              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Data are good for periods smaller than this   | 1000           |
       |                                              | number                                        |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.flag`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.flag**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Flag for data quality                         | 0              |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: int | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.comments.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.comments.author**             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | person who authored the comment               | J. Pedantic    |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.comments.time_stamp`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.comments.time_stamp**         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Date and time of in UTC of when comment was   | 2020-02-       |
       |                                              | made.                                         | 01T09:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime |            |                                               |                |
       | None                                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.comments.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.comments.value**              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | comment string                                | failure at     |
       |                                              |                                               | midnight.      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | list | None                  |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.rating.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.rating.author**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Author of who rated the data.                 | gradstudent ace|
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.rating.method`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.rating.method**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | The method used to rate the data.             | standard       |
       |                                              |                                               | deviation      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`data_quality.rating.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **data_quality.rating.value**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | A rating from 1-5 where 1 is bad and 5 is     | 4              |
       |                                              | good and 0 if unrated.                        |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: int | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`filters`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **filters**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Filter data for the channel.                  | AppliedFilter(n|
       |                                              |                                               | ame='filter_nam|
       | **Units**: None                              |                                               | e',            |
       |                                              |                                               | applied=True,  |
       | **Type**: list[mt_metadata.timeseries.filtere|                                               | stage=1)       |
       | d.AppliedFilter]                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: list                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_period.end`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.end**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | End date and time of collection in UTC.       | 2020-02-       |
       |                                              |                                               | 04T16:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_period.start`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.start**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Start date and time of collection in UTC.     | 2020-02-       |
       |                                              |                                               | 01T09:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.id`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.id**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Given FDSN archive ID name.                   | MT001          |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.network`
~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.network**                             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Given two character FDSN archive network      | EM             |
       |                                              | code. Needs to be 2 alpha numeric characters. |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.channel_code`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.channel_code**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Three character FDSN channel code.            | LQN            |
       |                                              | http://docs.fdsn.org/projects/source-         |                |
       | **Units**: None                              | identifiers/en/v1.0/channel-codes.html        |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.new_epoch`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.new_epoch**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Boolean telling if a new epoch needs to be    | False          |
       |                                              | created or not.                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: bool | None                        |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.alternate_code`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.alternate_code**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Alternate Code                                | _INT-NON_FDSN  |
       |                                              |                                               | .UNRESTRICTED  |
       | **Units**: None                              |                                               | _US-ALL _US-MT |
       |                                              |                                               | _US-MT-TA      |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`fdsn.alternate_network_code`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **fdsn.alternate_network_code**              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Alternate Network Code                        | _INT-NON_FDSN  |
       |                                              |                                               | .UNRESTRICTED  |
       | **Units**: None                              |                                               | _US-ALL _US-MT |
       |                                              |                                               | _US-MT-TA      |
       | **Type**: str | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
