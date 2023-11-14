[![Build PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for [`pyppbox`](https://github.com/rathaumons/pyppbox)

* Updated: **November 14, 2023**
* Synced with: v8.0.209 -> [[9a58914]](https://github.com/ultralytics/ultralytics/commit/9a5891444ebd374b1aba4aa147c1f9e11a1db5d2)
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
