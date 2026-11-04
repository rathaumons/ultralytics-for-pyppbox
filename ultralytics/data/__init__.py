# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import BaseDataset
    from .build import build_dataloader, build_grounding, build_yolo_dataset, load_inference_source
    from .dataset import (
        ClassificationDataset,
        GroundingDataset,
        PolygonSemanticDataset,
        SemanticDataset,
        YOLOConcatDataset,
        YOLODataset,
        YOLOMultiModalDataset,
    )

__all__ = (
    "BaseDataset",
    "ClassificationDataset",
    "GroundingDataset",
    "PolygonSemanticDataset",
    "SemanticDataset",
    "YOLOConcatDataset",
    "YOLODataset",
    "YOLOMultiModalDataset",
    "build_dataloader",
    "build_grounding",
    "build_yolo_dataset",
    "load_inference_source",
)


def __getattr__(name: str):
    """Load dataset classes and builders only when requested."""
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = "base" if name == "BaseDataset" else "build" if name[0].islower() else "dataset"
    value = getattr(import_module(f"{__name__}.{module}"), name)
    globals()[name] = value
    return value


def __dir__():
    """Include lazily available public names in module introspection."""
    return sorted(set(globals()) | set(__all__))
