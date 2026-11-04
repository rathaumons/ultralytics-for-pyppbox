[![Test Build](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml/badge.svg?branch=main)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/test_build.yaml) [![Publish on PyPI](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/publish.yaml/badge.svg?branch=main)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/publish.yaml)

# Customized Ultralytics for pyppbox

* Updated: **November 4, 2026**
* Synced with: v8.4.202 -> [[ae725d5]](https://github.com/ultralytics/ultralytics/commit/ae725d5cb20c2d849b864cd34fc15f5c55f877a5)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* Customized for [`pyppbox`](https://github.com/rathaumons/pyppbox) -> [SCOPE.md](https://github.com/rathaumons/ultralytics-for-pyppbox/blob/main/SCOPE.md)

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
