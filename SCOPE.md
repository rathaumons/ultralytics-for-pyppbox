# Maintainer guide: pyppbox scope

Use this guide when updating upstream code, changing dependencies, or considering
file removal. Keep fork-specific maintenance rules here; leave the main README
unchanged when updating this guide.

## Purpose and boundaries

This repository publishes **`pyppbox-ultralytics`** while preserving the
**`ultralytics`** import namespace. Its primary purpose is pyppbox inference.
It also retains Ultralytics tracking and the shared code needed for compatible
model loading, prediction, and ReID.

Pyppbox's `MyYOLOULT` adapter loads `.pt` checkpoints through `YOLO` or its existing
`NAS` branch, predicts on BGR frame arrays, and reads boxes, confidence scores,
and optional pose keypoints. Pose drawing also uses `Colors` and its palette.
Pyppbox supplies its own pipeline tracking and ReID stages.

Training, validation, tuning, export, and integrations still exist in this fork.
They load on demand and can require optional dependencies. Removing those APIs
or their implementations is a separate compatibility change, not routine
unused-file cleanup.

## Where to look

Paths below are relative to this repository unless marked as belonging to pyppbox.

| Area | Files to inspect |
| --- | --- |
| Consumer contract | In pyppbox: `pyppbox/modules/detectors/yoloult/__init__.py`, `pyppbox/utils/visualizetools.py`, and `tests/integration/test_yolo_results.py`. |
| Public imports and task selection | `ultralytics/__init__.py`, `ultralytics/models/**/__init__.py`, `ultralytics/engine/model.py`, and each model family's `model.py`. |
| Prediction and results | `ultralytics/engine/predictor.py`, `ultralytics/engine/results.py`, and `ultralytics/models/yolo/*/predict.py`. |
| Checkpoint loading and compatibility | `ultralytics/nn/tasks.py`, `ultralytics/nn/modules/`, `ultralytics/nn/distill_model.py`, and `ultralytics/utils/loss.py`. |
| Tracking and ReID | `ultralytics/trackers/`, especially `track.py` and `utils/reid.py`; configs are in `ultralytics/cfg/trackers/`, and callback infrastructure is in `ultralytics/utils/callbacks/base.py`. |
| Preprocessing and data helpers | `ultralytics/data/augment.py`, `ultralytics/data/build.py`, `ultralytics/data/loaders.py`, `ultralytics/data/utils.py`, and `ultralytics/data/converter.py`. |
| Shared mathematics and drawing | `ultralytics/utils/ops.py`, `ultralytics/utils/metrics.py`, `ultralytics/utils/plotting.py`, and `ultralytics/utils/tal.py`. |
| Backend selection and formats | `ultralytics/nn/autobackend.py`, `ultralytics/nn/backends/`, and `ultralytics/utils/formats.py`. |
| Defaults and dependencies | `ultralytics/utils/__init__.py`, `ultralytics/utils/checks.py`, `requirements.txt`, and `setup.py`. |
| Packaging and regression checks | `MANIFEST.in`, `.github/workflows/`, and `tests/test_assignment.py`. |

## Keep these invariants

### Inference and tracking

- Preserve the frame-input and result contracts used by pyppbox. Keep boxes,
  confidence scores, and pose rows aligned and in backend order.
- Keep all six trackers: `BYTETracker`, `BOTSORT`, `OCSORT`, `DeepOCSORT`,
  `FASTTracker`, and `TRACKTRACK`, together with their configs and helpers.
- Preserve prediction callback registration, motion compensation, and tracker
  lifecycle behavior. The callback base is shared with tracking; it is not
  exclusively training infrastructure.
- Keep native-feature ReID, `.pt` classification/embedding ReID, and exported-model
  ReID through `AutoBackend`. Classification and non-PyTorch backends are within
  this retention boundary even though pyppbox's detector normally uses `.pt`.
- Preserve tracking-related model families and solutions, including SAM video
  predictors, counters, heatmaps, and the related examples.

### Assignment

- Use **lapcpp only** in `trackers/utils/matching.py` and `utils/ops.py`.
  Do not reintroduce a SciPy solver or pure-NumPy solver fallback.
- Preserve both matching modes: joint thresholded rejection, and the legacy
  capped-cost solve followed by filtering. Keep their unmatched-index behavior.
- Keep empty and rectangular inputs, forbidden `+inf` edges, and infeasibility
  handling. The general assignment helper must reject NaN and negative infinity
  before calling the native solver.
- Test optimal cost and valid matches rather than assuming one exact pairing
  where several equal-cost assignments exist.

### Imports and process settings

- Keep public exports lazy. Importing YOLO/NAS or running normal prediction and
  tracking must not eagerly load unrelated model families, trainers, validators,
  training datasets, or losses.
- Resolve only the requested internal task component. Preserve explicit public
  `task_map` dictionaries and custom subclass overrides. Explicitly requesting
  the full public map can load its listed components.
