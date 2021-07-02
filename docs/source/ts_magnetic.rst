.. role:: red
.. role:: blue
.. role:: navy

Magnetic
========


:navy:`h_field_min.start`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **h_field_min.start**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Minimum magnetic field strength at beginning  | 40345.1        |
       |                                              | of measurement.                               |                |
       | **Units**: nt                                |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`h_field_min.end`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **h_field_min.end**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Minimum magnetic field strength at end of     | 50453.2        |
       |                                              | measurement.                                  |                |
       | **Units**: nt                                |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`h_field_max.start`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **h_field_max.start**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Maximum magnetic field strength at beginning  | 34565.2        |
       |                                              | of measurement.                               |                |
       | **Units**: nt                                |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`h_field_max.end`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **h_field_max.end**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Maximum magnetic field strength at end of     | 34526.1        |
       |                                              | measurement.                                  |                |
       | **Units**: nt                                |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

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
       | **Type**: integer                            |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
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
       | **Required**: :blue:`False`                  | Any comments about the channel.               | ambient air    |
       |                                              |                                               | temperature was|
       | **Units**: None                              |                                               | chilly, ice on |
       |                                              |                                               | cables         |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Required**: :red:`True`                    | Name of the component measured, can be        | T              |
       |                                              | uppercase and/or lowercase.  For now electric |                |
       | **Units**: None                              | channels should start with an 'e' and         |                |
       |                                              | magnetic channels start with an 'h', followed |                |
       | **Type**: string                             | by the component. If there are multiples of   |                |
       |                                              | the same channel the name could include an    |                |
       | **Style**: controlled vocabulary             | integer.  {type}{component}{number} --> Ex01. |                |
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
       | **Required**: :red:`True`                    | Horizontal azimuth of the channel in          | 0              |
       |                                              | measurement coordinate system spcified in     |                |
       | **Units**: degrees                           | station.orientation.reference_frame.  Default |                |
       |                                              | reference frame is a geographic right-handed  |                |
       | **Type**: float                              | coordinate system with north=0, east=90,      |                |
       |                                              | vertical=+ downward.                          |                |
       | **Style**: number                            |                                               |                |
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
       | **Type**: float                              | coordinate system with north=0, east=90,      |                |
       |                                              | vertical=+ downward.                          |                |
       | **Style**: number                            |                                               |                |
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
       | **Required**: :red:`True`                    | Digital sample rate                           | 8              |
       |                                              |                                               |                |
       | **Units**: samples per second                |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
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
       | **Required**: :blue:`False`                  | Horizontal azimuth of the channel in          | 0              |
       |                                              | translated coordinate system, this should     |                |
       | **Units**: degrees                           | only be used for derived product.  For        |                |
       |                                              | instance if you collected your data in        |                |
       | **Type**: float                              | geomagnetic coordinates and then translated   |                |
       |                                              | them to geographic coordinates you would set  |                |
       | **Style**: number                            | measurement_azimuth=0,                        |                |
       |                                              | translated_azimuth=-12.5 for a declination    |                |
       |                                              | angle of N12.5E.                              |                |
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
       | **Required**: :blue:`False`                  | Tilt of channel in translated coordinate      | 0              |
       |                                              | system, this should only be used for derived  |                |
       | **Units**: degrees                           | product.  For instance if you collected your  |                |
       |                                              | data using a tripod you would set             |                |
       | **Type**: float                              | measurement_tilt=45, translated_tilt=0 for a  |                |
       |                                              | vertical component.                           |                |
       | **Style**: number                            |                                               |                |
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
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: controlled vocabulary             |                                               |                |
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
       | **Required**: :blue:`False`                  | Any warnings about the data that should be    | periodic       |
       |                                              | noted.                                        | pipeline noise |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Required**: :blue:`False`                  | Author of who rated the data.                 | gradstundet ace|
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Required**: :blue:`False`                  | The method used to rate the data.             | standard       |
       |                                              |                                               | deviation      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Type**: integer                            |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`filter.name`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **filter.name**                              | **Description**                               | **Example**    |
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

:navy:`filter.applied`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **filter.applied**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Boolean if filter has been applied or not. If | "[True, False]"|
       |                                              | more than one filter input as a comma         |                |
       | **Units**: None                              | separated list.  Needs to be the same length  |                |
       |                                              | as name or if only one entry is given it is   |                |
       | **Type**: boolean                            | assumed to apply to all filters listed.       |                |
       |                                              |                                               |                |
       | **Style**: name list                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`filter.comments`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **filter.comments**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Any comments on filters.                      | low pass is not|
       |                                              |                                               | calibrated     |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: name                              |                                               |                |
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
       | **Required**: :red:`True`                    | End date and time of collection in UTC.       | 2020-02-04T16:2|
       |                                              |                                               | 3:45.453670+00:|
       | **Units**: None                              |                                               | 00             |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: time                              |                                               |                |
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
       | **Required**: :red:`True`                    | Start date and time of collection in UTC.     | 2020-02-01T09:2|
       |                                              |                                               | 3:45.453670+00:|
       | **Units**: None                              |                                               | 00             |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: time                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`sensor.id`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **sensor.id**                                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Instrument ID number can be serial number or  | mt01           |
       |                                              | a designated ID.                              |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`sensor.manufacturer`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **sensor.manufacturer**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Who manufactured the instrument.              | mt gurus       |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`sensor.type`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **sensor.type**                              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Description of the instrument type.           | broadband      |
       |                                              |                                               | 32-bit         |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`sensor.model`
~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **sensor.model**                             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Model version of the instrument.              | falcon5        |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
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
       | **Required**: :blue:`False`                  | Given FDSN archive ID name.                   | MT001          |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: alpha numeric                     |                                               |                |
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
       | **Required**: :blue:`False`                  | Given two character FDSN archive network      | EM             |
       |                                              | code.                                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: alpha numeric                     |                                               |                |
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
       | **Required**: :blue:`False`                  | Three character FDSN channel code.            | LQN            |
       |                                              | http://docs.fdsn.org/projects/source-         |                |
       | **Units**: None                              | identifiers/en/v1.0/channel-codes.html        |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: alpha numeric                     |                                               |                |
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
       | **Required**: :blue:`False`                  | Boolean telling if a new epoch needs to be    | False          |
       |                                              | created or not.                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: boolean                            |                                               |                |
       |                                              |                                               |                |
       | **Style**: name                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`location.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **location.latitude**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Latitude of location in datum specified at    | 23.134         |
       |                                              | survey level.                                 |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`location.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **location.longitude**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Longitude of location in datum specified at   | 14.23          |
       |                                              | survey level.                                 |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`location.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **location.elevation**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Elevation of location in datum specified at   | 123.4          |
       |                                              | survey level.                                 |                |
       | **Units**: meters                            |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
