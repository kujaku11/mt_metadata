.. role:: red
.. role:: blue
.. role:: navy

Provenance
==========


:navy:`create_time`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **create_time**                              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | date and time the file was created            | 2020-02-08T12:2|
       |                                              |                                               | 3:40.324600+00:|
       | **Units**: None                              |                                               | 00             |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: date time                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: 1980-01-01T00:00:00+00:00       |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`creating_application`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **creating_application**                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | name of the application that created the XML  | EMTF File      |
       |                                              | file                                          | Conversion     |
       | **Units**: None                              |                                               | Utilities 4.0  |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: mt_metadata                     |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`creator.name`
~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **creator.name**                             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | author name                                   | person name    |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`creator.email`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **creator.email**                            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | email of the contact person                   | mt.guru@em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: email                             |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`creator.org`
~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **creator.org**                              | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | organization name                             | mt gurus       |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`creator.org_url`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **creator.org_url**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | URL of organization                           | https://www.mt_|
       |                                              |                                               | gurus.org      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: url                               |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`submitter.name`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **submitter.name**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | author name                                   | person name    |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`submitter.email`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **submitter.email**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | email of the contact person                   | mt.guru@em.org |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: email                             |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`submitter.org`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **submitter.org**                            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | organization name                             | mt gurus       |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`submitter.org_url`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **submitter.org_url**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | URL of organization                           | https://www.mt_|
       |                                              |                                               | gurus.org      |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: url                               |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
