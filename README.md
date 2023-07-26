[![Auto Build Wheels](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for [`pyppbox`](https://github.com/rathaumons/pyppbox)

* Updated: **July 26, 2023**
* Synced with: v8.0.142 -> [[9627323]](https://github.com/ultralytics/ultralytics/commit/9627323d7cb5e8107e7a471f87d471108b263451) + [[3c787eb]](3c787eb0806bab79dda88f0be9a476666118b52f)
* All credit and info -> [[Original Ultralytics repo]](https://github.com/ultralytics/ultralytics)
* What customized:
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
  
