"""Visualization utilities for the Gray Immunity model."""

import matplotlib.pyplot as plt
import numpy as np

from .simulation import SimulationResult


def plot_wave_dynamics(
    result: SimulationResult,
    save_path: str | None = None,
    show: bool = True,
) -> plt.Figure:
    """Plot infected counts I(t) and mean population immunity ID_50 over time."""
    T = result.params.T
    time = np.arange(T)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    ax1.plot(time, result.infected_counts, color="tab:green", label="Infected I(t)")
    ax2.plot(time, result.mean_id50, color="tab:orange", linestyle="--", label="Mean ID50")

    ax1.set_xlabel("Time step (t)")
    ax1.set_ylabel("Infected individuals I(t)", color="tab:green")
    ax2.set_ylabel("Mean Immunity ID50 (EU)", color="tab:orange")
    ax1.set_title("Gray Immunity Model: Infection Waves and Mean Immunity")
    ax1.grid(linestyle="-", linewidth=0.5, alpha=0.6)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    if show:
        plt.show()
    return fig


def plot_immunity_distribution(
    result: SimulationResult,
    time_steps: list[int] | None = None,
    save_path: str | None = None,
    show: bool = True,
) -> plt.Figure:
    """Plot a 3D histogram of population ID_50 across selected time steps."""
    T = result.params.T
    if time_steps is None:
        time_steps = [int(round(x)) for x in np.linspace(T, 0, 6)]

    colors = ["orange", "green", "red", "gold", "magenta", "blue"]
    nbins = 50
    thresh = 200

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    for idx, t in enumerate(time_steps):
        if 0 <= t <= T:
            arr = result.id50_history[:, t]
            false_vals = arr[arr < thresh]
            if len(false_vals) == 0:
                continue
            hist, xbins = np.histogram(false_vals, bins=nbins)
            xs = (xbins[:-1] + xbins[1:]) / 2
            width = (xbins[1] - xbins[0]) * 0.85 if len(xbins) > 1 else 2.0
            ax.bar(
                xs,
                hist,
                zs=t,
                zdir="y",
                width=width,
                color=colors[idx % len(colors)],
                alpha=0.85,
            )

    ax.set_title("Histogram of $ID_{50}$ for Various Time Steps")
    ax.set_xlabel("$ID_{50}$ (EU)")
    ax.set_ylabel("Time step (t)")
    ax.set_zlabel("Frequency")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    if show:
        plt.show()
    return fig
