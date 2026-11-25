"""Main entry point for running the Gray Immunity epidemiological simulation.
Edit the configuration parameters below and run this file directly (e.g. from
your IDE or `python main.py`) without needing command-line arguments.
"""

import numpy as np
from pathlib import Path
from src.parameters import ModelParameters
from src.simulation import run_simulation
from src.visualization import plot_immunity_distribution, plot_wave_dynamics

# ---------------------------------------------------------------------------
# Configuration — adjust parameters here
# ---------------------------------------------------------------------------
POPULATION_SIZE   = 5000
TIME_STEPS        = 1000
RESTRICTION_PARAM = 0.1
RANDOM_SEED       = 42
OUTPUT_DIR        = Path("results")
SAVE_OUTPUTS      = True
SHOW_PLOTS        = True

def main() -> None:
    params = ModelParameters(N=POPULATION_SIZE, T=TIME_STEPS, r=RESTRICTION_PARAM, seed=RANDOM_SEED)
    result = run_simulation(params)
    print(f"Simulation finished (N={params.N}, T={params.T}, r={params.r}) | "
          f"Peak infected: {result.infected_counts.max()} | "
          f"Final infected: {result.infected_counts[-1]}")
    if SAVE_OUTPUTS:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        np.savetxt(OUTPUT_DIR / "infected_counts.csv", result.infected_counts, delimiter=",", fmt="%d")
        np.savetxt(OUTPUT_DIR / "mean_id50.csv"      , result.mean_id50      , delimiter=",", fmt="%.4f")
        plot_wave_dynamics(        result, save_path=str(OUTPUT_DIR / "wave_dynamics.png")        , show=SHOW_PLOTS)
        plot_immunity_distribution(result, save_path=str(OUTPUT_DIR / "immunity_distribution.png"), show=SHOW_PLOTS)
        print(f"Results saved to {OUTPUT_DIR}/")
    elif SHOW_PLOTS:
        plot_wave_dynamics(result, show=True)
        plot_immunity_distribution(result, show=True)

if __name__ == "__main__":
    main()
