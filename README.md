[![Test Build](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml) [![Build PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for pyppbox

* Updated: **April 30, 2024**
* Synced with: v8.1.48 -> [[c54b013]](https://github.com/ultralytics/ultralytics/commit/c54b013188870dafdd5ce0d78b3f5f3fdee655fd)
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