- Keep format metadata in `utils/formats.py`. Backend recognition and unsupported
  format errors must not import the exporter. Preserve the public
  `ultralytics.engine.exporter.export_formats` alias.
- Default dependency auto-install to **disabled**. Retain explicit opt-in through
  `YOLO_AUTOINSTALL=true`; do not silently install or upgrade packages.
- Preserve the calling application's OpenCV thread settings. Do not restore an
  import-time `cv2.setNumThreads(0)` call during an upstream merge.

### Checkpoint compatibility

Keep model, loss, distillation, transform, and legacy alias paths that `.pt`
files can reference. Deserialization occurs before the loader can discard
training-only state or extract a distilled student model.

A module with no direct source imports can still be required by a serialized
class name, a lazy export, a callback registration, or a configuration value.
Search results alone are not evidence that such a module is removable.

## What may be removed, and what must stay

Consider standalone nontracking examples, unreferenced dataset descriptors, and
unreferenced download scripts for removal. First verify that retained code,
configs, tests, examples, and supported checkpoints do not depend on them.

The current exclusions include standalone C++ and Rust inference examples,
ONNX/SAHI demonstration projects, the general tutorial notebook, unused dataset
YAMLs, and the standalone COCO/weight download scripts. Do not reintroduce these
solely because an upstream sync contains them. Tracking-related examples remain
within scope. Keep links in example documentation consistent with available files.

Apply these specific retention rules:

| Candidate | Rule |
| --- | --- |
| Model definitions and YAMLs | Retain existing model classes, module paths, and model configs for checkpoint and tracking compatibility. |
| Dataset configs | Keep referenced descriptors. `ImageNet.yaml` supports class-name mapping; `coco8.yaml` supplies YOLO-World fallback names. Other descriptors remain referenced by retained code/tests. |
| Data preparation helpers | Keep `ultralytics/data/scripts/get_imagenet.sh` and `ultralytics/data/split.py` while retained code/configuration references them. |
| Preprocessing and results | Keep `LetterBox`, classification transforms, loaders, plotting, and mask conversion. `ops.masks2segments()` reaches `data.converter.merge_multi_segment`. |
| Mathematical helpers | Keep `utils/tal.py`: detection heads and Hailo inference use it. Its role extends beyond training assignment. |
| Export utilities | Inspect individually. TensorRT uses `utils/export/engine.py`, TensorFlow uses `tensorflow.py`, QNN uses `qnn.py`, and Axelera uses `axelera.py` at inference time. Extract shared helpers before considering those files for removal. |
| Training/validation/tuning modules | Retain under the current scope. Future removal must update public methods, CLI modes, task maps, lazy exports, and integration registrations together. |

Do not call a runtime deletion zero-risk. Keep the compatibility layer when its
removal cannot be justified for the supported models and tracking paths.

## Dependency rules

Treat `requirements.txt` as the authoritative core dependency list. It currently
contains NumPy, Pillow, Requests, and lapcpp. Torch, torchvision, and the chosen
OpenCV build are supplied separately by pyppbox or the calling environment;
do not add dependencies that replace that configured runtime stack.

Keep feature-only dependencies in extras defined in `setup.py`:

| Extra | Dependencies and purpose |
| --- | --- |
| `plotting` | Matplotlib and Polars for charts and plotting helpers. |
| `tables` | Polars for DataFrame, CSV, and JSON result exports. |
| `profiling` | ultralytics-thop for FLOPs profiling; preserve its missing-package fallback. |
| `diagnostics` | psutil for resource monitoring and system checks. |
| `solutions`, `logging`, `typing` | Existing optional application, integration, and typing dependencies. |

The fork does not require SciPy for assignment, HUB SDK, or PyYAML. Its `YAML`
utility has an in-tree parser. Do not add these back without identifying a new
runtime requirement. Pyppbox has its own dependency list; changes here do not
remove SciPy, PyYAML, or other requirements from pyppbox itself.

From this checkout, optional features can be installed with:

```sh
python -m pip install ".[plotting,tables,profiling,diagnostics]"
```

## Packaging rules

- Use portable dotted package discovery; do not construct package names from
  platform-specific filesystem paths.
- Include runtime Python modules, `py.typed`, model/tracker/dataset YAMLs,
  referenced shell scripts, sample JPGs, and solution HTML templates.
- Exclude tests and repository configuration files from installed wheels.
  Source distributions may retain tests for development.
- Inspect wheel metadata to confirm the core requirements and optional markers.
  A dependency must not become mandatory merely because an optional module exists.
- Build both wheel and source distributions. Rebuild a wheel from the source
  archive and compare package contents, then exercise the wheel outside the
  checkout to catch missing resources and source-tree shadowing.

## Workflow for upstream updates and cleanup

### Record the baseline and target

Before each sync, record the following in its review notes:

