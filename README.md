[![Auto Build Wheels](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for [`pyppbox`](https://github.com/rathaumons/pyppbox)

* Updated: **July 11, 2023**
* Synced with: v8.0.132 -> [[495edc2]](https://github.com/ultralytics/ultralytics/commit/495edc261f4769ed31b118eafd8cdc23da2935fd) + [[82920ef]](https://github.com/ultralytics/ultralytics/commit/82920ef7ec4c529439c68a4aecc5c7935ecdecc1) + [[48d7dbd]](https://github.com/ultralytics/ultralytics/commit/48d7dbdbf949da70162610b71af049c7926b4963)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* What cutomized:
    - Enable OpenCV multithreading
    - Remove restrictions on customized OpenCV
    - Disable dependency auto-install
    - Disable auto update

## Installation

* Install from PyPI: 
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
    pip install wheel build
    python -m build --wheel --skip-dependency-check --no-isolation
    cd dist
    ```
  
