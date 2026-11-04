# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""Assignment regressions runnable without pytest or model downloads."""

import unittest
from itertools import permutations
from unittest.mock import patch

import lapcpp
import numpy as np
import torch

from ultralytics.trackers.utils.matching import linear_assignment
from ultralytics.utils.ops import linear_sum_assignment


def minimum_assignment_cost(cost):
    """Enumerate full matchings independently for small rectangular matrices."""
    if cost.shape[0] > cost.shape[1]:
        cost = cost.T
    rows, columns = cost.shape
    return min(
        sum(cost[row, column] for row, column in enumerate(choice))
        for choice in permutations(range(columns), rows)
    )


class LinearSumAssignmentTests(unittest.TestCase):
    def assert_optimal_assignment(self, cost, solver_input=None):
        rows, columns = linear_sum_assignment(cost if solver_input is None else solver_input)
        count = min(cost.shape)
        self.assertEqual(rows.shape, (count,))
        self.assertEqual(columns.shape, (count,))
        self.assertTrue(np.issubdtype(rows.dtype, np.integer))
        self.assertTrue(np.issubdtype(columns.dtype, np.integer))
        self.assertEqual(len(set(rows)), count)
        self.assertEqual(len(set(columns)), count)
        self.assertTrue(np.all(rows[:-1] < rows[1:]))
        self.assertTrue(np.all((rows >= 0) & (rows < cost.shape[0])))
        self.assertTrue(np.all((columns >= 0) & (columns < cost.shape[1])))
        self.assertAlmostEqual(float(cost[rows, columns].sum()), minimum_assignment_cost(cost))

    def test_small_matrices_match_independent_global_optima(self):
        rng = np.random.default_rng(20261104)
        for shape in ((rows, columns) for rows in range(1, 5) for columns in range(1, 5)):
            costs = (rng.normal(size=shape), rng.integers(-3, 4, size=shape), np.ones(shape))
            for cost in costs:
                with self.subTest(shape=shape, dtype=cost.dtype, tied=np.all(cost == cost.flat[0])):
                    self.assert_optimal_assignment(cost)

    def test_empty_dimensions(self):
        for shape in ((0, 0), (0, 4), (4, 0)):
            with self.subTest(shape=shape):
                self.assert_optimal_assignment(np.empty(shape))

    def test_noncontiguous_and_cpu_tensor_inputs(self):
        cost = np.arange(48, dtype=np.float32).reshape(6, 8)[::2, ::2]
        self.assertFalse(cost.flags.c_contiguous)
        self.assert_optimal_assignment(cost)
        self.assert_optimal_assignment(cost, torch.tensor(cost, device="cpu"))

    def test_positive_infinity_forbids_edges(self):
        for cost in (
            np.array([[1., np.inf], [np.inf, 2.]]),
            np.array([[np.inf, 1., np.inf], [np.inf, np.inf, 2.]]),
            np.array([[np.inf, np.inf], [1., np.inf], [np.inf, 2.]]),
        ):
            with self.subTest(shape=cost.shape):
                self.assert_optimal_assignment(cost)

    def test_infeasible_required_assignment_raises(self):
        costs = (
            np.array([[np.inf]]),
            np.array([[1., np.inf], [2., np.inf]]),
            np.array([[1., np.inf, np.inf], [2., np.inf, np.inf]]),
            np.array([[1., 2.], [np.inf, np.inf], [np.inf, np.inf]]),
        )
        for cost in costs:
            with self.subTest(shape=cost.shape), self.assertRaises(ValueError):
                linear_sum_assignment(cost)

    def test_nan_and_negative_infinity_are_rejected(self):
        for value in (np.nan, -np.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                linear_sum_assignment(np.array([[0., value], [1., 2.]]))

    def test_lapcpp_is_the_general_assignment_backend(self):
        with patch.object(lapcpp, "lapjv", wraps=lapcpp.lapjv) as solve:
            self.assert_optimal_assignment(np.array([[3., 1., 2.], [1., 4., 5.]]))
        solve.assert_called_once()


class TrackingAssignmentTests(unittest.TestCase):
    def test_threshold_rejection_and_unmatched_indices(self):
        cost = np.array([[.1, .8, .9], [.9, .7, .8]], dtype=np.float32)
        matches, unmatched_rows, unmatched_columns = linear_assignment(cost, thresh=.5)
        np.testing.assert_array_equal(matches, [[0, 0]])
        np.testing.assert_array_equal(unmatched_rows, [1])
        np.testing.assert_array_equal(unmatched_columns, [1, 2])

    def test_all_rejected_edges_return_well_shaped_empty_matches(self):
        matches, unmatched_rows, unmatched_columns = linear_assignment(np.ones((2, 3)), thresh=.5)
        self.assertEqual(matches.shape, (0, 2))
        np.testing.assert_array_equal(unmatched_rows, [0, 1])
        np.testing.assert_array_equal(unmatched_columns, [0, 1, 2])

    def test_empty_inputs_preserve_all_unmatched_endpoints(self):
        for shape in ((0, 0), (0, 3), (3, 0)):
            for use_lap in (True, False):
                with self.subTest(shape=shape, use_lap=use_lap):
                    matches, unmatched_rows, unmatched_columns = linear_assignment(
                        np.empty(shape), thresh=.5, use_lap=use_lap
                    )
                    self.assertEqual(matches.shape, (0, 2))
                    np.testing.assert_array_equal(unmatched_rows, np.arange(shape[0]))
                    np.testing.assert_array_equal(unmatched_columns, np.arange(shape[1]))

    def test_both_tracking_modes_use_lapcpp_and_legacy_gate_is_inclusive(self):
        cost = np.array([[.1, .8], [.9, .2]])
        with patch.object(lapcpp, "lapjv", wraps=lapcpp.lapjv) as solve:
            default_matches, _, _ = linear_assignment(cost, thresh=.5)
        solve.assert_called_once()
        np.testing.assert_array_equal(default_matches, [[0, 0], [1, 1]])
        # Full assignment followed by <= filtering retains an edge exactly at the limit.
        # Finite-limit rejection can choose either cardinality at this equal-cost boundary.
        with patch.object(lapcpp, "lapjv", wraps=lapcpp.lapjv) as solve:
            legacy_matches, unmatched_rows, unmatched_columns = linear_assignment(
                np.array([[.5]]), thresh=.5, use_lap=False
            )
        solve.assert_called_once()
        np.testing.assert_array_equal(legacy_matches, [[0, 0]])
        self.assertEqual(len(unmatched_rows), 0)
        self.assertEqual(len(unmatched_columns), 0)


if __name__ == "__main__":
    unittest.main()
