.. role:: red
.. role:: blue
.. role:: navy

SiteLayout
==========


:navy:`input_channels`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **input_channels**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | list of input channels for transfer function  | [Magnetic(hx), |
       |                                              | estimation                                    | Magnetic(hy)]  |
       | **Type**: list[mt_metadata.transfer_functions|                                               |                |
       | .io.emtfxml.metadata.electric.Elect          |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`output_channels`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **output_channels**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | list of output channels for transfer function | [Electric(ex), |
       |                                              | estimation                                    | Electric(ey),  |
       | **Type**: list[mt_metadata.transfer_functions|                                               | Magnetic(hz)]  |
       | .io.emtfxml.metadata.electric.Elect          |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
