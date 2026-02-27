#!/usr/bin/env python3
"""
Strategy Model Base Module (SMB-1.0)
Common functionality for all strategic models.

This module provides:
- Base classes for strategic models
- Common configuration loading/validation
- Standard output formatting
- Shared utilities (currency, dates, calculations)
- Model registry integration

Usage:
    from strategy_base import StrategyModel, load_config, format_currency

Model Version: 1.0.0
Implementation Date: 2026-01-16
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Union, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import yaml
import sys


# =============================================================================
# CONSTANTS
# =============================================================================

DEFAULT_BASE_YEAR = 2024
DEFAULT_PROJECTION_YEARS = 11
DEFAULT_CURRENCY = "EUR"

# Model Registry IDs
MODEL_IDS = {
    'RPM': 'RPM-1.0',   # Revenue Projection Model
    'MCSM': 'MCSM-1.0', # Monte Carlo Simulation Model
    'OSM': 'OSM-1.0',   # Organizational Scaling Model
    'CAM': 'CAM-1.0',   # Capital Expenditure Allocation Model
    'CSM': 'CSM-1.0',   # Cost Structure Model
    'PLM': 'PLM-1.0',   # Profit & Loss Model
    'SAM': 'SAM-1.0',   # Sensitivity Analysis Model
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ModelConfig:
    """Standard configuration for all models."""
    base_year: int = DEFAULT_BASE_YEAR
    projection_years: int = DEFAULT_PROJECTION_YEARS
    currency: str = DEFAULT_CURRENCY

    @property
    def years(self) -> np.ndarray:
        """Return array of projection years."""
        return np.arange(self.base_year, self.base_year + self.projection_years)

    @property
    def final_year(self) -> int:
        """Return final projection year."""
        return self.base_year + self.projection_years - 1


@dataclass
class ModelResult:
    """Standard result container for all models."""
    model_id: str
    model_name: str
    execution_time: float
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'model_id': self.model_id,
            'model_name': self.model_name,
            'execution_time_seconds': round(self.execution_time, 3),
            'success': self.success,
            'summary': self.summary,
            'errors': self.errors,
            'warnings': self.warnings
        }


# =============================================================================
# CONFIGURATION UTILITIES
# =============================================================================

def load_config(config_path: Union[str, Path]) -> Dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If YAML is invalid
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format in {config_path}: {e}")


def merge_configs(*configs: Dict) -> Dict:
    """
    Merge multiple configuration dictionaries.
    Later configs override earlier ones.

    Args:
        *configs: Configuration dictionaries to merge

    Returns:
        Merged configuration dictionary
    """
    result = {}
    for config in configs:
        if config:
            _deep_merge(result, config)
    return result


def _deep_merge(base: Dict, update: Dict) -> Dict:
    """Deep merge update into base dictionary."""
    for key, value in update.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def get_nested(config: Dict, path: str, default: Any = None) -> Any:
    """
    Get value from nested config using dot notation.

    Args:
        config: Configuration dictionary
        path: Dot-separated path (e.g., "section.subsection.key")
        default: Default value if path not found

    Returns:
        Value at path or default
    """
    keys = path.split('.')
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value


def set_nested(config: Dict, path: str, value: Any) -> Dict:
    """
    Set value in nested config using dot notation.

    Args:
        config: Configuration dictionary (modified in place)
        path: Dot-separated path
        value: Value to set

    Returns:
        Modified configuration
    """
    keys = path.split('.')
    current = config

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return config


def validate_config(config: Dict, required_fields: List[str]) -> List[str]:
    """
    Validate that required fields exist in config.

    Args:
        config: Configuration dictionary
        required_fields: List of required field paths (dot notation)

    Returns:
        List of missing field paths (empty if all present)
    """
    missing = []
    for field_path in required_fields:
        if get_nested(config, field_path) is None:
            missing.append(field_path)
    return missing


# =============================================================================
# OUTPUT UTILITIES
# =============================================================================

def save_csv(df: pd.DataFrame, filepath: Union[str, Path], verbose: bool = True) -> None:
    """Save DataFrame to CSV file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    if verbose:
        print(f"  Saved: {filepath}")


