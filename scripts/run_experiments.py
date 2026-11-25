"""CLI script to run Gray Immunity simulations and save outputs."""

import argparse
from pathlib import Path
import sys

import numpy as np

# Allow running directly from repository root without installing package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gray_immunity import ModelParameters, plot_wave_dynamics, run_simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Gray Immunity epidemiological simulation.")
    parser.add_argument("-N", type=int, default=5000, help="Population size (default: 5000)")
    parser.add_argument("-T", type=int, default=500, help="Number of time steps (default: 500)")
    parser.add_argument("-r", type=float, default=0.1, help="Restriction parameter (default: 0.1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory to save simulation outputs",
    )
    parser.add_argument("--no-plot", action="store_true", help="Skip saving plot")
    args = parser.parse_args()

    params = ModelParameters(N=args.N, T=args.T, r=args.r, seed=args.seed)
    result = run_simulation(params)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.out_dir / "infected_counts.csv", result.infected_counts, delimiter=",", fmt="%d")
    np.savetxt(args.out_dir / "mean_id50.csv", result.mean_id50, delimiter=",", fmt="%.4f")

    if not args.no_plot:
        plot_wave_dynamics(result, save_path=str(args.out_dir / "wave_dynamics.png"), show=False)

    print(f"Simulation complete (N={args.N}, T={args.T}, r={args.r}, seed={args.seed}).")
    print(f"Peak infected: {result.infected_counts.max()} | Final infected: {result.infected_counts[-1]}")
    print(f"Outputs saved to {args.out_dir}/")


if __name__ == "__main__":
    main()
