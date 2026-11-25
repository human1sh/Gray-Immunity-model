"""Model parameters for the Gray Immunity stochastic simulation."""

from dataclasses import dataclass


@dataclass
class ModelParameters:
    """Configuration parameters for the individual-based gray immunity model.

    Attributes:
        N: Population size.
        T: Number of discrete time steps.
        P_r: Probability that an infected individual recovers in a time step.
        I_mf: Immunity increment upon recovery from clinical infection (EU).
        I_sce: Immunity increment from subclinical exposure (EU).
        I_d: Immunity decay per time step without exposure/infection (EU).
        I_c: Immunity increment due to cross-immunity from other infections (EU).
        a: Hill/sigmoid sharpness parameter for infection/exposure probability.
        r: Restriction / contact reduction parameter.
        P_c: Probability of cross-immunity event per time step (defaults to 0.1 * r).
        I_cmax: Maximum infective contacts per time step (defaults to 30 * r).
        K: Half-saturation constant for transmission.
        initial_infected_frac: Initial fraction of infected individuals at t=0.
        id50_init_mean: Mean of initial ID_50 distribution.
        id50_init_sd: Standard deviation of initial ID_50 distribution.
        sce50_init_mean: Mean of initial SCE_50 distribution.
        sce50_init_sd: Standard deviation of initial SCE_50 distribution.
        seed: Optional random seed for reproducibility.
    """

    N: int = 5000
    T: int = 500
    P_r: float = 0.2
    I_mf: float = 200.0
    I_sce: float = 20.0
    I_d: float = 3.0
    I_c: float = 30.0
    a: float = 2.0
    r: float = 0.1
    P_c: float | None = None
    I_cmax: float | None = None
    K: float = 2500.0
    initial_infected_frac: float = 0.05
    id50_init_mean: float = 100.0
    id50_init_sd: float = 30.0
    sce50_init_mean: float = 20.0
    sce50_init_sd: float = 5.0
    seed: int | None = None

    def __post_init__(self) -> None:
        if self.P_c is None:
            self.P_c = 0.1 * self.r
        if self.I_cmax is None:
            self.I_cmax = 30.0 * self.r
