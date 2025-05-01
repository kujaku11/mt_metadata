import matplotlib.pyplot as plt
import numpy as np

from matplotlib.gridspec import GridSpec


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
    frequencies,
    complex_response,
    poles=None,
    zeros=None,
    xlim=None,
    title=None,
    x_units="Period",
    unwrap=True,
    pass_band=None,
    label=None,
    normalization_frequency=None,
):
    """
    This function was contributed by Ben Murphy at USGS
    2021-03-17: there are some issues encountered when using this function to plot generic resposnes, looks
    like the x-axis gets out of order when using frequency as the axis ...

    Edited 2021-11-18 JP to be more instructive and general.

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

    if poles is not None or zeros is not None:
        gs = GridSpec(2, 3)
        ax_amp = fig.add_subplot(gs[0, :2])
        ax_phs = fig.add_subplot(gs[1, :2], sharex=ax_amp)
        ax_pz = fig.add_subplot(gs[:, 2], aspect="equal")
    else:
        gs = GridSpec(2, 2)
        ax_amp = fig.add_subplot(gs[0, :2])
        ax_phs = fig.add_subplot(gs[1, :2], sharex=ax_amp)

    if not isinstance(complex_response, list):
        complex_response = [complex_response]

    if not isinstance(label, list):
        label = [label]

    assert len(label) == len(complex_response)

    if x_units.lower() == "period":
        frequencies = 1.0 / frequencies

    amp_min = []
    amp_max = []
    phase_min = []
    phase_max = []
    lines = []
    for name, cr in zip(label, complex_response):
        response_amplitude = np.absolute(cr)
        if is_flat_amplitude(cr):
            response_amplitude[:] = response_amplitude[0]

        if unwrap:
            response_phase = np.rad2deg(np.unwrap(np.angle(cr, deg=False)))
        else:
            response_phase = np.angle(cr, deg=True)

        amp_min.append(response_amplitude.min())
        amp_max.append(response_amplitude.max())
        phase_min.append(response_phase.min())
        phase_max.append(response_phase.max())

        # plot amplitude
        l1 = ax_amp.plot(
            frequencies,
            response_amplitude,
            linewidth=1.5,
            linestyle="-",
            label=name,
        )
        lines.append(l1)

        # plot phase
        ax_phs.plot(
            frequencies,
            response_phase,
            linewidth=1.5,
            linestyle="-",
        )

        # plot pass band
        if pass_band is not None:
            if x_units.lower() == "period":
                pass_band = 1.0 / pass_band

            ax_amp.fill_between(
                pass_band,
                [10e-20, 10e-20],
                [10e10, 10e10],
                color=(0.7, 0.7, 0.7),
                alpha=0.7,
                zorder=1,
            )

            ax_phs.fill_between(
                pass_band,
                [-100000, -100000],
                [100000, 100000],
                color=(0.7, 0.7, 0.7),
                alpha=0.7,
                zorder=1,
            )

        if poles is not None:
            ax_pz.scatter(
                np.real(poles),
                np.imag(poles),
                s=75,
                marker="x",
                ec="tab:blue",
                fc="tab:blue",
                label="Poles",
            )
        if zeros is not None:
            ax_pz.scatter(
                np.real(zeros),
                np.imag(zeros),
                s=75,
                marker="o",
                ec="tab:blue",
                fc="w",
                label="Zeros",
            )

    if normalization_frequency is not None:
        if x_units.lower() == "period":
            try:
                normalization_frequency = 1.0 / normalization_frequency
            except ZeroDivisionError:
                pass
        ax_amp.plot(
            [normalization_frequency, normalization_frequency],
            [10e-20, 10e10],
            color="k",
            lw=2,
        )
        ax_phs.plot(
            [normalization_frequency, normalization_frequency],
            [-10000, 10000],
            color="k",
            lw=2,
        )

    if xlim is not None:
        ax_amp.set_xlim(xlim)
    else:
        if x_units.lower() == "period":
            ax_amp.set_xlim([frequencies.max(), frequencies.min()])
        else:
            ax_amp.set_xlim([frequencies.min(), frequencies.max()])

    ax_amp.set_xscale("log")
    ax_amp.set_yscale("log")
    ax_amp.set_ylabel("Amplitude Response")
    ax_amp.grid()
    ax_amp.set_ylim(
        [
            10 ** (np.floor(np.log10(min(amp_min))) - 1),
            10 ** (np.ceil(np.log10(max(amp_max))) + 1),
        ]
    )

    if not unwrap:
        ax_phs.set_ylim([-200.0, 200.0])

    else:
        ax_phs.set_ylim([min(phase_min) - 10, max(phase_max) + 10])

    ax_phs.set_xscale("log")
    ax_phs.set_ylabel("Phase Response")

    if x_units.lower() == "period":
        x_label = "Period (s)"
    elif x_units.lower() == "frequency":
        x_label = "Frequency (Hz)"

    ax_phs.set_xlabel(x_label)
    ax_phs.grid()

    if poles is not None or zeros is not None:
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

    if len(label) > 1:
        fig.legend(
            lines,
            label,
            ncol=len(label),
            loc="upper center",
            borderaxespad=-0.5,
        )
    else:
        fig.suptitle(title)
    plt.tight_layout()

    plt.show()
