# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model import YOLO, YOLOE, YOLOWorld  # noqa: F401
    from . import classify, depth, detect, obb, pose, segment, semantic, world, yoloe  # noqa: F401

_EXPORTS = {
    "YOLO": "model",
    "YOLOE": "model",
    "YOLOWorld": "model",
    "classify": None,
    "depth": None,
    "detect": None,
    "obb": None,
    "pose": None,
    "segment": None,
    "semantic": None,
    "world": None,
    "yoloe": None,
}

__all__ = tuple(_EXPORTS)


def __getattr__(name):
    """Import public models and task components only when requested."""
    if name in _EXPORTS:
        module = _EXPORTS[name]
        value = import_module(f"{__name__}.{module or name}")
        if module is not None:
            value = getattr(value, name)
    elif name in _EXPORTS.values():
        value = import_module(f"{__name__}.{name}")
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
    globals()[name] = value
    return value


def __dir__():
    """Include lazy public exports in interactive completion."""
    return sorted(set(globals()) | set(__all__) | {module for module in _EXPORTS.values() if module})
