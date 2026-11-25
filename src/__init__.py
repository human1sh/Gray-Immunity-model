"""Gray Immunity Epidemiological Model.

An individual-based stochastic epidemiological model treating immunity as a
continuous variable ("gray immunity") and incorporating small immunity effects
(SIEs): cross-immunity, subclinical exposures, and gradual immunity decay.

Reference:
    Watve, M., Bhisikar, H., Kharate, R., & Bajpai, S. (2024).
    Epidemiology: Gray immunity model gives qualitatively different predictions.
    Journal of Biosciences, 49, 10. https://doi.org/10.1007/s12038-023-00382-y
"""

from .parameters import ModelParameters
from .simulation import SimulationResult, run_simulation
from .visualization import plot_immunity_distribution, plot_wave_dynamics

__all__ = [
    "ModelParameters",
    "SimulationResult",
    "run_simulation",
    "plot_wave_dynamics",
    "plot_immunity_distribution",
]
