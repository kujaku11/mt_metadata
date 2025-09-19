.. role:: red
.. role:: blue
.. role:: navy

ChannelWeightSpec
=================


:navy:`combination_style`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **combination_style**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | How to combine multiple feature weights.      | multiplication |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'CombinationStyleEnum'>      |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: multiplication                  |                                               |                |
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
       | **Required**: :red:`True`                    | list of tf ouput channels for which this      | [ ex ey hz ]   |
       |                                              | weighting scheme will be applied              |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[str]                          |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: list                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`feature_weight_specs`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **feature_weight_specs**                     | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | List of feature weighting schemes to use for  | []             |
       |                                              | TF processing.                                |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[mt_metadata.features.weights.f|                                               |                |
       | eature_weight_spec.FeatureWeightSpe          |                                               |                |
       | c]                                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: list                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`weights`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **weights**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Weights computed for this channel weight      | null           |
       |                                              | spec. Should be set after evaluation.         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: xarray.core.dataarray.DataArray |  |                                               |                |
       | xarray.core.dataset.Dataset |                |                                               |                |
       | numpy.ndarray | None                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: None                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