def save_yaml(data: Dict, filepath: Union[str, Path], verbose: bool = True) -> None:
    """Save dictionary to YAML file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    if verbose:
        print(f"  Saved: {filepath}")


def format_currency(value: float, currency: str = "EUR", decimals: int = 0) -> str:
    """
    Format value as currency string.

    Args:
        value: Numeric value
        currency: Currency code
        decimals: Decimal places

    Returns:
        Formatted string like "€1,234M" or "EUR 1,234M"
    """
    symbols = {'EUR': '€', 'USD': '$', 'GBP': '£', 'CHF': 'CHF '}
    symbol = symbols.get(currency, f"{currency} ")

    if abs(value) >= 1000:
        return f"{symbol}{value:,.{decimals}f}M"
    else:
        return f"{symbol}{value:,.{decimals}f}M"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format value as percentage string."""
    return f"{value:,.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """Format value as number with thousand separators."""
    return f"{value:,.{decimals}f}"


# =============================================================================
# CALCULATION UTILITIES
# =============================================================================

def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """
    Calculate Compound Annual Growth Rate.

    Args:
        start_value: Starting value
        end_value: Ending value
        years: Number of years

    Returns:
        CAGR as percentage (e.g., 5.0 for 5%)
    """
    if start_value <= 0 or end_value <= 0 or years <= 0:
        return 0.0
    return (pow(end_value / start_value, 1 / years) - 1) * 100


def project_with_cagr(
    base_value: float,
    cagr_percent: float,
    years: np.ndarray,
    base_year: int
) -> np.ndarray:
    """
    Project values using CAGR formula.

    Args:
        base_value: Starting value
        cagr_percent: CAGR as percentage
        years: Array of years
        base_year: Base year for calculation

    Returns:
        Array of projected values
    """
    cagr = cagr_percent / 100
    years_from_base = years - base_year
    return base_value * np.power(1 + cagr, years_from_base)


def project_with_escalation(
    base_value: float,
    escalation_percent: float,
    years: np.ndarray,
    base_year: int
) -> np.ndarray:
    """
    Project values with annual escalation (same as CAGR but semantically different).

    Args:
        base_value: Starting value
        escalation_percent: Annual escalation as percentage
        years: Array of years
        base_year: Base year for calculation

    Returns:
        Array of projected values
    """
    return project_with_cagr(base_value, escalation_percent, years, base_year)


def weighted_average(values: List[float], weights: List[float]) -> float:
    """Calculate weighted average."""
    if not values or not weights or len(values) != len(weights):
        return 0.0
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / total_weight


# =============================================================================
# TIME UTILITIES
# =============================================================================

def get_year_range(base_year: int, projection_years: int) -> np.ndarray:
    """Get array of years for projection."""
    return np.arange(base_year, base_year + projection_years)


def year_index(year: int, base_year: int) -> int:
    """Get index for a specific year (0-based from base year)."""
    return year - base_year


def years_between(start_year: int, end_year: int) -> int:
    """Get number of years between two years (inclusive)."""
    return end_year - start_year + 1


# =============================================================================
# BASE MODEL CLASS
# =============================================================================

class StrategyModel(ABC):
    """
    Abstract base class for all strategic models.

    Subclasses must implement:
    - model_id: Model identifier (e.g., "RPM-1.0")
    - model_name: Human-readable name
    - run(): Main execution method
    - _extract_params(): Extract parameters from config
    """

    def __init__(self, config: Dict, verbose: bool = True):
        """
        Initialize model with configuration.

        Args:
            config: Configuration dictionary
            verbose: Print progress messages
        """
        self.config = config
        self.verbose = verbose
        self.params = self._extract_params(config)
        self._start_time: Optional[float] = None
        self._warnings: List[str] = []
        self._errors: List[str] = []

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Return model identifier (e.g., 'RPM-1.0')."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return human-readable model name."""
        pass

    @abstractmethod
    def _extract_params(self, config: Dict) -> Dict:
        """Extract model-specific parameters from configuration."""
        pass

    @abstractmethod
    def run(self, **kwargs) -> ModelResult:
        """
        Run the model and return results.

        Returns:
            ModelResult with data, summary, and metadata
        """
        pass

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def warn(self, message: str) -> None:
        """Log a warning."""
        self._warnings.append(message)
        if self.verbose:
            print(f"  WARNING: {message}")

    def error(self, message: str) -> None:
        """Log an error."""
        self._errors.append(message)
        if self.verbose:
            print(f"  ERROR: {message}")

    def _start_timer(self) -> None:
        """Start execution timer."""
        import time
        self._start_time = time.time()

    def _get_elapsed_time(self) -> float:
        """Get elapsed time since timer start."""
        import time
        if self._start_time is None:
            return 0.0
        return time.time() - self._start_time

    def _create_result(
        self,
        success: bool,
        data: Dict[str, Any] = None,
        summary: Dict[str, Any] = None
    ) -> ModelResult:
        """Create standardized ModelResult."""
        return ModelResult(
            model_id=self.model_id,
            model_name=self.model_name,
            execution_time=self._get_elapsed_time(),
            success=success,
            data=data or {},
            summary=summary or {},
            errors=self._errors.copy(),
            warnings=self._warnings.copy()
        )

    def get_base_config(self) -> ModelConfig:
        """Get standard model configuration."""
        return ModelConfig(
            base_year=self.params.get('base_year', DEFAULT_BASE_YEAR),
            projection_years=self.params.get('projection_years', DEFAULT_PROJECTION_YEARS),
            currency=self.params.get('currency', DEFAULT_CURRENCY)
        )


