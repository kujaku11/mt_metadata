.. role:: red
.. role:: blue
.. role:: navy


Electric Channel
================

.. contents::  :local:

Electric channel refers to a dipole measurement of the electric field
for a single station for a single run.

Electric Channel Attributes
----------------------------

:navy:`ac.end`
~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **ac.end**                                   | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Ending AC value; if more than  |  49.5          |
       |                                              | one measurement input as a     |                |
       | **Units**: volts                             | list of Number [1 2 ...]       |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`ac.start`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **ac.start**                                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Starting AC value; if more     |  55.8          |
       |                                              | than one measurement input as  |                |
       | **Units**: volts                             | a list of Number [1 2 ...]     |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`channel_number`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **channel_number**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Channel number on the data     | 1              |
       |                                              | logger of the recorded         |                |
       | **Units**: None                              | channel.                       |                |
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
       | **Required**: :blue:`False`                  | Any comments about the channel | Lightning storm|
       |                                              | that would be useful to a      | at 6pm local   |
       | **Units**: None                              | user.                          | time           |
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
       | **Required**: :red:`True`                    | Name of the component          | Ex             |
       |                                              | measured.  Options: [ Ex; Ey ] |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`contact_resistance.end`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **contact_resistance.end**                   | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Starting contact resistance;   |  1.8           |
       |                                              | if more than one measurement   |                |
       | **Units**: ohms                              | input as a list [1             |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number list                       |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`contact_resistance.start`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **contact_resistance.start**                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Starting contact resistance;   |  1.4           |
       |                                              | if more than one measurement   |                |
       | **Units**: ohms                              | input as a list [1             |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number list                       |                                |                |
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

:navy:`dc.end`
~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **dc.end**                                   | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Ending DC value; if more than  | 1.5            |
       |                                              | one measurement input as a     |                |
       | **Units**: volts                             | list [1                        |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`dc.start`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **dc.start**                                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Starting DC value; if more     | 1.1            |
       |                                              | than one measurement input as  |                |
       | **Units**: volts                             | a list [1                      |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`dipole_length`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **dipole_length**                            | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Length of the dipole           | 55.25          |
       |                                              |                                |                |
       | **Units**: meters                            |                                |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
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
       | **Required**: :red:`True`                    | Name of filter applied or to   | [gain,         |
       |                                              | be applied. If more than one   |  highpass_e]   |
       | **Units**: None                              | filter input as a list in the  |                |
       |                                              | order in which the should be   |                |
       | **Type**: String                             | applied.                       |                |
       |                                              |                                |                |
       | **Style**: List                              |                                |                |
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
       | **Required**: :red:`True`                    | Azimuth angle of the channel   | 0              |
       |                                              | in the specified survey.orient |                |
       | **Units**: decimal degrees                   | ation.reference_frame.         |                |
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
       | **Required**: :red:`True`                    | Tilt angle of channel in surve | 0              |
       |                                              | y.orientation.reference_frame. |                |
       | **Units**: decimal degrees                   |                                |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.elevation**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Elevation of negative          | 123.4          |
       |                                              | electrode in datum specified   |                |
       | **Units**: meters                            | at survey level.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.id`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.id**                              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Negative electrode ID Number   | electrode01    |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.latitude**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Latitude of negative electrode | 23.134         |
       |                                              | in datum specified at survey   |                |
       | **Units**: decimal degrees                   | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.longitude**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Longitude of negative          | 14.23          |
       |                                              | electrode in datum specified   |                |
       | **Units**: decimal degrees                   | at survey level.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.manufacturer`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.manufacturer**                    | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Person or organization that    | Electro-Dudes  |
       |                                              | manufactured the electrode.    |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.model`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.model**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Model version of the           | falcon5        |
       |                                              | electrode.                     |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`negative.type`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **negative.type**                            | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Type of electrode              | Ag-AgCl        |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.elevation**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Elevation of the positive      | 123.4          |
       |                                              | electrode in datum specified   |                |
       | **Units**: meters                            | at survey level.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.id`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.id**                              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Positive electrode ID Number   | electrode02    |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.latitude**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Latitude of positive electrode | 23.134         |
       |                                              | in datum specified at survey   |                |
       | **Units**: decimal degrees                   | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.longitude**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Longitude of positive          | 14.23          |
       |                                              | electrode in datum specified   |                |
       | **Units**: decimal degrees                   | at survey level.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.manufacturer`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.manufacturer**                    | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Name of group or person that   | Electro-Dudes  |
       |                                              | manufactured the electrode.    |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.model`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.model**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Model version of the           | falcon5        |
       |                                              | electrode.                     |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`positive.type`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **positive.type**                            | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Type of electrode              | Pb-PbCl        |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
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
       |                                              | collection in UTC              | 23:45.453670   |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date Time                         |                                |                |
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
       | **Required**: :red:`True`                    | Start date and time of         | 2020-02-01T    |
       |                                              | collection in UTC.             | 09:23:45.453670|
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date Time                         |                                |                |
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
       | **Required**: :red:`True`                    | Data type for the channel.     | electric       |
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
       | **Required**: :red:`True`                    | Units of the data              | counts         |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

Example Electric Channel JSON
-----------------------------

::

   {
    "electric": {
       "ac.end": 10.2,
       "ac.start": 12.1,
       "channel_number": 2,
       "comments": null,
       "component": "EX",
       "contact_resistance.end": 1.2,
       "contact_resistance.start": 1.1,
       "data_quality.rating.author": "mt",
       "data_quality.rating.method": "ml",
       "data_quality.rating.value": 4,
       "data_quality.warning": null,
       "dc.end": 1.0,
       "dc.start": 2.0,
       "dipole_length": 100.0,
	   "fdsn.channel_code": "LQN",
       "filter.applied": [false],
       "filter.comments": null,
       "filter.name": [ "counts2mv", "lowpass"],
       "measurement_azimuth": 90.0,
       "measurement_tilt": 20.0,
       "negative.elevation": 100.0,
       "negative.id": "a",
       "negative.latitude": 12.12,
       "negative.longitude": -111.12,
       "negative.manufacturer": "test",
       "negative.model": "fats",
       "negative.type": "pb-pbcl",
       "positive.elevation": 101.0,
       "positive.id": "b",
       "positive.latitude": 12.123,
       "positive.longitude": -111.14,
       "positive.manufacturer": "test",
       "positive.model": "fats",
       "positive.type": "ag-agcl",
       "sample_rate": 256.0,
       "time_period.end": "1980-01-01T00:00:00+00:00",
       "time_period.start": "2020-01-01T00:00:00+00:00",
       "type": "electric",
       "units": "counts"
     }
   }