- The previous upstream release/tag and exact upstream commit SHA.
- The current fork commit and pyppbox consumer commit.
- The target upstream release/tag and exact commit SHA.
- Python, Torch, torchvision, OpenCV, lapcpp, and relevant backend/provider versions.
- The checkpoint files, input assets, devices, and configurations used for comparison.

A version string alone does not identify the source baseline. If an earlier sync
recorded only a version, establish the corresponding upstream commit before
integrating its successor. A fork's sync commit is not the upstream commit.

### Integrate in isolation

1. Preserve a clean baseline and use a dedicated branch or worktree for the sync.
   Verify that an upstream remote points to the official
   `https://github.com/ultralytics/ultralytics.git` repository, fetch the desired
   release, and pin the target SHA before reviewing changes.
2. Inspect the upstream baseline-to-target delta, including newly added,
   renamed, or deleted modules, model heads, trackers, backends, configs, format
   entries, and requirements. Existing fork paths are not a complete change list.
3. Choose integration based on verified Git ancestry. A three-way merge needs a
   real common baseline; a previous source-copy sync may need a reviewed port of
   the upstream delta. Do not invent ancestry or replace the fork wholesale.
4. Resolve conflicts by preserving each customization's purpose in the target
   architecture. Do not apply blanket "ours" or "theirs" resolutions. Keep lazy
   imports, lapcpp assignment, defaults, checkpoint aliases, and packaging rules
   even when the upstream implementation moves to different files.
5. Check the current pyppbox adapter. Search imports, lazy export tables, task
   maps, callbacks, configs, tests, and checkpoint class paths before removing
   anything. Include ignored tests in reference audits: new files under `tests/`
   are ignored by default.
6. Separate independent file cleanup from API changes and shared-module refactors.
   Keep each change small enough to compare behavior and packaged resources.

Use separate environments for the previous fork, candidate fork, and unmodified
target upstream where comparisons require them. Official `ultralytics` and
`pyppbox-ultralytics` provide the same import namespace; installing both in one
comparison environment can hide which implementation is being exercised.

### Acceptance gates before publishing

- Run the repository regressions and pyppbox adapter checks described below.
  Establish baseline results first and investigate new failures rather than
  weakening assertions to make the candidate pass.
- Exercise representative existing and newly supported real checkpoints with
  the same inputs, configuration, and device. Include detection, pose, and
  classifier/ReID paths, plus legacy/custom checkpoints when loading code changes.
- Compare the candidate with the previous fork for regressions and with the
  unmodified target upstream for intended upstream behavior. Record expected
  differences, numerical tolerances, and equal-cost assignment tie handling.
- Test all six trackers for continuity and unmatched/lost-track behavior. Exercise
  the actual affected backend/provider when changing exported inference or ReID;
  recognizing a suffix is not an execution test.
- Check missing optional dependencies, installation opt-in, OpenCV thread
  preservation, core requirement metadata, and runtime resource completeness.
- Build wheel and source packages, rebuild from the source archive, and run the
  wheel outside the checkout. Confirm the imported package path so an installed
  or checked-out copy cannot silently replace the artifact under test.
- Document untested model/device/platform combinations. Do not publish a change
  as verified for a backend that could not be exercised.

The current workflows build and publish packages; they do not enforce these
regressions as a publication gate. Run and record the checks manually until CI
implements them. A successful package build alone is not sync acceptance.
Update the recorded baseline and this guide only after the applicable checks pass.

## Verification

Run the repository regression suite from the checkout:

```sh
python -m unittest discover -s tests -p test_assignment.py -v
```

This suite checks assignment invariants; lazy imports and custom task maps;
normal `.pt` round trips for locally constructed YOLOv8 detection,
pose, and classification models; CPU prediction, embeddings, and tracking; all
six trackers with synthetic detections/native ReID; format recognition and error
paths; actual TorchScript inference/ReID; dependency absence; installation opt-in;
and OpenCV thread preservation.

Restricted `.pt` loading has a separate capability-gated test. It runs only when
`_SafeLoad.SUPPORTED` is true (Torch 2.6+), verifies that the real loader registers
checkpoint globals and passes `weights_only=True`, and checks the reconstructed
model weights under the import boundary. Older Torch versions, including 2.5.1,
skip this test; their standard-loading fallback does not establish restricted
loading coverage. Record the Torch version and skipped checks in validation
results, and run the test on a supported version before claiming that restricted
loading has been verified.

Also run pyppbox's `tests/integration/test_yolo_results.py` against this fork. Its
CPU/NumPy/CUDA `Results` adapter checks verify result handling, not GPU model
inference. Verify package builds and run inference/tracking from the built wheel
with optional dependencies unavailable.

For changes to model classes, aliases, transforms, or backend helpers, add
representative real pretrained/legacy/custom checkpoint and hardware-backend
comparisons. Locally generated checkpoints and a small TorchScript encoder do
not prove compatibility with every model generation, NAS/SAM execution, exported
framework, video source, GPU provider, or operating system. Format recognition
is not backend execution coverage.
