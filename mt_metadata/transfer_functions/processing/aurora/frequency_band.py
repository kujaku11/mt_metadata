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
