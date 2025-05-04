# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:26:52 2021

@author: jpeacock
"""

import unittest

import numpy as np
from mt_metadata.features.coherence import Coherence


class TestCoherence(unittest.TestCase):
    def test_init(self):
        coh = Coherence()

    def test_init_from_dict(self):
        """
            Test that we can create a dictionary with the coherence metadata
            and pass this to a Coherence() mt_metadata object and get the expected values.

        """
        window_type = "hamming"
        window_length = 512
        coh_dict = {
            # "channel_1": "ex",
            # "channel_2": "hy",
            "ch1": "ex",
            "ch2": "hy",
            "detrend" : "linear",
            "window.clock_zero_type": "ignore",
            "window.normalized": True,
            "window.num_samples": 512,
            "window.overlap": 128,
            "window.type": window_type
        }
        coh = Coherence()
        coh.from_dict(meta_dict=coh_dict)
        assert coh.window.type == window_type
        assert coh.window.num_samples == window_length
        assert coh.channel_pair_str == "ex, hy"

    def test_calculate_coherence(self, plot: bool = False):
        """

        Parameters
        ----------
        plot: bool
            Used for debugging tests, makes a sanity check plot of coherence vs frequency

        """
        # TODO: make this use a test fixture that gets the syntehtic data
        np.random.seed(0)
        n_obs = 40000  # same number of points as legacy EMTF synthetic data
        x = np.random.random(n_obs)
        y = np.random.random(n_obs)
        t = np.arange(n_obs)
        frq = 0.2  # Hz of a sine
        sine = np.sin(2 * np.pi * frq * t)
        x += sine
        y += sine
        coh = Coherence()
        coh.from_dict(meta_dict={
            "channel_1":"ex",
            "channel_2":"ey",
        },
        )
        f, coh_values = coh.compute(x, y)
        assert len(f) == (coh.window.num_samples/2) + 1

        if plot:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot(f, coh_values)
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Squared Coherence (Hz)")
            ax.set_title(f"Squared Coherence for random noise with a tone at {frq:.2f}Hz")
            plt.show()
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
