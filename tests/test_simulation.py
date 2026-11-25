"""Unit tests for the Gray Immunity simulation."""

import unittest
import numpy as np
from src.parameters import ModelParameters
from src.simulation import run_simulation

class TestGrayImmunitySimulation(unittest.TestCase):
    def test_output_shapes_and_non_negative_immunity(self) -> None:
        params = ModelParameters(N=200, T=30, r=0.1, seed=42)
        result = run_simulation(params)
        self.assertEqual(result.infected_counts.shape, (30,))
        self.assertEqual(result.mean_id50.shape, (30,))
        self.assertEqual(result.id50_history.shape, (200, 31))
        self.assertEqual(result.state_history.shape, (200, 31))
        self.assertTrue(np.all(result.id50_history >= 0.0))
        self.assertTrue(np.all((result.state_history == 0) | (result.state_history == 1)))

    def test_reproducibility_with_seed(self) -> None:
        p1 = ModelParameters(N=150, T=25, seed=123)
        p2 = ModelParameters(N=150, T=25, seed=123)
        r1 = run_simulation(p1)
        r2 = run_simulation(p2)
        np.testing.assert_array_equal(r1.infected_counts, r2.infected_counts)
        np.testing.assert_allclose(r1.mean_id50, r2.mean_id50)

if __name__ == "__main__":
    unittest.main()
