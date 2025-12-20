# ==============================================================================
# Imports
# ==============================================================================
from typing import Annotated

import numpy as np
import scipy.signal as ssig
from pydantic import Field, model_validator

from mt_metadata.features.coherence import Coherence
from mt_metadata.processing.window import Window


# from pathos.multiprocessing import ProcessingPool as Pool


# ==============================================================================


class StridingWindowCoherence(Coherence):
    """
    Computes coherence for each sub-window (FFT window) across the time series.
    Returns a 2D array: (window index, frequency).
    """

    subwindow: Annotated[
        Window,
        Field(
            default_factory=Window,  # type: ignore
            description="The window used for the subwindow coherence calculation.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["hann", "hamming", "blackman"],
            },
        ),
    ]

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data: dict) -> dict:
        data["name"] = "striding_window_coherence"
        data["domain"] = "frequency"
        data["description"] = (
            "Computes coherence for each sub-window "
            "(FFT window) across the time series."
        )

        return data

    def set_subwindow_from_window(self, fraction=0.2):
        """
        Set the subwindow as a fraction of the main window.
        """
        self.subwindow = Window()  # type: ignore
        self.subwindow.type = self.window.type
        self.subwindow.num_samples = int(self.window.num_samples * fraction)
        self.subwindow.overlap = int(self.subwindow.num_samples // 2)
        self.subwindow.additional_args = self.window.additional_args
        # No need to update stride; main window stride is set by self.window.num_samples_advance

    def compute(
        self, ts_1: np.ndarray, ts_2: np.ndarray, parallel: bool = False
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        For each main window (length self.window.num_samples, stride self.window.num_samples_advance),
        compute coherence using the subwindow parameters (self.subwindow) within that main window.
        Returns:
            frequencies: 1D array of frequencies
            coherences: 2D array (n_main_windows, n_frequencies)
        """
        n = len(ts_1)
        main_win_len = self.window.num_samples
        main_stride = (
            self.window.num_samples_advance
            if hasattr(self.window, "num_samples_advance")
            else main_win_len
        )
        results = []

        if self.subwindow.type in [
            "kaiser",
            "kaiser_bessel_derived",
            "gaussian",
            "general_cosine",
            "general_gaussian",
            "general_hamming",
            "dpss",
            "chebwin",
        ]:
            win_tuple = tuple(
                [self.subwindow.type]
                + [param for param in self.subwindow.additional_args.values()]
            )

        else:
            win_tuple = self.subwindow.type

        ts_1 = np.nan_to_num(ts_1)
        ts_2 = np.nan_to_num(ts_2)

        starts = range(0, n - main_win_len + 1, main_stride)
        # if parallel:

        #     def process_segment(start):
        #         f, coh = ssig.coherence(
        #             ts_1[start : start + main_win_len],
        #             ts_2[start : start + main_win_len],
        #             window=win_tuple,
        #             nperseg=self.subwindow.num_samples,
        #             noverlap=self.subwindow.overlap,
        #             detrend=self.detrend,
        #         )
        #         return f, coh

        #     with Pool() as pool:
        #         results = pool.map(process_segment, starts)

        #     f = results[0][0]
        #     coherences = [r[1] for r in results]

        # else:
        coherences = []
        for start in starts:
            end = start + main_win_len
            seg1 = ts_1[start:end]
            seg2 = ts_2[start:end]

            f, coh = ssig.coherence(
                seg1,
                seg2,
                window=win_tuple,
                nperseg=self.subwindow.num_samples,
                noverlap=self.subwindow.overlap,
                detrend=self.detrend,
            )
            coherences.append(coh)

        return f, np.array(coherences)
