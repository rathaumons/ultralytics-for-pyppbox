# Ultralytics YOLO 🚀, AGPL-3.0 license

import subprocess
from pathlib import Path

import pytest

from ultralytics.utils import ONLINE, ROOT, SETTINGS

WEIGHT_DIR = Path(SETTINGS['weights_dir'])
TASK_ARGS = [
    ('detect', 'yolov8n', 'coco8.yaml'),
    ('segment', 'yolov8n-seg', 'coco8-seg.yaml'),
    ('classify', 'yolov8n-cls', 'imagenet10'),
    ('pose', 'yolov8n-pose', 'coco8-pose.yaml'), ]  # (task, model, data)
EXPORT_ARGS = [
    ('yolov8n', 'torchscript'),
    ('yolov8n-seg', 'torchscript'),
    ('yolov8n-cls', 'torchscript'),
    ('yolov8n-pose', 'torchscript'), ]  # (model, format)


def run(cmd):
    # Run a subprocess command with check=True
    subprocess.run(cmd.split(), check=True)


def test_special_modes():
    run('yolo help')
    run('yolo checks')
    run('yolo version')
    run('yolo settings reset')
    run('yolo copy-cfg')
    run('yolo cfg')


@pytest.mark.parametrize('task,model,data', TASK_ARGS)
def test_train(task, model, data):
    run(f'yolo train {task} model={model}.yaml data={data} imgsz=32 epochs=1 cache=disk')


@pytest.mark.parametrize('task,model,data', TASK_ARGS)
def test_val(task, model, data):
    run(f'yolo val {task} model={WEIGHT_DIR / model}.pt data={data} imgsz=32')


@pytest.mark.parametrize('task,model,data', TASK_ARGS)
def test_predict(task, model, data):
    run(f"yolo predict model={WEIGHT_DIR / model}.pt source={ROOT / 'assets'} imgsz=32 save save_crop save_txt")


@pytest.mark.skipif(not ONLINE, reason='environment is offline')
@pytest.mark.parametrize('task,model,data', TASK_ARGS)
def test_predict_online(task, model, data):
    mode = 'track' if task in ('detect', 'segment', 'pose') else 'predict'  # mode for video inference
    model = WEIGHT_DIR / model
    run(f'yolo predict model={model}.pt source=https://ultralytics.com/images/bus.jpg imgsz=32')
    run(f'yolo {mode} model={model}.pt source=https://ultralytics.com/assets/decelera_landscape_min.mov imgsz=96')

    # Run Python YouTube tracking because CLI is broken. TODO: fix CLI YouTube
    # run(f'yolo {mode} model={model}.pt source=https://youtu.be/G17sBkb38XQ imgsz=32 tracker=bytetrack.yaml')


@pytest.mark.parametrize('model,format', EXPORT_ARGS)
def test_export(model, format):
    run(f'yolo export model={WEIGHT_DIR / model}.pt format={format} imgsz=32')


# Test SAM, RTDETR Models
def test_rtdetr(task='detect', model='yolov8n-rtdetr.yaml', data='coco8.yaml'):
    # Warning: MUST use imgsz=640
    run(f'yolo train {task} model={model} data={data} imgsz=640 epochs=1 cache=disk')
    run(f'yolo val {task} model={model} data={data} imgsz=640')
    run(f"yolo predict {task} model={model} source={ROOT / 'assets/bus.jpg'} imgsz=640 save save_crop save_txt")


def test_fastsam(task='segment', model=WEIGHT_DIR / 'FastSAM-s.pt', data='coco8-seg.yaml'):
    source = ROOT / 'assets/bus.jpg'

    run(f'yolo segment val {task} model={model} data={data} imgsz=32')
    run(f'yolo segment predict model={model} source={source} imgsz=32 save save_crop save_txt')

    from ultralytics import FastSAM
    from ultralytics.models.fastsam import FastSAMPrompt

    # Create a FastSAM model
    sam_model = FastSAM(model)  # or FastSAM-x.pt

    # Run inference on an image
    everything_results = sam_model(source, device='cpu', retina_masks=True, imgsz=1024, conf=0.4, iou=0.9)

    # Everything prompt
    prompt_process = FastSAMPrompt(source, everything_results, device='cpu')
    ann = prompt_process.everything_prompt()

    # Bbox default shape [0,0,0,0] -> [x1,y1,x2,y2]
    ann = prompt_process.box_prompt(bbox=[200, 200, 300, 300])

    # Text prompt
    ann = prompt_process.text_prompt(text='a photo of a dog')

    # Point prompt
    # points default [[0,0]] [[x1,y1],[x2,y2]]
    # point_label default [0] [1,0] 0:background, 1:foreground
    ann = prompt_process.point_prompt(points=[[200, 200]], pointlabel=[1])
    prompt_process.plot(annotations=ann, output='./')


def test_mobilesam():
    from ultralytics import SAM

    # Load the model
    model = SAM(WEIGHT_DIR / 'mobile_sam.pt')

    # Source
    source = ROOT / 'assets/zidane.jpg'

    # Predict a segment based on a point prompt
    model.predict(source, points=[900, 370], labels=[1])

    # Predict a segment based on a box prompt
    model.predict(source, bboxes=[439, 437, 524, 709])

    # Predict all
    # model(source)


# Slow Tests
@pytest.mark.slow
@pytest.mark.parametrize('task,model,data', TASK_ARGS)
def test_train_gpu(task, model, data):
    run(f'yolo train {task} model={model}.yaml data={data} imgsz=32 epochs=1 device="0"')  # single GPU
    run(f'yolo train {task} model={model}.pt data={data} imgsz=32 epochs=1 device="0,1"')  # Multi GPU
