import numpy as np
import pandas as pd


class FrequencyBand(pd.Interval):
    """
    Has a lower_bound, upper_bound, central_frequency and method for Fourier
    coefficient indices.
    """

    def __init__(self, left, right, closed="left", **kwargs):
        """

        Parameters
        ----------
        left
        right
        closed
        kwargs:
            "average_type": string
             one of ["geometric", "arithmetic"]
             Tells which type of mean to use when computing the band center.
        """
        pd.Interval.__init__(self, left, right, **kwargs)
        self.average_type = kwargs.get("average_type", "geometric")
        self.lower_bound = self.left
        self.upper_bound = self.right

    @property
    def lower_bound(self):
        return self.left

    @property
    def upper_bound(self):
        return self.right

    def lower_closed(self):
        return self.closed_left

    def upper_closed(self):
        return self.closed_right

    def fourier_coefficient_indices(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array
            Intended to represent the one-sided (positive) frequency axis of
            the data that has been FFT-ed

        Returns
        -------
        indices: numpy array of integers
            Integer indices of the fourier coefficients associated with the
            frequecies passed as input argument
        """
        if self.lower_closed:
            cond1 = frequencies >= self.lower_bound
        else:
            cond1 = frequencies > self.lower_bound
        if self.upper_closed:
            cond2 = frequencies <= self.upper_bound
        else:
            cond2 = frequencies < self.upper_bound

        indices = np.where(cond1 & cond2)[0]
        return indices

    def in_band_harmonics(self, frequencies):
        """
        rename to within_band_harmonics?
        Parameters
        ----------
        frequencies: array-like, floating poirt

        Returns: numpy array
            the actual harmonics or frequencies in band, rather than the indices.
        -------

        """
        indices = self.fourier_coefficient_indices(frequencies)
        harmonics = frequencies[indices]
        return harmonics

    @property
    def center_frequency(self):
        """
        Returns
        -------
        center_frequency: float
            The frequency associated with the band center.
        """
        if self.average_type == "geometric":
            return np.sqrt(self.lower_bound * self.upper_bound)
        elif self.average_type == "arithmetic":
            return (self.lower_bound + self.upper_bound)/2
        else:
            raise NotImplementedError

    @property
    def center_period(self):
        return 1.0 / self.center_frequency


class FrequencyBands(object):
    """
    This is just collection of FrequencyBand objects.
    It is intended to be used at a single decimation level

    The core underlying variable is "band_edges", a 2D array, with one row per
    frequency band and two columns, one for the left-hand (lower bound) of the
    frequency band and one for the right-hand (upper bound).

    Note there are some "clever" ways to define the bands using a 1-D array but this
    assumes the bands to be adjacent, and there is no good reason to bake this
    constriant in -- band edges is thus 2-D.
    """

    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
        band_edges: 2d numpy array
        """
        self.band_edges = kwargs.get("band_edges", None)

    @property
    def number_of_bands(self):
        return self.band_edges.shape[0]

    def validate(self):
        """
        placeholder for sanity checks.
        Main reason this is here is in anticipation of supporting an append() method
        to this class that accepts FrequencyBand objects.  In that case we may wish
        to re-order the band edges.


        """
        band_centers = self.band_centers()

        # check band centers are monotonically increasing
        monotone_condition = np.all(band_centers[1:] > band_centers[:-1])
        if monotone_condition:
            pass
        else:
            print(
                "Band Centers are Not Monotonic.  This probably means that "
                "the bands are being defined in an adhoc / on the fly way"
            )
            print("This condition untested 20210720")
            print("Attempting to reorganize bands")
            # use np.argsort to rorganize the bands
            self.band_edges = self.band_edges[np.argsort(band_centers), :]

        # check other conditions?:

        return

    def bands(self, direction="increasing_frequency"):
        """
        make this a generator for iteration over bands
        Returns
        -------

        """
        band_indices = range(self.number_of_bands)
        if direction == "increasing_period":
            band_indices = np.flip(band_indices)
        return (self.band(i_band) for i_band in band_indices)

    def band(self, i_band):
        """
        Parameters
        ----------
        i_band: integer (zero-indexed)
            Specifies the band to return

        Returns
        -------
        frequency_band: FrequencyBand() object
        """
        frequency_band = FrequencyBand(
            self.band_edges[i_band, 0],
            self.band_edges[i_band, 1],
        )

        return frequency_band

    def band_centers(self, frequency_or_period="frequency"):
        """
        Parameters
        ----------
        frequency_or_period : str
            One of ["frequency" , "period"].  Determines if the vector of band
            centers is returned in "Hz" or "s"

        Returns
        -------
        band_centers : numpy array
            center frequencies of the bands in Hz or in s
        """
        band_centers = np.full(self.number_of_bands, np.nan)
        for i_band in range(self.number_of_bands):
            frequency_band = self.band(i_band)
            band_centers[i_band] = frequency_band.center_frequency
        if frequency_or_period == "period":
            band_centers = 1.0 / band_centers
        return band_centers

    def from_decimation_object(self, decimation_object):
        """
        Define band_edges array from config object,

        Parameters
        ----------
        decimation_object: mt_metadata.transfer_functions.processing.aurora.Decimation
        """
        # replace below with decimation_object.delta_frequency ?
        df = (
            decimation_object.decimation.sample_rate
            / decimation_object.window.num_samples
        )
        half_df = df / 2.0
        # half_df /=100
        lower_edges = (decimation_object.lower_bounds * df) - half_df
        upper_edges = (decimation_object.upper_bounds * df) + half_df
        band_edges = np.vstack((lower_edges, upper_edges)).T
        self.band_edges = band_edges


def get_fft_harmonics(samples_per_window, sample_rate):
    """
    Works for odd and even number of points.

    Could be midified with kwargs to support one_sided, two_sided, ignore_dc
    ignore_nyquist, and etc.  Could actally take FrequencyBands as an argument
    if we wanted as well.

    Parameters
    ----------
    samples_per_window: integer
        Number of samples in a window that will be Fourier transformed.
    sample_rate: float
            Inverse of time step between samples,
            Samples per second

    Returns
    -------
    harmonic_frequencies: numpy array
        The frequencies that the fft will be computed.
        These are one-sided (positive frequencies only)
        Does not return Nyquist
        Does return DC component
    """
    n_fft_harmonics = int(samples_per_window / 2)  # no bin at Nyquist,
    delta_t = 1.0 / sample_rate
    harmonic_frequencies = np.fft.fftfreq(samples_per_window, d=delta_t)
    harmonic_frequencies = harmonic_frequencies[0:n_fft_harmonics]
    return harmonic_frequencies


def df_from_bands(band_list):
    """
    Utility function that transforms a list of bands into a dataframe

    Note: The decimation_level here is +1 to agree with EMTF convention.
        Not clear this is really necessary

    Parameters
    ----------
    band_list: list
        obtained from mt_metadata.transfer_functions.processing.aurora.decimation_level.DecimationLevel.bands

    Returns
    -------
    out_df: pd.Dataframe
        Same format as that generated by EMTFBandSetupFile.get_decimation_level()
    """
    df_columns = [
        "decimation_level",
        "lower_bound_index",
        "upper_bound_index",
        "frequency_min",
        "frequency_max",
    ]
    n_rows = len(band_list)
    df_columns_dict = {}
    for col in df_columns:
        df_columns_dict[col] = n_rows * [None]
    for i_band, band in enumerate(band_list):
        df_columns_dict["decimation_level"][i_band] = band.decimation_level + 1
        df_columns_dict["lower_bound_index"][i_band] = band.index_min
        df_columns_dict["upper_bound_index"][i_band] = band.index_max
        df_columns_dict["frequency_min"][i_band] = band.frequency_min
        df_columns_dict["frequency_max"][i_band] = band.frequency_max
    out_df = pd.DataFrame(data=df_columns_dict)
    out_df.sort_values(by="lower_bound_index", inplace=True)
    out_df.reset_index(inplace=True, drop=True)
    return out_df
