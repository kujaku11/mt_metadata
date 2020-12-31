.. role:: red
.. role:: blue
.. role:: navy


Auxiliary Channels
==================

.. contents::  :local:

Auxiliary channels include state of health channels, temperature, etc.

Auxiliary Channel Attributes
----------------------------- 

:navy:`channel_number`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **channel_number**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Channel Number on the data     | 1              |
       |                                              | logger.                        |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: Integer                            |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`comments`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **comments**                                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments about the channel | Pc1 at 6pm     |
       |                                              | that would be useful to a      | local time.    |
       | **Units**: None                              | user.                          |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`component`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **component**                                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the component          | temperature    |
       |                                              | measured.  Options: [          |                |
       | **Units**: None                              | temperature  ;  battery  ;     |                |
       |                                              | ... ]                          |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`data_quality.rating.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **data_quality.rating.author**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Name of person or organization | graduate       |
       |                                              | who rated the data.            | student ace    |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`data_quality.rating.method`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **data_quality.rating.method**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | The method used to rate the    | standard       |
       |                                              | data.  Should be a descriptive | deviation      |
       | **Units**: None                              | name and not just the name of  |                |
       |                                              | a software package.  If a      |                |
       | **Type**: String                             | rating is provided             |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`data_quality.rating.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **data_quality.rating.value**                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Rating from 1-5 where 1 is bad | 4              |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: Integer                            |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`data_quality.warning`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **data_quality.warning**                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any warnings about the data    | periodic       |
       |                                              | that should be noted for       | pipeline noise |
       | **Units**: None                              | users.                         |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+
	   
:navy:`fdsn.channel_code`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **fdsn.channel_code**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | FDSN channel code, this is a   | LQN            |
       |                                              | 3 character code in the form   |                |
       | **Units**: None                              | [band][type][direction]        |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Alpha-Numeric                     |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+
	   
.. seealso:: https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/ for more information on channel codes.
	   

:navy:`filter.applied`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **filter.applied**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Boolean if filter has been     |  [True, False] |
       |                                              | applied or not. If more than   |                |
       | **Units**: None                              | one filter input as a list     |                |
       |                                              | that matches filter.names      |                |
       | **Type**: Boolean                            |                                |                |
       |                                              |                                |                |
       | **Style**: List                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`filter.comments`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **filter.comments**                          | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments on filters that   | low pass is not|
       |                                              | is important for users.        | calibrated     |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`filter.name`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **filter.name**                              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of filter applied or to   | [gain, lp_aux] |
       |                                              | be applied. If more than one   |                |
       | **Units**: None                              | filter input as a list in the  |                |
       |                                              | order in which the should be   |                |
       | **Type**: String                             | applied.                       |                |
       |                                              |                                |                |
       | **Style**: List                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.elevation**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Elevation of channel location  | 123.4          |
       |                                              | in datum specified at survey   |                |
       | **Units**: meters                            | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.latitude**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Latitude of channel location   | 23.134         |
       |                                              | in datum specified at survey   |                |
       | **Units**: decimal degrees                   | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.longitude**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Longitude of channel location  | 14.23          |
       |                                              | in datum specified at survey   |                |
       | **Units**: decimal degrees                   | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`measurement_azimuth`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **measurement_azimuth**                      | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Azimuth of channel in the      | 0              |
       |                                              | specified survey.orientation.r |                |
       | **Units**: decimal degrees                   | eference_frame.                |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`measurement_tilt`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **measurement_tilt**                         | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Tilt of channel in survey.orie | 0              |
       |                                              | ntation.reference_frame.       |                |
       | **Units**: decimal degrees                   |                                |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`sample_rate`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **sample_rate**                              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Sample rate of the channel.    | 8              |
       |                                              |                                |                |
       | **Units**: samples per second                |                                |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`time_period.end`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **time_period.end**                          | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | End date and time of           | 2020-02-04 T16:|
       |                                              | collection in UTC.             | 23:45.453670   |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: time                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`time_period.start`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **time_period.start**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Start date and time of         | 2020-02-01 T09:|
       |                                              | collection in UTC.             | 23:45.453670   |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: time                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`transformed_azimuth`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **transformed_azimuth**                      | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Azimuth angle of channel that  | 0              |
       |                                              | has been transformed into a    |                |
       | **Units**: decimal degrees                   | specified coordinate system.   |                |
       |                                              | Note this value is only for    |                |
       | **Type**: Float                              | derivative products from the   |                |
       |                                              | archived data.                 |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`transformed_tilt`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **transformed_tilt**                         | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Tilt angle of channel that has | 0              |
       |                                              | been transformed into a        |                |
       | **Units**: decimal degrees                   | specified coordinate system.   |                |
       |                                              | Note this value is only for    |                |
       | **Type**: Float                              | derivative products from the   |                |
       |                                              | archived data.                 |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`type`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **type**                                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Data type for the channel.     | temperature    |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`units`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **units**                                    | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Units of the data.  Options:   | celsius        |
       |                                              | SI units or counts.            |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

Example Auxiliary XML
---------------------

::

   <auxiliary>
       <comments>great</comments>
       <component>Temperature</component>
       <data_logger>
           <channel_number type="Integer">1</channel_number>
       </data_logger>
       <data_quality>
           <warning>None</warning>
           <rating>
               <author>mt</author>
               <method>ml</method>
               <value type="Integer">4</value>
           </rating>
       </data_quality>
       <fdsn>
           <channel_code>LQN</channel_code>
       <fdsn>
       <filter>
           <name>
               <i>lowpass</i>
               <i>counts2mv</i>
           </name>
           <applied type="boolean">
               <i type="boolean">True</i>
           </applied>
           <comments>test</comments>
       </filter>
       <location>
           <latitude type="Float" units="degrees">12.324</latitude>
           <longitude type="Float" units="degrees">-112.03</longitude>
           <elevation type="Float" units="degrees">1234.0</elevation>
       </location>
       <measurement_azimuth type="Float" units="degrees">0.0</measurement_azimuth>
       <measurement_tilt type="Float" units="degrees">90.0</measurement_tilt>
       <sample_rate type="Float" units="samples per second">8.0</sample_rate>
       <time_period>
           <end>2020-01-01T00:00:00+00:00</end>
           <start>2020-01-04T00:00:00+00:00</start>
       </time_period>
       <type>auxiliary</type>
       <units>celsius</units>
   </auxiliary>
