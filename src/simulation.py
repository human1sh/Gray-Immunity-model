"""Core stochastic individual-based simulation for the Gray Immunity model."""

from dataclasses import dataclass
import numpy as np
from src.parameters import ModelParameters


@dataclass
class SimulationResult:
    """Container for outputs of a gray immunity simulation run."""

    params: ModelParameters
    infected_counts: np.ndarray
    mean_id50: np.ndarray
    id50_history: np.ndarray
    state_history: np.ndarray


def _positive_normal(rng: np.random.Generator, mean: float, sd: float, size: int) -> np.ndarray:
    """Sample from a normal distribution, clamping negative values to 1e-4."""
    vals = np.round(rng.normal(mean, sd, size=size), 3)
    return np.where(vals < 0, 1e-4, vals)


def run_simulation(params: ModelParameters | None = None) -> SimulationResult:
    """Run the individual-based gray immunity epidemiological simulation.

    Args:
        params: ModelParameters instance. Uses defaults if None.

    Returns:
        SimulationResult containing time series of infected counts, mean ID_50,
        and full individual-level state/immunity histories.
    """
    if params is None:
        params = ModelParameters()

    rng = np.random.default_rng(params.seed)
    N, T = params.N, params.T

    # Initialize individual states
    S_curr = rng.choice(
        [0, 1],
        size=N,
        p=[1.0 - params.initial_infected_frac, params.initial_infected_frac],
    ).astype(np.int8)
    E = _positive_normal(rng, 20.0 * params.r, 0.01, N)
    ID_50_curr = _positive_normal(rng, params.id50_init_mean, params.id50_init_sd, N)
    SCE_50 = _positive_normal(rng, params.sce50_init_mean, params.sce50_init_sd, N)

    ID_50_history = np.zeros((N, T + 1), dtype=np.float64)
    S_history = np.zeros((N, T + 1), dtype=np.int8)
    ID_50_history[:, 0] = ID_50_curr
    S_history[:, 0] = S_curr

    infected_counts = np.zeros(T, dtype=np.int64)
    mean_id50 = np.zeros(T, dtype=np.float64)

    E_pow_a = E ** params.a
    SCE_pow_a = SCE_50 ** params.a

    for t in range(T):
        I_t = int(np.sum(S_curr))
        infected_counts[t] = I_t
        mean_id50[t] = float(np.mean(ID_50_curr))

        I_trans = (params.I_cmax * I_t) / (params.K + I_t)
        P_inf = E_pow_a / ((ID_50_curr ** params.a) + E_pow_a)
        P1 = 1.0 - ((1.0 - P_inf) ** I_trans)

        P_sce = E_pow_a / (SCE_pow_a + E_pow_a)
        P2 = 1.0 - ((1.0 - P_sce) ** I_trans)

        S_next = np.zeros(N, dtype=np.int8)
        ID_50_next = np.zeros(N, dtype=np.float64)

        # Draw uniform random numbers for all individuals
        u_rec = rng.random(N)
        u_inf = rng.random(N)
        u_sce = rng.random(N)
        u_ci = rng.random(N)

        # Currently infected individuals (S == 1)
        inf_mask = S_curr == 1
        rec_mask = inf_mask & (u_rec < params.P_r)
        S_next[rec_mask] = 0
        ID_50_next[rec_mask] = ID_50_curr[rec_mask] + params.I_mf

        not_rec_mask = inf_mask & ~rec_mask
        reinf_mask = not_rec_mask & (u_inf < P1)
        S_next[reinf_mask] = 1
        ID_50_next[reinf_mask] = ID_50_curr[reinf_mask]

        not_reinf_mask = not_rec_mask & ~reinf_mask
        S_next[not_reinf_mask] = 0
        sce_inf_mask = not_reinf_mask & (u_sce < P2)
        ID_50_next[sce_inf_mask] = ID_50_curr[sce_inf_mask] + params.I_sce

        decay_inf_mask = not_reinf_mask & ~sce_inf_mask
        ID_50_next[decay_inf_mask] = np.maximum(0.0, ID_50_curr[decay_inf_mask] - params.I_d)

        # Currently susceptible/uninfected individuals (S == 0)
        susc_mask = ~inf_mask
        new_inf_mask = susc_mask & (u_inf < P1)
        S_next[new_inf_mask] = 1
        ID_50_next[new_inf_mask] = ID_50_curr[new_inf_mask]

        stay_susc_mask = susc_mask & ~new_inf_mask
        S_next[stay_susc_mask] = 0

        sce_susc_mask = stay_susc_mask & (u_sce < P2)
        ci_and_sce = sce_susc_mask & (u_ci < params.P_c)
        only_sce = sce_susc_mask & ~ci_and_sce
        ID_50_next[ci_and_sce] = ID_50_curr[ci_and_sce] + params.I_sce + params.I_c
        ID_50_next[only_sce] = ID_50_curr[only_sce] + params.I_sce

        no_sce_susc = stay_susc_mask & ~sce_susc_mask
        ci_only = no_sce_susc & (u_ci < params.P_c)
        neither = no_sce_susc & ~ci_only
        ID_50_next[ci_only] = np.maximum(0.0, ID_50_curr[ci_only] - params.I_d + params.I_c)
        ID_50_next[neither] = np.maximum(0.0, ID_50_curr[neither] - params.I_d)

        S_curr = S_next
        ID_50_curr = ID_50_next
        S_history[:, t + 1] = S_curr
        ID_50_history[:, t + 1] = ID_50_curr

    return SimulationResult(
        params=params,
        infected_counts=infected_counts,
        mean_id50=mean_id50,
        id50_history=ID_50_history,
        state_history=S_history,
    )