# =============================================================================
# MODEL REGISTRY
# =============================================================================

class ModelRegistry:
    """
    Registry of available strategic models.

    Usage:
        registry = ModelRegistry()
        registry.register('RPM', RevenueProjectionModel)
        model = registry.create('RPM', config)
        result = model.run()
    """

    _models: Dict[str, type] = {}

    @classmethod
    def register(cls, model_id: str, model_class: type) -> None:
        """Register a model class."""
        cls._models[model_id] = model_class

    @classmethod
    def create(cls, model_id: str, config: Dict, **kwargs) -> StrategyModel:
        """Create a model instance."""
        if model_id not in cls._models:
            raise ValueError(f"Unknown model: {model_id}. Available: {list(cls._models.keys())}")
        return cls._models[model_id](config, **kwargs)

    @classmethod
    def list_models(cls) -> List[str]:
        """List registered model IDs."""
        return list(cls._models.keys())

    @classmethod
    def get_model_class(cls, model_id: str) -> type:
        """Get model class by ID."""
        return cls._models.get(model_id)


# =============================================================================
# RESULT FORMATTING
# =============================================================================

def format_model_header(model_name: str, width: int = 80) -> str:
    """Format model output header."""
    return f"\n{'='*width}\n{model_name}\n{'='*width}"


def format_section(title: str, width: int = 60) -> str:
    """Format section header."""
    return f"\n[{title}]\n{'-'*width}"


def format_key_value(key: str, value: Any, indent: int = 2) -> str:
    """Format key-value pair for display."""
    prefix = " " * indent
    return f"{prefix}{key}: {value}"


def format_summary_table(
    data: Dict[str, Any],
    title: str = "SUMMARY",
    currency: str = "EUR"
) -> str:
    """
    Format summary dictionary as readable table.

    Args:
        data: Summary data dictionary
        title: Table title
        currency: Currency for formatting

    Returns:
        Formatted string
    """
    lines = [format_section(title)]

    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"\n  {key.upper()}:")
            for sub_key, sub_value in value.items():
                formatted = _format_value(sub_value, sub_key, currency)
                lines.append(f"    {sub_key}: {formatted}")
        else:
            formatted = _format_value(value, key, currency)
            lines.append(f"  {key}: {formatted}")

    return "\n".join(lines)


def _format_value(value: Any, key: str, currency: str) -> str:
    """Auto-format value based on key name and type."""
    if value is None:
        return "N/A"

    key_lower = key.lower()

    # Currency values
    if any(x in key_lower for x in ['_m', '_eur', '_usd', 'revenue', 'cost', 'ebitda', 'income', 'budget', 'capex']):
        if isinstance(value, (int, float)):
            return format_currency(value, currency)

    # Percentage values
    if any(x in key_lower for x in ['percent', 'pct', 'margin', 'rate', 'cagr', 'growth', 'roi']):
        if isinstance(value, (int, float)):
            return format_percent(value)

    # Count values
    if any(x in key_lower for x in ['count', 'headcount', 'num', 'total']) and not any(x in key_lower for x in ['percent', 'pct']):
        if isinstance(value, (int, float)):
            return format_number(value)

    # Default formatting
    if isinstance(value, float):
        return f"{value:.2f}"

    return str(value)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    'DEFAULT_BASE_YEAR',
    'DEFAULT_PROJECTION_YEARS',
    'DEFAULT_CURRENCY',
    'MODEL_IDS',

    # Data classes
    'ModelConfig',
    'ModelResult',

    # Config utilities
    'load_config',
    'merge_configs',
    'get_nested',
    'set_nested',
    'validate_config',

    # Output utilities
    'save_csv',
    'save_yaml',
    'format_currency',
    'format_percent',
    'format_number',

    # Calculation utilities
    'calculate_cagr',
    'project_with_cagr',
    'project_with_escalation',
    'weighted_average',

    # Time utilities
    'get_year_range',
    'year_index',
    'years_between',

    # Base classes
    'StrategyModel',
    'ModelRegistry',

    # Formatting
    'format_model_header',
    'format_section',
    'format_key_value',
    'format_summary_table',
]
