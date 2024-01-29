[![Build PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for [`pyppbox`](https://github.com/rathaumons/pyppbox)

* Updated: **January 29, 2024**
* Synced with: v8.1.7 -> [[18d7ab0]](https://github.com/ultralytics/ultralytics/commit/18d7ab06ddcacdbde48900f5740d65223eafbf49)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* What customized:
    - Enable OpenCV multithreading
    - Remove restrictions on customized OpenCV
    - Disable dependency auto-install
    - Disable auto update

## Installation

* Install from [PyPI](https://pypi.org/project/pyppbox-ultralytics/):
    ```
    pip install pyppbox-ultralytics
    ``` 
* Or install from GitHub directly:
    ```
    pip install git+https://github.com/rathaumons/ultralytics-for-pyppbox.git
    ```
* Or build from source:
    ```
    git clone https://github.com/rathaumons/ultralytics-for-pyppbox.git
    cd ultralytics-for-pyppbox
    python -m pip install --upgrade pip
    pip install "setuptools>=67.2.0"
    pip install -r requirements.txt
    pip install wheel build
    python -m build --wheel --skip-dependency-check --no-isolatio
    cd dist
    ```
