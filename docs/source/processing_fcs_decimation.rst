.. role:: red
.. role:: blue
.. role:: navy

Decimation
==========


:navy:`id`
~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **id**                                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Decimation level ID                           | 1              |
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
       | **Default**: ""                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`channels_estimated`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **channels_estimated**                       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | list of channels                              | [ex, hy]       |
       |                                              |                                               |                |
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

:navy:`time_period.end`
~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.end**                          | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | End date and time of collection in UTC.       | 2020-02-       |
       |                                              |                                               | 04T16:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_period.start`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_period.start**                        | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Start date and time of collection in UTC.     | 2020-02-       |
       |                                              |                                               | 01T09:23:45.453|
       | **Units**: None                              |                                               | 670+00:00      |
       |                                              |                                               |                |
       | **Type**: float | int | numpy.datetime64 | pa|                                               |                |
       | ndas._libs.tslibs.timestamps.Timest          |                                               |                |
       | amp | str |                                  |                                               |                |
       | mt_metadata.common.mttime.MTime              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MTime                           |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`channels`
~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **channels**                                 | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | List of channels                              | [ex, hy]       |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'mt_metadata.common.list_dic|                                               |                |
       | t.ListDict'>                                 |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: ListDict                        |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_series_decimation.level`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_series_decimation.level**             | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Decimation level, must be a non-negative      | 0              |
       |                                              | integer starting at 0                         |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: int | None                         |                                               |                |
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

