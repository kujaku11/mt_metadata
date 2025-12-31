.. role:: red
.. role:: blue
.. role:: navy

Orientation
===========


:navy:`method`
~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **method**                                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | method for orienting station layout           | compass        |
       |                                              |                                               |                |
       | **Type**: <enum 'OrientationMethodEnum'>     |                                               |                |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`reference_frame`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **reference_frame**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Reference frame for station layout.  There    | geomagnetic    |
       |                                              | are only 2 options geographic and             |                |
       | **Type**: <enum                              | geomagnetic.  Both assume a right-handed      |                |
       | 'GeographicReferenceFrameEnum'>              | coordinate system with North=0 E=90 and       |                |
       | **Units**: None                              | vertical positive downward                    |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`angle_to_geographic_north`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **angle_to_geographic_north**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Angle to rotate the data to align with        | geomagnetic    |
       |                                              | geographic north. If this number is 0 then it |                |
       | **Type**: float | None                       | is assumed the data are aligned with          |                |
       |                                              | geographic north in a right handed coordinate |                |
       | **Units**: degrees                           | system.                                       |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`value`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **value**                                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Channel orientation relative to each other    | orthogonal     |
       |                                              |                                               |                |
       | **Type**: mt_metadata.common.enumerations.Cha|                                               |                |
       | nnelOrientationEnum | None                   |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
