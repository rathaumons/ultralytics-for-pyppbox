# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""Assignment and inference import regressions without pytest or model downloads."""

import os
import subprocess
import sys
import textwrap
import unittest
from itertools import permutations
from pathlib import Path
from tempfile import TemporaryDirectory
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


class InferenceImportTests(unittest.TestCase):
    """Inference and tracking must work when optional training/model modules are unavailable."""

    def run_without_optional_modules(self, code):
        guard = """
            import sys
            from importlib.abc import MetaPathFinder

            def forbidden(name):
                roots = (
                    'ultralytics.engine.trainer', 'ultralytics.engine.validator',
                    'ultralytics.engine.exporter', 'ultralytics.data.base',
                    'ultralytics.data.dataset', 'ultralytics.utils.loss',
                    'ultralytics.models.utils.loss', 'ultralytics.models.fastsam',
                    'ultralytics.models.llm', 'ultralytics.models.rtdetr',
                    'ultralytics.models.sam',
                )
                return (
                    any(name == root or name.startswith(root + '.') for root in roots)
                    or (name.startswith('ultralytics.models.')
                        and name.rsplit('.', 1)[-1] in ('train', 'train_seg', 'train_world', 'val'))
                )

            class ImportBoundary(MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if forbidden(fullname):
                        raise AssertionError('Inference imported optional module: ' + fullname)

            sys.meta_path.insert(0, ImportBoundary())
        """
        check = "\nassert not any(forbidden(name) for name in sys.modules)\n"
        with TemporaryDirectory() as config_dir:
            env = dict(os.environ, YOLO_AUTOINSTALL="false", YOLO_OFFLINE="true",
                       YOLO_CONFIG_DIR=config_dir, PYTHONIOENCODING="utf-8")
            result = subprocess.run(
                [sys.executable, "-c", textwrap.dedent(guard) + textwrap.dedent(code) + check],
                cwd=Path(__file__).resolve().parents[1], env=env, capture_output=True,
                text=True, encoding="utf-8", errors="replace", timeout=60,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_yolo_and_nas_import_without_training_or_other_families(self):
        self.run_without_optional_modules("""
            from ultralytics import NAS, YOLO
            assert YOLO.__name__ == 'YOLO'
            assert NAS.__name__ == 'NAS'
        """)

    def test_custom_model_task_maps_control_component_loading(self):
        self.run_without_optional_modules("""
            import torch
            from ultralytics import YOLO
            from ultralytics.engine.model import Model

            class CustomNetwork:
                pass

            class CustomPredictor:
                pass

            for base in (Model, YOLO):
                class Extension(base):
                    def __init__(self):
                        torch.nn.Module.__init__(self)
                        self.task = 'detect'

                    @property
                    def task_map(self):
                        return {'detect': {'model': CustomNetwork, 'predictor': CustomPredictor}}

                extension = Extension()
                assert extension._smart_load('model') is CustomNetwork
                assert extension._smart_load('predictor') is CustomPredictor
        """)

    def test_prediction_embedding_and_model_tracking_do_not_load_training(self):
        self.run_without_optional_modules("""
            from pathlib import Path
            from tempfile import TemporaryDirectory
            import numpy as np
            import torch
            from ultralytics import YOLO
            from ultralytics.nn.tasks import torch_safe_load
            from ultralytics.utils import ROOT

            image = np.zeros((64, 64, 3), dtype=np.uint8)
            for task, filename in (
                ('detect', 'yolov8.yaml'), ('pose', 'yolov8-pose.yaml'),
                ('classify', 'yolov8-cls.yaml'),
            ):
                model = YOLO(ROOT / 'cfg/models/v8' / filename, verbose=False)
                with TemporaryDirectory() as checkpoint_dir:
                    checkpoint = Path(checkpoint_dir) / (task + '.pt')
                    model.save(checkpoint)
                    safe_checkpoint, _ = torch_safe_load(checkpoint, safe_only=True)
                    assert isinstance(safe_checkpoint['model'], type(model.model))
                    model = YOLO(checkpoint, verbose=False)
                result, = model.predict(image, imgsz=64, device='cpu', save=False, verbose=False)
                assert model.task == task and result.orig_shape == image.shape[:2]
                if task == 'classify':
                    assert result.probs is not None
                    embeddings = model.embed(image, imgsz=64, device='cpu', verbose=False)
                    assert len(embeddings) == 1 and isinstance(embeddings[0], torch.Tensor)
                else:
                    assert result.boxes is not None
                    if task == 'pose':
                        assert result.keypoints is not None
                    tracked, = model.track(image, imgsz=64, device='cpu', save=False,
                                           verbose=False, tracker='bytetrack.yaml', persist=True)
                    assert tracked.boxes is not None and len(model.predictor.trackers) == 1
        """)

    def test_all_trackers_and_native_reid_work_without_training_imports(self):
        self.run_without_optional_modules("""
            import numpy as np
            from ultralytics.engine.results import Boxes
            from ultralytics.trackers.track import TRACKER_MAP
            from ultralytics.utils import ROOT, YAML, IterableSimpleNamespace

            assert len(TRACKER_MAP) == 6
            image = np.zeros((80, 120, 3), dtype=np.uint8)
            features = np.array([[1., 0., 0., 0.]], dtype=np.float32)
            for name, tracker_type in TRACKER_MAP.items():
                config = YAML.load(ROOT / 'cfg/trackers' / (name + '.yaml'))
                config['gmc_method'] = 'none'
                config['with_reid'] = name in ('botsort', 'deepocsort', 'tracktrack')
                config['model'] = 'auto'
                tracker = tracker_type(IterableSimpleNamespace(**config))
                ids = []
                for offset in range(3):
                    data = np.array([[10 + offset, 10, 40 + offset, 60, .95, 0]], dtype=np.float32)
                    tracks = tracker.update(Boxes(data, image.shape[:2]), img=image, feats=features)
                    assert len(tracks) == 1, (name, tracks)
                    ids.append(int(tracks[0, 4]))
                assert len(set(ids)) == 1, (name, ids)
                if config['with_reid']:
                    assert tracker.tracked_stracks[0].smooth_feat is not None
                tracker.update(Boxes(np.empty((0, 6), dtype=np.float32), image.shape[:2]), img=image)
        """)


if __name__ == "__main__":
    unittest.main()
