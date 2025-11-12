.. role:: red
.. role:: blue
.. role:: navy

Orientation
===========


:navy:`angle_to_geographic_north`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **angle_to_geographic_north**                | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Angle to geographic north of the station      | 0              |
       |                                              | orientation                                   |                |
       | **Units**: degrees                           |                                               |                |
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

:navy:`layout`
~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **layout**                                   | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Orientation of channels relative to each      | orthogonal     |
       |                                              | other                                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'ChannelOrientationEnum'>    |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**:                                 |                                               |                |
       | ChannelOrientationEnum.orthogonal            |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
