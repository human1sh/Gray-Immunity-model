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
    """Plot histograms of population ID_50 at selected time steps."""
    if time_steps is None:
        T = result.params.T
        time_steps = [0, T // 4, T // 2, (3 * T) // 4, T]

    fig, ax = plt.subplots(figsize=(10, 5))
    for t in time_steps:
        if 0 <= t <= result.params.T:
            ax.hist(
                result.id50_history[:, t],
                bins=40,
                alpha=0.45,
                label=f"t = {t}",
                density=True,
            )

    ax.set_xlabel("Immunity Level ID50 (EU)")
    ax.set_ylabel("Density")
    ax.set_title("Population Immunity Distribution Over Time")
    ax.legend()
    ax.grid(linewidth=0.5, alpha=0.6)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    if show:
        plt.show()
    return fig
