.. role:: red
.. role:: blue
.. role:: navy

Survey
======


:navy:`id`
~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **id**                                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Alpha numeric ID that will be unique for      | EMT20          |
       |                                              | archiving.                                    |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
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

:navy:`datum`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **datum**                                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Datum of latitude and longitude coordinates.  | WGS 84         |
       |                                              | Should be a well-known datum, such as WGS84,  |                |
       | **Units**: None                              | and will be the reference datum for all       |                |
       |                                              | locations.  This is important for the user,   |                |
       | **Type**: str | int                          | they need to make sure all coordinates in the |                |
       |                                              | survey and child items (i.e. stations,        |                |
       |                                              | channels) are referenced to this datum.       |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: WGS 84                          |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`geographic_name`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **geographic_name**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Closest geographic reference to survey,       | Yukon          |
       |                                              | usually a city but could be a landmark or     |                |
       | **Units**: None                              | some other common geographic reference point. |                |
       |                                              |                                               |                |
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

:navy:`name`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **name**                                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Descriptive name of the survey.               | MT Characteriza|
       |                                              |                                               | tion of Yukon  |
       | **Units**: None                              |                                               | Terrane        |
       |                                              |                                               |                |
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

:navy:`project`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Alpha numeric name for the project e.g USGS-  | YUTOO          |
       |                                              | GEOMAG.                                       |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
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

:navy:`stations`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **stations**                                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | List of stations recorded in the survey.      | ListDict[Statio|
       |                                              |                                               | n(id=id)]      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: mt_metadata.common.list_dict.ListDi|                                               |                |
       | ct | list | dict |                           |                                               |                |
       | collections.OrderedDict | tuple              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: ListDict                        |                                               |                |
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
       | **Required**: :blue:`False`                  | List of filters for channel responses.        | ListDict[Filter|
       |                                              |                                               | ()]            |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: mt_metadata.common.list_dict.ListDi|                                               |                |
       | ct | list | dict |                           |                                               |                |
       | collections.OrderedDict | tuple              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: ListDict                        |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`summary`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **summary**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Summary paragraph of survey including the     | long project of|
       |                                              | purpose; difficulties; data quality; summary  | characterizing |
       | **Units**: None                              | of outcomes if the data have been processed   | mineral        |
       |                                              | and modeled.                                  | resources in   |
       | **Type**: <class 'str'>                      |                                               | Yukon          |
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

:navy:`time_period.end_date`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.end_date**                     | **Description**                               | **Example**    |
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

:navy:`time_period.start_date`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.start_date**                   | **Description**                               | **Example**    |
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

:navy:`acquired_by.organization`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.organization**                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Organization full name                        | mt gurus       |
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

:navy:`acquired_by.email`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.email**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Email of the contact person                   | mt.guru@em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.EmailStr | None  |                                               |                |
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

:navy:`acquired_by.url`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.url**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | URL of the contact person                     | https://em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.AnyUrl | None |  |                                               |                |
       | str                                          |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`acquired_by.comments.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.comments.author**              | **Description**                               | **Example**    |
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

:navy:`acquired_by.comments.time_stamp`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.comments.time_stamp**          | **Description**                               | **Example**    |
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

:navy:`acquired_by.comments.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.comments.value**               | **Description**                               | **Example**    |
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

:navy:`acquired_by.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acquired_by.author**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Persons name, should be full first and last   | person name    |
       |                                              | name.                                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
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

:navy:`funding_source.name`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.name**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Persons name, should be full first and last   | person name    |
       |                                              | name.                                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str] | str | None             |                                               |                |
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

:navy:`funding_source.organization`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.organization**              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Organization full name                        | mt gurus       |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str] | str | None             |                                               |                |
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

:navy:`funding_source.email`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.email**                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Email of the contact person                   | mt.guru@em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[pydantic.networks.EmailStr] | |                                               |                |
       | pydantic.networks.EmailStr | None            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`funding_source.url`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.url**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | URL of the contact person                     | em.org         |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[pydantic.networks.AnyHttpUrl] |                                               |                |
       | | pydantic.networks.AnyHttpUrl |             |                                               |                |
       | None                                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`funding_source.comments.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.comments.author**           | **Description**                               | **Example**    |
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

:navy:`funding_source.comments.time_stamp`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.comments.time_stamp**       | **Description**                               | **Example**    |
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

