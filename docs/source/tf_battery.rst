.. role:: red
.. role:: blue
.. role:: navy

Battery
=======


:navy:`type`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **type**                                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Description of battery type.                  | pb-acid gel    |
       |                                              |                                               | cell           |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: name                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`id`
~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **id**                                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | battery id                                    | battery01      |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: name                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`voltage.start`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **voltage.start**                            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Starting value of a diagnostic measurement.   | 12.3           |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`voltage.end`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **voltage.end**                              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Ending value of a diagnostic measurement.     | 10             |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: float                              |                                               |                |
       |                                              |                                               |                |
       | **Style**: number                            |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
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
       | **Required**: :blue:`False`                  | Any comments about the battery.               | discharged too |
       |                                              |                                               | quickly        |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: name                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
