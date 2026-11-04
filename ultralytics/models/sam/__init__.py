# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model import SAM  # noqa: F401
    from .predict import (
        Predictor,
        SAM2DynamicInteractivePredictor,
        SAM2Predictor,
        SAM2VideoPredictor,
        SAM3Predictor,
        SAM3SemanticPredictor,
        SAM3VideoPredictor,
        SAM3VideoSemanticPredictor,
    )  # noqa: F401

_EXPORTS = {
    "SAM": "model",
    "Predictor": "predict",
    "SAM2DynamicInteractivePredictor": "predict",
    "SAM2Predictor": "predict",
    "SAM2VideoPredictor": "predict",
    "SAM3Predictor": "predict",
    "SAM3SemanticPredictor": "predict",
    "SAM3VideoPredictor": "predict",
    "SAM3VideoSemanticPredictor": "predict",
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
