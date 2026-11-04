# Ultralytics YOLO on Axelera Voyager SDK

This document explains how to build and run complete Ultralytics YOLO inference
pipelines on Axelera Metis devices using the Axelera runtime.

The typical workflow has two phases:

1. **Model preparation.** You use Ultralytics, PyTorch, and the Voyager SDK
   compiler to train, export, and compile your model to `.axm` format.
2. **Application development.** You use `axelera-rt` to build and run an
   end-to-end video pipeline. `axelera-rt` is a lightweight, self-contained
   library with minimal package dependencies. It lets you describe pipelines
   that read frames from a camera, preprocess them, run model inference, and
   postprocess the results. The runtime can also fuse pipeline stages together
   automatically to minimize computation and data transfers.

A pipeline looks like this:

```python
pipeline = op.seq(
    op.color_convert("RGB", src="BGR"),  # OpenCV reads BGR; models expect RGB
    op.letterbox(640, 640),
    op.to_tensor(),
    op.load("yolo26n-pose.axm"),
    ConfidenceFilter(threshold=0.25),  # custom operator — see below
    op.to_image_space(keypoint_cols=range(6, 57, 3)),
).optimized()  # runtime fuses ops for maximum throughput

poses = pipeline(frame)  # frame in, raw (N, 57) NumPy array out — drops straight into existing post-processing
```

## Pose and Tracking Example

[`yolo26-pose-tracker.py`](./yolo26-pose-tracker.py) uses OpenCV for capture,
drawing, and output. The model and optional tracker run through the Axelera
pipeline. It uses a YOLO26 `nms=False` (NMS-free) pose export.

| Mode | Pipeline output | Capture / render |
| --- | --- | --- |
| `--tracker none` | Raw NumPy pose rows | OpenCV capture and manual drawing |
| `--tracker tracktrack` (default) | `TrackedObject` objects | OpenCV capture and manual drawing |

The tracking path adds `op.ax_pose()` before `op.tracker()` to convert raw poses
into the typed objects required by the tracker. `--tracker none` skips both stages.
The script runs without the `ultralytics` package once the model is compiled.

## Quick Start

### Install

Install the Axelera runtime explicitly before running the example. The version
below matches `AXELERA_SDK` in this fork's
[Axelera helper](../../ultralytics/utils/export/axelera.py):

```bash
python -m pip install axelera-rt==1.9.0 --no-cache-dir --extra-index-url https://software.axelera.ai/artifactory/api/pypi/axelera-pypi/simple
```

Model preparation also needs the Voyager compiler and its export dependencies.
Install the compiler explicitly if it is not already available:

```bash
python -m pip install axelera-devkit==1.9.0 --extra-index-url https://software.axelera.ai/artifactory/api/pypi/axelera-pypi/simple
```

