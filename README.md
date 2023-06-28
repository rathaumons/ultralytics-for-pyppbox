[![Auto Build Wheels](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml/badge.svg)](https://github.com/rathaumons/ultralytics-for-pyppbox/actions/workflows/autobuild.yaml)

# Customized Ultralytics for [`pyppbox`](https://github.com/rathaumons/pyppbox)

* Updated: **June 28, 2023**
* Synced with: v8.0.124 [17e1392](https://github.com/ultralytics/ultralytics/commit/17e139220bf7988cf89d547f00f715989c79eefe)
* What cutomized: 
    - Enable OpenCV multithreading
    - Remove restrictions on customized OpenCV
    - Disable dependency auto-install
    - Disable auto update

## Installation

* Download and install the latest `.whl` on [`GitHub release`](https://github.com/rathaumons/ultralytics-for-pyppbox/releases)

* Or install from PyPI: 
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
