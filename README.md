[![Test Build](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml/badge.svg?branch=main)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml) [![Publish on PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/publish.yaml/badge.svg?branch=main)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/publish.yaml)

# Customized Ultralytics for pyppbox

* Updated: **September 8, 2026**
* Synced with: v8.4.144 -> [[1ba77f6]](https://github.com/ultralytics/ultralytics/commit/1ba77f668344711bf1c8859fe318ce2cda81757d)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* Customized for [`pyppbox`](https://github.com/rathaumons/pyppbox):
    - Enable OpenCV multithreading
    - Remove restrictions on customized OpenCV
    - Remove unnecessary dependencies
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