:navy:`funding_source.comments.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.comments.value**            | **Description**                               | **Example**    |
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

:navy:`funding_source.grant_id`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **funding_source.grant_id**                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Grant ID number or name                       | MT-01-2020     |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str] | str | None             |                                               |                |
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

:navy:`citation_dataset.doi`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.doi**                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | full url of the doi number                    | http://doi.### |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.HttpUrl | str |  |                                               |                |
       | None                                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`citation_dataset.authors`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.authors**                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | author names                                  | M.Tee A. Roura |
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

:navy:`citation_dataset.title`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.title**                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Full title of the citation                    | Paper Title    |
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

:navy:`citation_dataset.year`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.year**                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Year of citation                              | 2020           |
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

:navy:`citation_dataset.volume`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.volume**                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Journal volume of the citation                | 12             |
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

:navy:`citation_dataset.pages`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.pages**                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Page numbers of the citation                  | 10-15          |
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

:navy:`citation_dataset.journal`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_dataset.journal**                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Journal title of citation                     | Journal of     |
       |                                              |                                               | Geophysical    |
       | **Units**: None                              |                                               | Research       |
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

:navy:`citation_journal.doi`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.doi**                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | full url of the doi number                    | http://doi.### |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.HttpUrl | str |  |                                               |                |
       | None                                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`citation_journal.authors`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.authors**                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | author names                                  | M.Tee A. Roura |
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

:navy:`citation_journal.title`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.title**                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Full title of the citation                    | Paper Title    |
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

:navy:`citation_journal.year`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.year**                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Year of citation                              | 2020           |
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

:navy:`citation_journal.volume`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.volume**                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Journal volume of the citation                | 12             |
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

:navy:`citation_journal.pages`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.pages**                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Page numbers of the citation                  | 10-15          |
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

:navy:`citation_journal.journal`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation_journal.journal**                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Journal title of citation                     | Journal of     |
       |                                              |                                               | Geophysical    |
       | **Units**: None                              |                                               | Research       |
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

:navy:`northwest_corner.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **northwest_corner.latitude**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Latitude of the location.                     | 12.324         |
       |                                              |                                               |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
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

:navy:`northwest_corner.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **northwest_corner.longitude**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Longitude of the location.                    | 12.324         |
       |                                              |                                               |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
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

:navy:`northwest_corner.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **northwest_corner.elevation**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Elevation of the location.                    | 1234.0         |
       |                                              |                                               |                |
       | **Units**: meters                            |                                               |                |
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

:navy:`southeast_corner.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **southeast_corner.latitude**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Latitude of the location.                     | 12.324         |
       |                                              |                                               |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
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

:navy:`southeast_corner.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **southeast_corner.longitude**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Longitude of the location.                    | 12.324         |
       |                                              |                                               |                |
       | **Units**: degrees                           |                                               |                |
       |                                              |                                               |                |
       | **Type**: float | None                       |                                               |                |
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

:navy:`southeast_corner.elevation`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **southeast_corner.elevation**               | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Elevation of the location.                    | 1234.0         |
       |                                              |                                               |                |
       | **Units**: meters                            |                                               |                |
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

:navy:`country`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **country**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Country where the survey was conducted.       | Canada         |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str] | str | None             |                                               |                |
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

:navy:`state`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **state**                                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | State or province where the survey was        | Yukon          |
       |                                              | conducted.                                    |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str] | str | None             |                                               |                |
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

:navy:`project_lead.organization`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.organization**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Organization full name                        | mt gurus       |
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

:navy:`project_lead.email`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.email**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Email of the contact person                   | mt.guru@em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.EmailStr | None  |                                               |                |
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

:navy:`project_lead.url`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.url**                         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | URL of the contact person                     | https://em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: pydantic.networks.AnyUrl | None |  |                                               |                |
       | str                                          |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`project_lead.comments.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.comments.author**             | **Description**                               | **Example**    |
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

:navy:`project_lead.comments.time_stamp`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.comments.time_stamp**         | **Description**                               | **Example**    |
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

:navy:`project_lead.comments.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.comments.value**              | **Description**                               | **Example**    |
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

:navy:`project_lead.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **project_lead.author**                      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Persons name, should be full first and last   | person name    |
       |                                              | name.                                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: str | None                         |                                               |                |
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

:navy:`release_license`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **release_license**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Release license for the data.                 | CC-BY-4.0      |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'str'>                      |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: CC-BY-4.0                       |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
