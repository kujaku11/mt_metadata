import matplotlib.pyplot as plt
import numpy as np

from matplotlib.gridspec import GridSpec
from scipy import signal


def is_flat_amplitude(array):
    """
    Check of an amplitude response is basically flat.  If so, it is best to tune the y-axis lims to
    make numeric noise invisible

    Parameters
    ----------
    array

    Returns
    -------

    """
    differences = np.diff(np.abs(array))
    if np.isclose(differences, 0.0).all():
        return True
    else:
        return False


def cast_angular_frequency_to_period_or_hertz(w, units):
    if units.lower() == "period":
        x_axis = (2.0 * np.pi) / w
    elif units.lower() == "frequency":
        x_axis = w / (2.0 * np.pi)
    return x_axis


def plot_response(
    w_obs=None,
    resp_obs=None,
    zpk_obs=None,
    zpk_pred=None,
    w_values=None,
    xlim=None,
    title=None,
    x_units="Period",
):
    """
    This function was contributed by Ben Murphy at USGS
    2021-03-17: there are some issues encountered when using this function to plot generic resposnes, looks
    like the x-axis gets out of order when using frequency as the axis ... 
    Parameters
    ----------
    w_obs
    resp_obs
    zpk_obs
    zpk_pred
    w_values
    xlim
    title

    Returns
    -------

    """
    fig = plt.figure(figsize=(14, 4))
    if title is not None:
        fig.suptitle(title)
    gs = GridSpec(2, 3)
    ax_amp = fig.add_subplot(gs[0, :2])
    ax_phs = fig.add_subplot(gs[1, :2])
    ax_pz = fig.add_subplot(gs[:, 2], aspect="equal")

    if w_obs is not None and resp_obs is not None:
        kwargs = {}

        response_amplitude = np.absolute(resp_obs)
        if is_flat_amplitude(resp_obs):
            response_amplitude[:] = response_amplitude[0]
            ax_amp.set_ylim([0.9 * response_amplitude[0], 1.1 * response_amplitude[0]])
        x_values = cast_angular_frequency_to_period_or_hertz(w_obs, x_units)
        ax_amp.plot(
            x_values,
            response_amplitude,
            color="tab:blue",
            linewidth=1.5,
            linestyle="-",
            label="True",
        )
        ax_phs.plot(
            x_values,
            np.angle(resp_obs, deg=True),
            color="tab:blue",
            linewidth=1.5,
            linestyle="-",
        )
    elif zpk_obs is not None:
        w_obs, resp_obs = signal.freqresp(zpk_obs, w=w_values)
        x_values = cast_angular_frequency_to_period_or_hertz(w_obs, x_units)
        ax_amp.plot(
            x_values,
            np.absolute(resp_obs),
            color="tab:blue",
            linewidth=1.5,
            linestyle="-",
            label="True",
        )
        ax_phs.plot(
            x_values,
            np.angle(resp_obs, deg=True),
            color="tab:blue",
            linewidth=1.5,
            linestyle="-",
        )
        ax_pz.scatter(
            np.real(zpk_obs.zeros),
            np.imag(zpk_obs.zeros),
            s=75,
            marker="o",
            ec="tab:blue",
            fc="w",
            label="True Zeros",
        )
        ax_pz.scatter(
            np.real(zpk_obs.poles),
            np.imag(zpk_obs.poles),
            s=75,
            marker="x",
            ec="tab:blue",
            fc="tab:blue",
            label="True Poles",
        )

    if zpk_pred is not None:
        w_pred, resp_pred = signal.freqresp(zpk_pred, w=w_values)
        x_values = cast_angular_frequency_to_period_or_hertz(w_values, x_units)

        ax_amp.plot(
            x_values,
            np.absolute(resp_pred),
            color="tab:red",
            linewidth=3,
            linestyle=":",
            label="Fit",
        )
        # print(np.angle(resp_pred, deg=True))
        ax_phs.plot(
            x_values,
            np.angle(resp_pred, deg=True),
            color="tab:red",
            linewidth=3,
            linestyle=":",
        )
        ax_pz.scatter(
            np.real(zpk_pred.zeros),
            np.imag(zpk_pred.zeros),
            s=35,
            marker="o",
            ec="tab:red",
            fc="w",
            label="Fit Zeros",
        )
        ax_pz.scatter(
            np.real(zpk_pred.poles),
            np.imag(zpk_pred.poles),
            s=35,
            marker="x",
            ec="tab:red",
            fc="tab:blue",
            label="Fit Poles",
        )

    if xlim is not None:
        ax_amp.set_xlim(xlim)
        ax_phs.set_xlim(xlim)

    ax_amp.set_xscale("log")
    ax_amp.set_yscale("log")
    ax_amp.set_ylabel("Amplitude Response")
    ax_amp.grid()
    ax_amp.legend()

    ax_phs.set_ylim([-200.0, 200.0])
    ax_phs.set_xscale("log")
    ax_phs.set_ylabel("Phase Response")
    if x_units.lower() == "period":
        x_label = "Period (s)"
    elif x_units.lower() == "frequency":
        x_label = "Frequency (Hz)"
    ax_phs.set_xlabel(x_label)
    ax_phs.grid()

    ax_pz.set_xlabel("Re(z)")
    ax_pz.set_ylabel("Im(z)")
    max_lim = max(
        [
            abs(ax_pz.get_ylim()[0]),
            abs(ax_pz.get_ylim()[1]),
            abs(ax_pz.get_xlim()[0]),
            abs(ax_pz.get_xlim()[0]),
        ]
    )
    ax_pz.set_ylim([-1.25 * max_lim, 1.25 * max_lim])
    ax_pz.set_xlim([-1.25 * max_lim, 1.25 * max_lim])
    ax_pz.grid()
    ax_pz.legend()

    plt.show()
