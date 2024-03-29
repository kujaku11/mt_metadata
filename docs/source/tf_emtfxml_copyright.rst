.. role:: red
.. role:: blue
.. role:: navy

Copyright
=========


:navy:`selected_publications`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **selected_publications**                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Any publications that use this data           | my paper       |
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

:navy:`release_status`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **release_status**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | the release status of the data                | Unrestricted   |
       |                                              |                                               | release        |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: controlled vocabulary             |                                               |                |
       |                                              |                                               |                |
       | **Default**: Unrestricted Release            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`conditions_of_use`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **conditions_of_use**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Any notes on conditions of use                | Cite data upon |
       |                                              |                                               | usage.         |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**:                                 |                                               |                |
       | All data and metadata for this survey are    |                                               |                |
       | available free of charge and may be copied   |                                               |                |
       | freely, duplicated and further distributed   |                                               |                |
       | provided this data set is cited as the       |                                               |                |
       | reference. While the author(s) strive to     |                                               |                |
       | provide data and metadata of best possible   |                                               |                |
       | quality, neither the author(s) of this data  |                                               |                |
       | set, not IRIS make any claims, promises, or  |                                               |                |
       | guarantees about the accuracy, completeness, |                                               |                |
       | or adequacy of this information, and         |                                               |                |
       | expressly disclaim liability for errors and  |                                               |                |
       | omissions in the contents of this file.      |                                               |                |
       | Guidelines about the quality or limitations  |                                               |                |
       | of the data and metadata, as obtained from   |                                               |                |
       | the author(s), are included for informational|                                               |                |
       | purposes only.                               |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`acknowledgement`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **acknowledgement**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | any acknowledgments the transfer function     | This project   |
       |                                              | should have.                                  | was funded by  |
       | **Units**: None                              |                                               | x.             |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`additional_info`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **additional_info**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | any additional information about the data.    | This purpose of|
       |                                              |                                               | this project is|
       | **Units**: None                              |                                               | ...            |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`citation.title`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.title**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Full title of the citation                    | Paper Title    |
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

:navy:`citation.authors`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.authors**                         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | author names                                  | M.Tee A. Roura |
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

:navy:`citation.year`
~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.year**                            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Year of citation                              | 2020           |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: date                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 1980-01-01T00:00:00+00:00       |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`citation.volume`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.volume**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Journal volume of the citation                | 12             |
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

:navy:`citation.pages`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.pages**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Page numbers of the citation                  | 10-15          |
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

:navy:`citation.journal`
~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.journal**                         | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | Journal title of citation                     | Journal of     |
       |                                              |                                               | Geophysical    |
       | **Units**: None                              |                                               | Research       |
       |                                              |                                               |                |
       | **Type**: string                             |                                               |                |
       |                                              |                                               |                |
       | **Style**: free form                         |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`citation.doi`
~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.doi**                             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | doi number of the citation                    | ###/###        |
       |                                              |                                               |                |
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

:navy:`citation.survey_d_o_i`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **citation.survey_d_o_i**                    | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :blue:`False`                  | doi number of the survey                      | ###/###        |
       |                                              |                                               |                |
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