:navy:`time_series_decimation.factor`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_series_decimation.factor**            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Decimation factor between parent sample rate  | 4.0            |
       |                                              | and decimated time series sample rate.        |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'float'>                    |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 1.0                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_series_decimation.method`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_series_decimation.method**            | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Type of decimation                            | default        |
       |                                              |                                               |                |
       | **Units**:                                   |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'MethodEnum'>                |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MethodEnum.default              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_series_decimation.sample_rate`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_series_decimation.sample_rate**       | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Sample rate of the decimation level data      | 256            |
       |                                              | (after decimation).                           |                |
       | **Units**: samples per second                |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'float'>                    |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: 1.0                             |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`time_series_decimation.anti_alias_filter`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **time_series_decimation.anti_alias_filter** | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Type of anti alias filter for decimation.     | default        |
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
       | **Default**: default                         |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.harmonic_indices`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 51 45 15

       +----------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.harmonic_indices**  | **Description**                               | **Example**    |
       +====================================================+===============================================+================+
       | **Required**: :red:`True`                          | List of harmonics indices kept, if all use -1 | [0, 4, 8]      |
       |                                                    |                                               |                |
       | **Units**: None                                    |                                               |                |
       |                                                    |                                               |                |
       | **Type**: typing.Union[int, list[int], NoneType]   |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       | **Default**: None                                  |                                               |                |
       |                                                    |                                               |                |
       |                                                    |                                               |                |
       +----------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.method`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.method**      | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Fourier transform method                      | fft            |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'MethodEnum'>                |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: MethodEnum.fft                  |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.min_num_stft_windows`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 55 45 15

       +--------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.min_num_stft_windows**  | **Description**                               | **Example**    |
       +========================================================+===============================================+================+
       | **Required**: :red:`True`                              | How many FFT windows must be available for    | 4              |
       |                                                        | the time series to valid for STFT.            |                |
       | **Units**: None                                        |                                               |                |
       |                                                        |                                               |                |
       | **Type**: <class 'int'>                                |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       | **Default**: 0                                         |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       +--------------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.per_window_detrend_type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 58 45 15

       +-----------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.per_window_detrend_type**  | **Description**                               | **Example**    |
       +===========================================================+===============================================+================+
       | **Required**: :red:`True`                                 | Additional detrending applied per window.     | linear         |
       |                                                           | Not available for standard scipy spectrogram  |                |
       | **Units**: None                                           | -- placholder for ARMA prewhitening.          |                |
       |                                                           |                                               |                |
       | **Type**: <enum 'PerWindowDetrendTypeEnum'>               |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       | **Default**: PerWindowDetrendTypeEnum.null                |                                               |                |
       |                                                           |                                               |                |
       |                                                           |                                               |                |
       +-----------------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.pre_fft_detrend_type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 55 45 15

       +--------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.pre_fft_detrend_type**  | **Description**                               | **Example**    |
       +========================================================+===============================================+================+
       | **Required**: :red:`True`                              | Pre FFT detrend method to be applied          | linear         |
       |                                                        |                                               |                |
       | **Units**: None                                        |                                               |                |
       |                                                        |                                               |                |
       | **Type**: <enum 'PreFftDetrendTypeEnum'>               |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       | **Default**: PreFftDetrendTypeEnum.linear              |                                               |                |
       |                                                        |                                               |                |
       |                                                        |                                               |                |
       +--------------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.prewhitening_type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 52 45 15

       +-----------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.prewhitening_type**  | **Description**                               | **Example**    |
       +=====================================================+===============================================+================+
       | **Required**: :red:`True`                           | Prewhitening method to be applied             | first          |
       |                                                     |                                               | difference     |
       | **Units**: None                                     |                                               |                |
       |                                                     |                                               |                |
       | **Type**: <enum 'PrewhiteningTypeEnum'>             |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       | **Default**: PrewhiteningTypeEnum.first_difference  |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       +-----------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.recoloring`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.recoloring**  | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | Whether the data are recolored [True] or not  | True           |
       |                                              | [False].                                      |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <class 'bool'>                     |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: True                            |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.num_samples`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 53 45 15

       +------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.num_samples**  | **Description**                               | **Example**    |
       +======================================================+===============================================+================+
       | **Required**: :red:`True`                            | Number of samples in a single window          | 256            |
       |                                                      |                                               |                |
       | **Units**: samples                                   |                                               |                |
       |                                                      |                                               |                |
       | **Type**: <class 'int'>                              |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       | **Default**: 256                                     |                                               |                |
       |                                                      |                                               |                |
       |                                                      |                                               |                |
       +------------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.overlap`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 49 45 15

       +--------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.overlap**  | **Description**                               | **Example**    |
       +==================================================+===============================================+================+
       | **Required**: :red:`True`                        | Number of samples overlapped by adjacent      | 32             |
       |                                                  | windows                                       |                |
       | **Units**: samples                               |                                               |                |
       |                                                  |                                               |                |
       | **Type**: <class 'int'>                          |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       | **Default**: 32                                  |                                               |                |
       |                                                  |                                               |                |
       |                                                  |                                               |                |
       +--------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 45 45 15

       +----------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.type** | **Description**                               | **Example**    |
       +==============================================+===============================================+================+
       | **Required**: :red:`True`                    | name of the window type                       | hamming        |
       |                                              |                                               |                |
       | **Units**: None                              |                                               |                |
       |                                              |                                               |                |
       | **Type**: <enum 'TypeEnum'>                  |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       | **Default**: TypeEnum.boxcar                 |                                               |                |
       |                                              |                                               |                |
       |                                              |                                               |                |
       +----------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.clock_zero_type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 57 45 15

       +----------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.clock_zero_type**  | **Description**                               | **Example**    |
       +==========================================================+===============================================+================+
       | **Required**: :red:`True`                                | how the clock-zero is specified               | user specified |
       |                                                          |                                               |                |
       | **Units**: None                                          |                                               |                |
       |                                                          |                                               |                |
       | **Type**: <enum 'ClockZeroTypeEnum'>                     |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       | **Default**: ClockZeroTypeEnum.ignore                    |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       +----------------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.clock_zero`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 52 45 15

       +-----------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.clock_zero**  | **Description**                               | **Example**    |
       +=====================================================+===============================================+================+
       | **Required**: :red:`True`                           | Start date and time of the first data window  | 2020-02-       |
       |                                                     |                                               | 01T09:23:45.453|
       | **Units**: None                                     |                                               | 670+00:00      |
       |                                                     |                                               |                |
       | **Type**: mt_metadata.common.mttime.MTime | str |   |                                               |                |
       | float | int | numpy.datetime64 |                    |                                               |                |
       | pandas._libs.tslibs.timestamps.Timestamp |          |                                               |                |
       | None                                                |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       | **Default**: MTime                                  |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       +-----------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.normalized`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 52 45 15

       +-----------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.normalized**  | **Description**                               | **Example**    |
       +=====================================================+===============================================+================+
       | **Required**: :red:`True`                           | True if the window shall be normalized so the | False          |
       |                                                     | sum of the coefficients is 1                  |                |
       | **Units**: None                                     |                                               |                |
       |                                                     |                                               |                |
       | **Type**: <class 'bool'>                            |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       | **Default**: True                                   |                                               |                |
       |                                                     |                                               |                |
       |                                                     |                                               |                |
       +-----------------------------------------------------+-----------------------------------------------+----------------+

:navy:`short_time_fourier_transform.window.additional_args`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. container::

   .. table::
       :class: tight-table
       :widths: 57 45 15

       +----------------------------------------------------------+-----------------------------------------------+----------------+
       | **short_time_fourier_transform.window.additional_args**  | **Description**                               | **Example**    |
       +==========================================================+===============================================+================+
       | **Required**: :red:`True`                                | Additional arguments for the window function  | {'param':      |
       |                                                          |                                               | 'value'}       |
       | **Units**: None                                          |                                               |                |
       |                                                          |                                               |                |
       | **Type**: <class 'dict'>                                 |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       | **Default**: dict                                        |                                               |                |
       |                                                          |                                               |                |
       |                                                          |                                               |                |
       +----------------------------------------------------------+-----------------------------------------------+----------------+