See the official [Axelera integration guide](https://docs.ultralytics.com/integrations/axelera)
for platform, driver, and SDK setup. This fork disables dependency auto-install
by default, so install any missing export or inference dependencies manually.

Use NumPy and the OpenCV build provided by pyppbox or your environment. Showing
a window requires OpenCV GUI support. Model preparation also needs your chosen
PyTorch and torchvision builds; the standalone inference script does not import
them.

### Compile

Export and compile your trained model directly to Axelera format using the
Ultralytics CLI:

```bash
yolo export model=your-model.pt format=axelera
```

To prepare the pose model for this example's fixed 640-pixel preprocessing:

```bash
yolo export model=yolo26n-pose.pt format=axelera imgsz=640 nms=False
```

The compiled model is saved to `yolo26n-pose_axelera_model/`. Pass the `.axm`
file inside that directory to `--model`.

> [!NOTE]
> Each model directory also contains `metadata.yaml` with the model's
> class names and configuration. You can load this info directly to avoid manual
> label entry in your own application.

> [!IMPORTANT]
> Re-export any `.axm` you compiled with Voyager SDK 1.7 or earlier. 1.8 raised the
> compiled model format, and older files are rejected at load time with
> `Unsupported model version: 4.0, expected at least 5.0`. A 1.8 `.axm` loads on 1.9
> unchanged.

### Run

#### Pose Estimation (Ultralytics YOLO26)

```bash
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source 0 --tracker none         # pose only # webcam
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source image.jpg --tracker none # pose only # image
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source video.mp4 --tracker none # pose only # video
```

#### Pose Tracking (Ultralytics YOLO26 + TrackTrack)

```bash
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source video.mp4              # video with tracking
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source 0 --tracker tracktrack # webcam with tracking
```

#### Headless Output

```bash
python yolo26-pose-tracker.py --model yolo26n-pose.axm --source video.mp4 --no-display --output tracked.mp4
```

`--no-display` writes annotated frames to `--output`. With the default GUI mode,
frames appear in an OpenCV window and `--output` is unused. Press `q`, `Q`, or
Escape to stop the GUI run.

### Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--model` | _required_ | Path to the compiled `.axm` pose model. |
| `--source` | `0` | Image path, video path, or webcam index. |
| `--conf` | `0.25` | Confidence threshold. |
| `--tracker` | `tracktrack` | `bytetrack`, `oc-sort`, `sort`, `tracktrack`, or `none`. |
| `--no-display` | _off_ | Disable the GUI and save annotated frames to `--output`. |
| `--output` | `output.mp4` | Output video path used when `--no-display` is set. |

## What You'll See in the Code

### Custom Operators

The pipeline is fully composable — drop in your own operators anywhere in the
sequence. Just subclass `op.Operator` and implement `__call__`:

```python
class ConfidenceFilter(op.Operator):
    threshold: float = 0.25

    def __call__(self, x):
        """Filter detections by confidence score."""
        # Each operator receives the output of the previous one in op.seq().
        # Here x is the output of the pose detection model — an array of
        # shape (batch, num_detections, num_values) where each row holds
        # [bbox, confidence, class_id, keypoints…]. Column 4 is the
        # confidence score. Squeeze the batch dim and filter by score.
        if x.ndim == 3:
            x = x[0]
        return x[x[:, 4] >= self.threshold]
```

This means they are fused, scheduled, and optimized alongside built-in ops like
`op.letterbox` and the model itself — adding a custom filter carries no special
overhead.

### Capture, Drawing, and Output

The script reads frames with `cv2.VideoCapture`, runs `pipeline(frame)`, and draws
the returned poses with `draw_pose()` or `draw_tracked_poses()`. It displays frames
with `cv2.imshow()` in GUI mode and writes them with `cv2.VideoWriter` in headless
mode. Capture and rendering stay in OpenCV for both pose-only and tracking runs.

### Multi-Object Tracking

Adding tracking to a detection or pose pipeline is essentially a single line via
`op.tracker()`. The tracker works on typed objects, so the pipeline must produce
them (via `op.ax_pose()` / `op.ax_detection()`) before tracking:

```python
pipeline = op.seq(
    # ... your detection or pose pipeline ...
    op.ax_pose(num_keypoints=17, class_id_type=op.CocoClasses),  # raw rows -> list[PoseObject]
    op.tracker(algo="tracktrack"),  # list[PoseObject] -> list[TrackedObject]
)
```

`tracktrack` is the default. Pass `--tracker` to select another algorithm:

| Algorithm  | Key Strength                                         | Reference                |
| ---------- | ---------------------------------------------------- | ------------------------ |
| TrackTrack | Iterative matching with track-aware NMS (SOTA)       | CVPR 2025                |
| ByteTrack  | Handles low-confidence detections via dual threshold | Zhang et al., ECCV 2022  |
| OC-SORT    | Observation-centric re-update + virtual trajectory   | Cao et al., CVPR 2023    |
| SORT       | Simple, fast IoU-only baseline                       | Bewley et al., ICIP 2016 |

The tracker operates on bounding boxes, but the original detection (with all its
metadata) is preserved — use `tracked.tracked` on each result to access the
original keypoints, masks, or other model outputs. You'll see this pattern in
`yolo26-pose-tracker.py`.

## Learn More

The [Voyager SDK](https://github.com/axelera-ai-hub/voyager-sdk) has everything
beyond these introductory examples: advanced pipeline patterns, ReID and
appearance-based tracking, the high-performance display system, production-ready
application templates, and the full API reference.

Questions or feedback? Join the
[Axelera community](https://community.axelera.ai/).
