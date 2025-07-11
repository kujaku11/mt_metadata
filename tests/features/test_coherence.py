# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:26:52 2021

@author: jpeacock
"""
import copy
import numpy as np
import unittest

from mt_metadata.features.coherence import Coherence


class TestCoherence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        """
        Set up the test class, this is run once for the entire test class.
        """
        # This is where you would set up any resources needed for the tests
        # For example, you could create a Coherence instance here if needed
        cls.coh = Coherence()
        cls.coh_dict = {
            "ch1": "ex",
            "ch2": "hy",
            "detrend" : "linear",
            "window.clock_zero_type": "ignore",
            "window.normalized": True,
            "window.num_samples": 512,
            "window.overlap": 128,
            "window.type": "hamming"
        }
        
    def test_init(self):
        coh = Coherence()

    def test_init_from_dict(self):
        """
            Test that we can create a dictionary with the coherence metadata
            and pass this to a Coherence() mt_metadata object and get the expected values.

        """
        window_type = "hamming"
        window_length = 512
        coh_dict = copy.deepcopy(self.coh_dict)
        coh_dict["window.type"] = window_type
        coh_dict["window.num_samples"] = window_length
        # Use 'feature_id' for dispatch, 'name' for instance label
        test_dict = {"feature_id": "coherence", "name": "test_coh", "ch1": "ex", "ch2": "hy"}
        test_dict.update(coh_dict)
        from mt_metadata.features.feature import Feature
        coh = Feature.from_feature_id(test_dict)
        assert coh.window.type == window_type
        assert coh.window.num_samples == window_length
        assert coh.channel_pair_str == "ex, hy"
        print(coh.station1, coh.station2)
	    # Provide dummy arrays for compute
        x = np.random.randn(1024)
        y = np.random.randn(1024)
        f, coh_values = coh.compute(x, y)
        assert len(f) == (coh.window.num_samples/2) + 1

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

    def test_validate_station_ids(self):
        # Case 1: Both stations provided, ch1/ch2 are local
        coh = Coherence()
        coh.ch1 = "ex"
        coh.ch2 = "hy"
        coh.station1 = None
        coh.station2 = None
        coh.validate_station_ids("staA", "staB")
        assert coh.station1 == "staA"
        assert coh.station2 == "staA"

        # Case 2: ch1 is remote, ch2 is local
        coh = Coherence()
        coh.ch1 = "rx"
        coh.ch2 = "ey"
        coh.station1 = None
        coh.station2 = None
        coh.validate_station_ids("staA", "staB")
        assert coh.station1 == "staB"
        assert coh.station2 == "staA"

        # Case 3: station1/station2 set to wrong value, should be reset to None and reassigned
        coh = Coherence()
        coh.ch1 = "ex"
        coh.ch2 = "hy"
        coh.station1 = "wrong"
        coh.station2 = "wrong"
        coh.validate_station_ids("staA", "staB")
        assert coh.station1 == "staA"
        assert coh.station2 == "staA"

        # Case 4: Only local station provided
        coh = Coherence()
        coh.ch1 = "ex"
        coh.ch2 = "hy"
        coh.station1 = None
        coh.station2 = None
        coh.validate_station_ids("staA")
        assert coh.station1 == "staA"
        assert coh.station2 == "staA"

        # Case 5: ch2 is remote, ch1 is local
        coh = Coherence()
        coh.ch1 = "ex"
        coh.ch2 = "ry"
        coh.station1 = None
        coh.station2 = None
        coh.validate_station_ids("staA", "staB")
        assert coh.station1 == "staA"
        assert coh.station2 == "staB"

    def test_striding_window_coherence(self):
        """
        Test StridingWindowCoherence computes a 2D array of coherence values (window x frequency).
        Optionally, plot the result as a pcolor plot for visual inspection.
        """
        from mt_metadata.features.coherence import StridingWindowCoherence

        np.random.seed(42)
        n_obs = 4096
        x = np.random.randn(n_obs)
        y = np.random.randn(n_obs)
        # Add a strong common sine wave to both
        t = np.arange(n_obs)
        sine = 10 * np.sin(2 * np.pi * 0.1 * t)  # Increase amplitude for higher SNR
        x += sine
        y += sine

        swc = StridingWindowCoherence()
        swc.window.num_samples = 1024
        swc.set_subwindow_from_window(fraction=0.25)  # subwindow = 256
        swc.stride = 128
        f, coh2d = swc.compute(x, y)
        # Check output shape: (n_windows, n_freqs)
        assert coh2d.ndim == 2
        assert coh2d.shape[1] == len(f)
        # Should have at least a few windows
        assert coh2d.shape[0] > 1
        # Coherence at the sine frequency should be high in at least one window
        sine_idx = np.argmin(np.abs(f - 0.1))
        assert np.any(coh2d[:, sine_idx] > 0.5)

        # Optional: plot the 2D coherence as a pcolor plot
        plot = False  # Set to True to enable plotting
        if plot:
            import matplotlib.pyplot as plt
            fig, axs = plt.subplots(2, 1, figsize=(10, 7), sharex=False)
            # Top panel: time series
            axs[0].plot(x, label='x', alpha=0.7)
            axs[0].plot(y, label='y', alpha=0.7)
            axs[0].set_ylabel('Amplitude')
            axs[0].set_title('Input Time Series')
            axs[0].legend()
            # Bottom panel: coherence spectrogram
            mesh = axs[1].pcolormesh(np.arange(coh2d.shape[0]), f, coh2d.T, shading='auto', cmap='viridis', vmin=0, vmax=1)
            cbar = plt.colorbar(mesh, ax=axs[1], label='Coherence')
            cbar.ax.set_title("[0.00, 1.00]")
            axs[1].set_xlabel('Window Index')
            axs[1].set_ylabel('Frequency (Hz)')
            axs[1].set_title('Striding Window Coherence')
            plt.tight_layout()
            plt.show()
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
