[![Test Build](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml) [![Build PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for pyppbox

* Updated: **April 13, 2024**
* Synced with: v8.1.47 -> [[42416bc]](https://github.com/ultralytics/ultralytics/commit/42416bc608b49cbdcb091e81adbb4caaf11eac38)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* Customized for [`pyppbox`](https://github.com/rathaumons/pyppbox):
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

    <details><summary><ins>Click here to expand!</ins></summary>
    
    ```
    git clone https://github.com/rathaumons/ultralytics-for-pyppbox.git
    cd ultralytics-for-pyppbox
    python -m pip install --upgrade pip
    python -m pip install -U pip setuptools
    pip install wheel build
    python -m build --wheel --skip-dependency-check --no-isolatio
    cd dist
    ```
    
    </details>
