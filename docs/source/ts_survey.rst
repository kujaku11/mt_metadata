.. role:: red
.. role:: blue
.. role:: navy

Survey
======

.. contents::  :local:

A survey describes an entire data set that covers a specific time span
and region. This may include multiple PIs in multiple data collection
episodes but should be confined to a specific experiment or project. The
``Survey`` metadata category describes the general parameters of the
survey.

Survey Attributes
------------------

:navy:`acquired_by.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **acquired_by.author**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the person or persons  | person name    |
       |                                              | who acquired the data.  This   |                |
       | **Units**: None                              | can be different from the      |                |
       |                                              | project lead if a contractor   |                |
       | **Type**: String                             | or different group collected   |                |
       |                                              | the data.                      |                |
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
       | **Required**: :blue:`False`                  | Any comments about aspects of  | Lightning      |
       |                                              | how the data were collected or | strike caused a|
       | **Units**: None                              | any inconsistencies in the     | time skip at 8 |
       |                                              | data.                          | am UTC.        |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`fdsn.network`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **fdsn.network**                             | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Network code given by          | EM             |
       |                                              | PASSCAL/IRIS/FDSN.  This will  |                |
       | **Units**: None                              | be a two character String that |                |
       |                                              | describes who and where the    |                |
       | **Type**: String                             | network operates.              |                |
       |                                              |                                |                |
       | **Style**: Alpha Numeric                     |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`citation_dataset.doi`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------------+
       | **citation_dataset.doi**                     | **Description**                | **Example**          |
       +==============================================+================================+======================+
       | **Required**: :red:`True`                    | The full URL of the doi Number | http://doi.10.adfabe |
       |                                              | provided by the archive that   |                      |
       | **Units**: None                              | describes the raw data         |                      |
       |                                              |                                |                      |
       | **Type**: String                             |                                |                      |
       |                                              |                                |                      |
       | **Style**: URL                               |                                |                      |
       |                                              |                                |                      |
       |                                              |                                |                      |
       +----------------------------------------------+--------------------------------+----------------------+

:navy:`citation_journal.doi`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+-----------------------+
       | **citation_journal.doi**                     | **Description**                | **Example**           |
       +==============================================+================================+=======================+
       | **Required**: :blue:`False`                  | The full URL of the doi Number |  http://doi.10.xbsfs2 |
       |                                              | for a journal article(s) that  |                       |
       | **Units**: None                              | uses these data.  If multiple  |                       |
       |                                              | journal articles use these     |                       |
       | **Type**: String                             | data provide as a comma        |                       |
       |                                              | separated String of urls.      |                       |
       | **Style**: URL                               |                                |                       |
       |                                              |                                |                       |
       +----------------------------------------------+--------------------------------+-----------------------+

:navy:`comments`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **comments**                                 | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :blue:`False`                  | Any comments about the survey  | Solar activity |
       |                                              | that are important for any     | low.           |
       | **Units**: None                              | user to know.                  |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`country`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **country**                                  | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Country or countries that the  |  Canada        |
       |                                              | survey is located in. If       |                |
       | **Units**: None                              | multiple input as comma        |                |
       |                                              | separated names.               |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`datum`
~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **datum**                                    | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | The reference datum for all    | WGS84          |
       |                                              | geographic coordinates         |                |
       | **Units**: None                              | throughout the survey. It is   |                |
       |                                              | up to the user to be sure that |                |
       | **Type**: String                             | all coordinates are projected  |                |
       |                                              | into this datum.  Should be a  |                |
       | **Style**: Controlled Vocabulary             | well-known datum: [ WGS84  ;   |                |
       |                                              | NAD83  ;  OSGB36  ;  GDA94  ;  |                |
       |                                              | ETRS89  ;  PZ-90.11  ]         |                |
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
       | **Required**: :red:`True`                    | Geographic names that          | Southwestern,  |
       |                                              | encompass the survey.  These   | USA            |
       | **Units**: None                              | should be broad geographic     |                |
       |                                              | names.  Further information    |                |
       | **Type**: String                             | can be found at https://w      |                |
       |                                              | ww.usgs.gov/core-science-      |                |
       | **Style**: Free Form                         | systems/ngp/board-on-          |                |
       |                                              | geographic-names               |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`name`
~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **name**                                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Descriptive name of the survey | MT Characteriza|
       |                                              |                                | tion of Yukon  |
       | **Units**: None                              |                                | Terrane        |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`northwest_corner.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **northwest_corner.latitude**                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Latitude of the northwest      | 23.134         |
       |                                              | corner of the survey in the    |                |
       | **Units**: decimal degrees                   | datum specified.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`northwest_corner.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **northwest_corner.longitude**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Longitude of the northwest     | 14.23          |
       |                                              | corner of the survey in the    |                |
       | **Units**: decimal degrees                   | datum specified.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`project`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **project**                                  | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Alphanumeric name for the      | GEOMAG         |
       |                                              | project.  This is different    |                |
       | **Units**: None                              | than the fdsn.identifier in    |                |
       |                                              | that it describes a project    |                |
       | **Type**: String                             | with a common project lead and |                |
       |                                              | source of funding.  There may  |                |
       | **Style**: Free Form                         | be multiple surveys within a   |                |
       |                                              | project. For example if the    |                |
       |                                              | project is to estimate         |                |
       |                                              | geomagnetic hazards that       |                |
       |                                              | project = GEOMAG but the       |                |
       |                                              | fdsn.identifier = YKN20.       |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`project_lead.author`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **project_lead.author**                      | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Name of the project lead.      | Magneto        |
       |                                              | This should be a person who is |                |
       | **Units**: None                              | responsible for the data.      |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`project_lead.email`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **project_lead.email**                       | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Email of the project lead.     | mt.guru@em.org |
       |                                              | This is in case there are any  |                |
       | **Units**: None                              | questions about data.          |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Email                             |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`project_lead.organization`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **project_lead.organization**                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Organization name of the       | MT Gurus       |
       |                                              | project lead.                  |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`release_license`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+---------------------------------------+----------------+
       | **release_license**                          | **Description**                       | **Example**    |
       +==============================================+=======================================+================+
       | **Required**: :red:`True`                    | How the data can be used. The         | CC-0           |
       |                                              | options are based on Creative         |                |
       | **Units**: None                              | Commons licenses.  Options -->        |                |
       |                                              | [CC-0; CC-BY; CC-BY-SA; CC-BY-ND;     |                |
       | **Type**: String                             | CC-BY-NC-SA; CC-BY-NC-ND]             |                |
       |                                              | For details visit,                    |                |
       | **Style**: Controlled Vocabulary             |                                       |                |
       |                                              | https://creativecommons.org/licenses/ |                |
       |                                              |                                       |                |
       +----------------------------------------------+---------------------------------------+----------------+

:navy:`southeast_corner.latitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **southeast_corner.latitude**                | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Latitude of the southeast      | 23.134         |
       |                                              | corner of the survey in the    |                |
       | **Units**: decimal degrees                   | datum specified.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`southeast_corner.longitude`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **southeast_corner.longitude**               | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Longitude of the southeast     | 14.23          |
       |                                              | corner of the survey in the    |                |
       | **Units**: decimal degrees                   | datum specified.               |                |
       |                                              |                                |                |
       | **Type**: Float                              |                                |                |
       |                                              |                                |                |
       | **Style**: Number                            |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`summary`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **summary**                                  | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Summary paragraph of the       | Long project of|
       |                                              | survey including the purpose;  | characterizing |
       | **Units**: None                              | difficulties; data quality;    | mineral        |
       |                                              | summary of outcomes if the     | resources in   |
       | **Type**: String                             | data have been processed and   | Yukon          |
       |                                              | modeled.                       |                |
       | **Style**: Free Form                         |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`time_period.end_date`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **time_period.end_date**                     | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | End date of the survey in UTC. | 2020-02-01     |
       |                                              |                                |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

