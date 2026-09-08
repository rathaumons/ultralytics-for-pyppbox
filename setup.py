# Ultralytics YOLO 🚀, AGPL-3.0 license

from pathlib import Path
from setuptools import setup

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent # root directory
README = (PARENT / 'README.md').read_text(encoding='utf-8')


def get_version():
    """
    Retrieve the version number from the 'ultralytics/__init__.py' file.

    Returns:
        (str): The version number extracted from the '__version__' attribute in the 'ultralytics/__init__.py' file.
    """
    file = PARENT / 'ultralytics/__init__.py'
    with open(file) as version_file:
        for line in version_file.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError('[!] Unable to find version string.')


def parse_requirements(file_path: Path):
    """
    Parse a requirements.txt file, ignoring lines that start with '#' and any text after '#'.

    Args:
        file_path (str | Path): Path to the requirements.txt file.

    Returns:
        (List[str]): List of parsed requirements.
    """
    requirements = []
    for line in Path(file_path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line.split('#')[0].strip()) # ignore inline comments

    return requirements


setup(
    name='pyppbox-ultralytics', # name of pypi package
    version=get_version(), # version of pypi package
    python_requires='>=3.8',
    license='AGPL-3.0',
    description=('Ultralytics YOLO 🚀 for SOTA object detection, instance segmentation, semantic segmentation, depth estimation, classification, pose estimation, oriented object detection, and multi-object tracking.'),
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/rathaumons/ultralytics-for-pyppbox',
    project_urls={'Bug Reports': 'https://github.com/rathaumons/ultralytics-for-pyppbox/issues',
                  'Source': 'https://github.com/rathaumons/ultralytics-for-pyppbox'},
    packages=['ultralytics'] + [str(x) for x in Path('ultralytics').rglob('*/') if x.is_dir() and '__' not in str(x)],
    package_data={'ultralytics': ['**/*.yaml', '**/*.sh', '../tests/*.py'], 'ultralytics.assets': ['*.jpg'], 'ultralytics.solutions.templates': ['*.html']},
    include_package_data=True,
    install_requires=parse_requirements(PARENT / 'requirements.txt'),
    extras_require={
        'export': [
            "onnx>=1.12.0; platform_system != 'Darwin'", # ONNX export
            "onnx>=1.12.0,<1.18.0; platform_system == 'Darwin' and python_version < '3.13'",  # TF inference hanging on MacOS (tested up to onnx==1.20.0)
            "onnx>=1.20.0; platform_system == 'Darwin' and python_version >= '3.13'",
            "onnxslim>=0.1.82",
            # ONNX export validation and inference. Jetson jobs provide custom aarch64 onnxruntime-gpu wheels.
            "onnxruntime<1.20.0; python_version < '3.11' and (platform_machine != 'aarch64' or platform_system != 'Linux')",
            "onnxruntime>=1.20.0; python_version >= '3.11'",
            # Raspberry Pi Python 3.11 ExecuTorch inference requires the last known-good Linux ARM64 Torch 2.12 stack.
            "torch>=2.12.0,<2.13.0; platform_system == 'Linux' and platform_machine == 'aarch64' and python_version == '3.11'",
        ],
        'extra': [
            "ipython", # interactive notebook
            "albumentations>=1.4.6", # training augmentations
            "faster-coco-eval>=1.6.7", # COCO mAP
        ],
        'solutions': [
            "shapely>=2.0.0",  # shapely for point and polygon data matching
            "lapx>=0.10.0",  # for solution tracking linear assignment
            # CLIP for similarity search auto-installs on first use via ultralytics.nn.text_model (https://github.com/ultralytics/CLIP)
            "streamlit>=1.51.0; python_version >= '3.10'",  # for live inference on web browser, i.e `yolo streamlit-predict`
            "streamlit>=1.29.0,<1.51.0; python_version < '3.10' and (platform_machine != 'aarch64' or platform_system != 'Linux')",
            "flask>=3.0.1",  # for similarity search solution
        ],
        'logging': [
            "wandb",  # https://docs.ultralytics.com/integrations/weights-biases
            "tensorboard",  # https://docs.ultralytics.com/integrations/tensorboard
            "mlflow",  # https://docs.ultralytics.com/integrations/mlflow
        ],
        'typing': [
            "types-pillow",
            "types-psutil",
            "types-pyyaml",
            "types-requests",
            "types-shapely",
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows', ],
    keywords="machine-learning, deep-learning, computer-vision, ML, DL, AI, RT-DETR, SAM3, YOLO, YOLOv3, YOLOv5, YOLOv8, YOLO11, YOLO26, Platform, Ultralytics",
    entry_points={'console_scripts': ['yolo = ultralytics.cfg:entrypoint', 'ultralytics = ultralytics.cfg:entrypoint']}
)
