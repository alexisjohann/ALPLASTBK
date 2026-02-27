"""
GPM 1.0: Goalkeeper Performance Model

Multi-dimensional framework for systematic evaluation of goalkeeper
techniques and training time allocation.

SSOT: model-definition.yaml
"""

try:
    from .gpm_model import (
        GoalkeeperPerformanceModel,
        GoalkeeperProfile,
        PerformanceLevel,
        TechniqueDimensions,
    )
except ImportError:
    from gpm_model import (
        GoalkeeperPerformanceModel,
        GoalkeeperProfile,
        PerformanceLevel,
        TechniqueDimensions,
    )

__version__ = "1.0.0"
__all__ = [
    "GoalkeeperPerformanceModel",
    "GoalkeeperProfile",
    "PerformanceLevel",
    "TechniqueDimensions",
]