:navy:`time_period.start_date`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 30 45 15

       +----------------------------------------------+--------------------------------+----------------+
       | **time_period.start_date**                   | **Description**                | **Example**    |
       +==============================================+================================+================+
       | **Required**: :red:`True`                    | Start date of the survey in    | 1995-06-21     |
       |                                              | UTC.                           |                |
       | **Units**: None                              |                                |                |
       |                                              |                                |                |
       | **Type**: String                             |                                |                |
       |                                              |                                |                |
       | **Style**: Date                              |                                |                |
       |                                              |                                |                |
       |                                              |                                |                |
       +----------------------------------------------+--------------------------------+----------------+

	
	
Example Survey XML Element
--------------------------

::

   <?xml version="1.0" ?>
   <survey>
       <acquired_by>
           <author>MT Graduate Students</author>
           <comments>Multiple over 5 years</comments>
       </acquired_by>
       <fdsn>
           <identifier>SAM1990</identifier>
           <network>EM</network>
       </fdsn> 
       <citation_dataset>
           <doi>https://doi.###</doi>
       </citation_dataset>
       <citation_journal>
           <doi>https://doi.###</doi>
       </citation_journal>
       <comments>None</comments>
       <country>USA, Canada</country>
       <datum>WGS84</datum>
       <geographic_name>Yukon</geographic_name>
       <name>Imaging Gold Deposits of the Yukon Province</name>
       <northwest_corner>
           <latitude type="Float" units="decimal degrees">-130</latitude>
           <longitude type="Float" units="decimal degrees">75.9</longitude>
       </northwest_corner>
       <project>AURORA</project>
       <project_lead>
           <Email>m.tee@mt.org</Email>
           <organization>EM Ltd.</organization>
           <author>M. Tee</author>
       </project_lead>
       <release_license>CC0</release_license>
       <southeast_corner>
           <latitude type="Float" units="decimal degrees">-110.0</latitude>
           <longitude type="Float" units="decimal degrees">65.12</longitude>
       </southeast_corner>
       <summary>This survey spanned multiple years with graduate students
                collecting the data.  Lots of curious bears and moose,
                some interesting signal from the aurora.  Modeled data
                image large scale crustal features like the 
                "fingers of god" that suggest large mineral deposits.
       </summary>
       <time_period>
           <end_date>2020-01-01</end_date>
           <start_date>1995-01-01</start_date>
       </time_period>
   </survey>