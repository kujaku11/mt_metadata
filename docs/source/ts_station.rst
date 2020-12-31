.. role:: red
.. role:: blue
.. role:: navy

Station
=======

.. contents::  :local:

A station encompasses a single site where data are collected. If the
location changes during a run, then a new station should be created and
subsequently a new run under the new station. If the sensors, cables,
data logger, battery, etc. are replaced during a run but the station
remains in the same location, then this can be recorded in the ``Run``
metadata but does not require a new station entry.

Station Attributes
-------------------

:navy:`acquired_by.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **acquired_by.author**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of person or group that   | person name    |
       |                                              | collected the station data and |                |
       | **Units**: None                              | will be the point of contact   |                |
       |                                              | if any questions arise about   |                |
       | **Type**: String                             | the data.                      |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`acquired_by.comments`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **acquired_by.comments**                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments about who         | Expert diggers.|
       |                                              | acquired the data.             |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+


:navy:`channel_layout`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **channel_layout**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | How the dipoles and magnetic   | "+"            |
       |                                              | channels of the station were   |                |
       | **Units**: None                              | laid out.  Options: ["L"; "+"] |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`channels_recorded`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **channels_recorded**                        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | List of components recorded by |  T             |
       |                                              | the station. Should be a       |                |
       | **Units**: None                              | summary of all channels        |                |
       |                                              | recorded dropped channels will |                |
       | **Type**: String                             | be recorded in Run.            |                |
       |                                              | Options:                       |                |
       | **Style**: Controlled Vocabulary             | [ Ex;  Ey; Hx; Hy; Hz; T       |                |
       |                                              | Battery; other  ]              |                |
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
       | **Required**: :blue:`False`                  | Any comments on the station    | Pipeline near  |
       |                                              | that would be important for a  | by.            |
       | **Units**: None                              | user.                          |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`data_type`
~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **data_type**                                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | All types of data recorded by  | BBMT           |
       |                                              | the station. If multiple types |                |
       | **Units**: None                              | input as a comma separated     |                |
       |                                              | list. Options -->              |                |
       | **Type**: String                             | [RMT; AMT; BBMT; LPMT]         |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+
	   
:navy:`fdsn.identifier`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **fdsn.identifier**                          | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Station name that is archived  | MT201          |
       |                                              | {a-z;A-Z;0-9.  For IRIS this   |                |
       | **Units**: None                              | is a 5 character String.       |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Alpha Numeric                     |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`geographic_name`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **geographic_name**                          | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Closest geographic name to the | Kelly, YK      |
       |                                              | station, or a location         | or             |
       | **Units**: None                              | description unique to the      | Three Elms     |
       |                                              | station                        |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`id`
~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **id**                                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Station ID name.  This should  | MT001          |
       |                                              | be an alpha numeric name that  |                |
       | **Units**: None                              | is typically 5-6 characters    |                |
       |                                              | long.  Commonly the project    |                |
       | **Type**: String                             | name in 2 or 3 letters and     |                |
       |                                              | the station number.            |                |
       | **Style**: Alpha Numeric                     |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.declination.comments`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.declination.comments**            | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments on declination    | Different than |
       |                                              | that are important to an end   | recorded       |
       | **Units**: None                              | user.                          | declination    |
       |                                              |                                | from data      |
       | **Type**: String                             |                                | logger.        |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.declination.model`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.declination.model**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the geomagnetic        | WMM-2016       |
       |                                              | reference model as             |                |
       | **Units**: None                              | model_name-YYYY.               |                |
       |                                              | Model options ->               |                |
       | **Type**: String                             | [EMAG2; EMM; HDGM; IGRF; WMM]  |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`location.declination.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **location.declination.value**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Declination angle relative to  | 12.3           |
       |                                              | geographic north positive      |                |
       | **Units**: decimal degrees                   | clockwise estimated from       |                |
       |                                              | location and geomagnetic       |                |
       | **Type**: Float                              | model.                         |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
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
       | **Required**: :red:`True`                    | Elevation of station location  | 123.4          |
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
       | **Required**: :red:`True`                    | Latitude of station location   | 23.134         |
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
       | **Required**: :red:`True`                    | Longitude of station location  | 14.23          |
       |                                              | in datum specified at survey   |                |
       | **Units**: decimal degrees                   | level.                         |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`orientation.method`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **orientation.method**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Method for orienting station   | compass        |
       |                                              | channels.  Options:            |                |
       | **Units**: None                              | [compass; GPS; theodolite;     |                |
       |                                              | electric_compass ]             |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`orientation.reference_frame`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **orientation.reference_frame**              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Reference frame for station    | geomagnetic    |
       |                                              | layout.  There are only 2      |                |
       | **Units**: None                              | options geographic and         |                |
       |                                              | geomagnetic.  Both assume a    |                |
       | **Type**: String                             | right-handed coordinate system |                |
       |                                              | with North=0                   |                |
       | **Style**: Controlled Vocabulary             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`orientation.transformed_reference_frame`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **orientation.transformed_reference_frame**  | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Reference frame rotation angel | 10             |
       |                                              | relative to                    |                |
       | **Units**: None                              | orientation.reference_frame    |                |
       |                                              | assuming positive clockwise.   |                |
       | **Type**: Float                              | Should only be used if data    |                |
       |                                              | are rotated.                   |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.comments`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.comments**                      | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments on provenance of  | From a         |
       |                                              | the data.                      | graduated      |
       | **Units**: None                              |                                | graduate       |
       |                                              |                                | student.       |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.creation_time`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.creation_time**                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Date and time the file was     | 2020-02-08 T12:|
       |                                              | created.                       | 23:40.324600   |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date Time                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.log`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.log**                           | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | A history of any changes made  | 2020-02-10     |
       |                                              | to the data.                   | T14:24:45+00:00|
       | **Units**: None                              |                                | updated station|
       |                                              |                                | metadata.      |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.software.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.software.author**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Author of the software used to | programmer 01  |
       |                                              | create the data files.         |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.software.name`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.software.name**                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the software used to   | mtrules        |
       |                                              | create data files              |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.software.version`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.software.version**              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Version of the software used   | 12.01a         |
       |                                              | to create data files           |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.submitter.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.submitter.author**              | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the person submitting  | person name    |
       |                                              | the data to the archive.       |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.submitter.email`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.submitter.email**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Email of the person submitting | mt.guru@em.org |
       |                                              | the data to the archive.       |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Email                             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`provenance.submitter.organization`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **provenance.submitter.organization**        | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the organization that  | MT Gurus       |
       |                                              | is submitting data to the      |                |
       | **Units**: None                              | archive.                       |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
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
       | **Required**: :red:`True`                    | Start date and time of         | 2020-02-01 T09:|
       |                                              | collection in UTC.             | 23:45.453670   |
       | **Units**: None                              |                                | +00:00         |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date Time                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+


Example Station JSON
--------------------

::

   {    "station": {
           "acquired_by": {
               "author": "mt",
               "comments": null},
           "channel_layout": "L",
           "channels_recorded": "Ex, Ey, Bx, By",
           "comments": null,
           "data_type": "MT",
           "geographic_name": "Whitehorse, Yukon",
           "id": "MT012",
           "location": {
               "latitude": 10.0,
               "longitude": -112.98,
               "elevation": 1234.0,
               "declination": {
                   "value": 12.3,
                   "comments": null,
                   "model": "WMM-2016"}},
           "orientation": {
               "method": "compass",
               "reference_frame": "geomagnetic"},
           "provenance": {
               "comments": null,
               "creation_time": "1980-01-01T00:00:00+00:00",
               "log": null,
               "software": {
                   "author": "test",
                   "version": "1.0a",
                   "name": "name"},
               "submitter": {
                   "author": "name",
                   "organization": null,
                   "email": "test@here.org"}},
           "time_period": {
               "end": "1980-01-01T00:00:00+00:00",
               "start": "1982-01-01T16:45:15+00:00"}
            }
   }
