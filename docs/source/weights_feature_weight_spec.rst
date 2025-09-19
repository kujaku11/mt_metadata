.. role:: red
.. role:: blue
.. role:: navy

FeatureWeightSpec
=================


:navy:`feature_name`
~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **feature_name**                             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | The name of the feature to evaluate (e.g.,    | coherence      |
       |                                              | coherence, impedance_ratio).                  |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'FeatureNameEnum'>           |                                               |                |
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

:navy:`feature`
~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **feature**                                  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | The feature specification.                    | {'type':       |
       |                                              |                                               | 'coherence'}   |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: dict | mt_metadata.features.feature|                                               |                |
       | .Feature | mt_metadata.features.coh          |                                               |                |
       | erence.Coherence | mt_metadata.feat          |                                               |                |
       | ures.fc_coherence.FCCoherence                |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: Feature                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`weight_kernels`
~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **weight_kernels**                           | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | List of weight kernel specification.          | {'type':       |
       |                                              |                                               | 'monotonic'}   |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: list[mt_metadata.features.weights.m|                                               |                |
       | onotonic_weight_kernel.MonotonicWei          |                                               |                |
       | ghtKernel | mt_metadata.features.we          |                                               |                |
       | ights.taper_monotonic_weight_kernel          |                                               |                |
       | .TaperMonotonicWeightKernel | mt_me          |                                               |                |
       | tadata.features.weights.activation_          |                                               |                |
       |                                              |                                               |                |
       | **Default**: list                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+
