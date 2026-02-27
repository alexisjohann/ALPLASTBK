"""
EBF Model Registry: Database Manager
=====================================
Single Source of Truth for all behavioral and institutional models.

This module provides:
1. Schema validation
2. Model CRUD operations
3. Registry queries
4. Consistency checking
5. Reporting

Single Source of Truth Location: models/models.registry.yaml
Schema Definition: models/models.schema.yaml
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import json


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ModelStatus(Enum):
    """Allowed model statuses"""
    STABLE = "STABLE"
    BETA = "BETA"
    EXPERIMENTAL = "EXPERIMENTAL"
    PLANNED = "PLANNED"


class ModelCategory(Enum):
    """Model categories"""
    SUCCESSION = "SUCCESSION"
    COMPLIANCE = "COMPLIANCE"
    BEHAVIORAL = "BEHAVIORAL"
    SOCIAL = "SOCIAL"
    OTHER = "OTHER"


class ValidationConfidence(Enum):
    """Confidence levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ============================================================================
# DATA CLASSES: Match schema entities
# ============================================================================

@dataclass
class Dimension:
    """A model dimension"""
    symbol: str
    name: str
    description: str
    weight: float
    beta_coefficient: Optional[float] = None
    range_min: float = 0.0
    range_max: float = 1.0

    def validate(self) -> bool:
        """Validate dimension"""
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Weight must be 0-1, got {self.weight}")
        if self.beta_coefficient is not None and self.beta_coefficient == 0:
            raise ValueError(f"Beta coefficient cannot be zero")
        return True


@dataclass
class ValidationMetrics:
    """Validation performance metrics"""
    accuracy: float
    confidence: ValidationConfidence
    data_points: int
    rmse: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None

    def validate(self) -> bool:
        """Validate metrics"""
        if not (0.0 <= self.accuracy <= 1.0):
            raise ValueError(f"Accuracy must be 0-1, got {self.accuracy}")
        if self.data_points < 1:
            raise ValueError(f"Must have ≥1 data points")
        return True


@dataclass
class ModelRecord:
    """Complete model registry record"""
    model_id: str
    short_name: str
    category: ModelCategory
    status: ModelStatus
    version: str
    created: datetime
    last_updated: datetime
    maintainer: str
    description: Optional[str] = None
    dimensions: Optional[List[Dimension]] = None
    validation: Optional[ValidationMetrics] = None
    documentation_url: Optional[str] = None

    def validate(self) -> bool:
        """Validate model record"""
        # Check required fields
        if not self.model_id or not self.short_name:
            raise ValueError("model_id and short_name required")

        # Validate dimensions if present
        if self.dimensions:
            for dim in self.dimensions:
                dim.validate()

            # Check dimension weights sum to ~1.0
            total_weight = sum(d.weight for d in self.dimensions)
            if not (0.95 <= total_weight <= 1.05):
                raise ValueError(
                    f"Dimension weights must sum to ~1.0, got {total_weight}"
                )

        # Validate validation metrics if present
        if self.validation:
            self.validation.validate()

        return True


# ============================================================================
# REGISTRY: Main database class
# ============================================================================

class ModelRegistry:
    """Central model registry - Single Source of Truth"""

    def __init__(self, registry_path: str = "models/models.registry.yaml",
                 schema_path: str = "models/models.schema.yaml"):
        """
        Initialize registry

        Args:
            registry_path: Path to registry file (data)
            schema_path: Path to schema file (definition)
        """
        self.registry_path = Path(registry_path)
        self.schema_path = Path(schema_path)

        self.models: Dict[str, ModelRecord] = {}
        self.schema: Dict = {}

        # Load files
        self._load_schema()
        self._load_registry()

    def _load_schema(self):
        """Load schema definition"""
        if self.schema_path.exists():
            with open(self.schema_path, 'r') as f:
                self.schema = yaml.safe_load(f)
            print(f"✓ Schema loaded from {self.schema_path}")
        else:
            print(f"⚠ Schema file not found: {self.schema_path}")

    def _load_registry(self):
        """Load registry data"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)

            # Parse models from registry file
            if data and 'models' in data:
                for model_data in data['models']:
                    model = self._parse_model_record(model_data)
                    self.models[model.model_id] = model

            print(f"✓ Registry loaded: {len(self.models)} models")
        else:
            print(f"⚠ Registry file not found: {self.registry_path}")

    def _parse_model_record(self, model_data: Dict) -> ModelRecord:
        """Parse model data from YAML into ModelRecord"""
        # Parse enums
        category = ModelCategory[model_data['category']]
        status = ModelStatus[model_data['status']]

        # Parse dates
        created = datetime.fromisoformat(model_data['created'])
        last_updated = datetime.fromisoformat(model_data['last_updated'])

        # Parse dimensions if present
        dimensions = None
        if 'dimensions' in model_data:
            dimensions = [
                Dimension(
                    symbol=d['symbol'],
                    name=d['name'],
                    description=d.get('description', ''),
                    weight=d['weight'],
                    beta_coefficient=d.get('beta_coefficient'),
                    range_min=d.get('range', [0, 1])[0],
                    range_max=d.get('range', [0, 1])[1]
                )
                for d in model_data['dimensions']
            ]

        # Parse validation if present
        validation = None
        if 'validation' in model_data and model_data['validation']:
            val = model_data['validation']
            validation = ValidationMetrics(
                accuracy=val['accuracy'],
                confidence=ValidationConfidence[val['confidence']],
                data_points=val['data_points'],
                rmse=val.get('rmse'),
                precision=val.get('precision'),
                recall=val.get('recall')
            )

        return ModelRecord(
            model_id=model_data['model_id'],
            short_name=model_data['short_name'],
            category=category,
            status=status,
            version=model_data['version'],
            created=created,
            last_updated=last_updated,
            maintainer=model_data['maintainer'],
            description=model_data.get('description'),
            dimensions=dimensions,
            validation=validation,
            documentation_url=model_data.get('documentation_url')
        )

    def save_registry(self):
        """Save registry to YAML file"""
        data = {
            'metadata': {
                'version': '1.0',
                'updated': datetime.now().isoformat(),
                'total_models': len(self.models)
            },
            'models': []
        }

        # Convert models back to dict format
        for model_id, model in self.models.items():
            model_dict = {
                'model_id': model.model_id,
                'short_name': model.short_name,
                'category': model.category.value,
                'status': model.status.value,
                'version': model.version,
                'created': model.created.isoformat(),
                'last_updated': model.last_updated.isoformat(),
                'maintainer': model.maintainer,
            }

            if model.description:
                model_dict['description'] = model.description

            if model.dimensions:
                model_dict['dimensions'] = [
                    {
                        'symbol': d.symbol,
                        'name': d.name,
                        'description': d.description,
                        'weight': d.weight,
                        'beta_coefficient': d.beta_coefficient,
                        'range': [d.range_min, d.range_max]
                    }
                    for d in model.dimensions
                ]

            if model.validation:
                model_dict['validation'] = {
                    'accuracy': model.validation.accuracy,
                    'confidence': model.validation.confidence.value,
                    'data_points': model.validation.data_points,
                    'rmse': model.validation.rmse,
                    'precision': model.validation.precision,
                    'recall': model.validation.recall
                }

            data['models'].append(model_dict)

        # Write to file
        with open(self.registry_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        print(f"✓ Registry saved to {self.registry_path}")

    # ========================================================================
    # QUERY OPERATIONS
    # ========================================================================

    def get_model(self, model_id: str) -> Optional[ModelRecord]:
        """Get a model by ID"""
        return self.models.get(model_id)

    def list_models(self, status: Optional[ModelStatus] = None,
                    category: Optional[ModelCategory] = None) -> List[ModelRecord]:
        """List models with optional filtering"""
        result = list(self.models.values())

        if status:
            result = [m for m in result if m.status == status]

        if category:
            result = [m for m in result if m.category == category]

        return result

    def list_models_by_status(self, status: ModelStatus) -> List[ModelRecord]:
        """Get all models with given status"""
        return [m for m in self.models.values() if m.status == status]

    def list_models_by_category(self, category: ModelCategory) -> List[ModelRecord]:
        """Get all models in given category"""
        return [m for m in self.models.values() if m.category == category]

    def get_best_validated_models(self, n: int = 5) -> List[ModelRecord]:
        """Get top N models by validation accuracy"""
        validated = [m for m in self.models.values() if m.validation]
        validated.sort(key=lambda m: m.validation.accuracy, reverse=True)
        return validated[:n]

    # ========================================================================
    # VALIDATION OPERATIONS
    # ========================================================================

    def validate_model(self, model_id: str) -> tuple[bool, List[str]]:
        """Validate a single model against schema"""
        model = self.get_model(model_id)
        if not model:
            return False, [f"Model not found: {model_id}"]

        errors = []
        try:
            model.validate()
        except ValueError as e:
            errors.append(str(e))

        return len(errors) == 0, errors

    def validate_all_models(self) -> Dict[str, tuple[bool, List[str]]]:
        """Validate all models"""
        results = {}
        for model_id in self.models:
            valid, errors = self.validate_model(model_id)
            results[model_id] = (valid, errors)
        return results

    def check_dimension_weights_valid(self) -> Dict[str, float]:
        """Check that all models have valid dimension weights"""
        issues = {}
        for model_id, model in self.models.items():
            if model.dimensions:
                total = sum(d.weight for d in model.dimensions)
                if not (0.95 <= total <= 1.05):
                    issues[model_id] = total
        return issues

    # ========================================================================
    # REPORTING
    # ========================================================================

    def get_portfolio_summary(self) -> str:
        """Generate portfolio summary report"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("EBF MODEL REGISTRY SUMMARY")
        report.append("=" * 80)

        # Count by status
        report.append("\nModels by Status:")
        for status in ModelStatus:
            count = len(self.list_models_by_status(status))
            report.append(f"  {status.value:15s}: {count}")

        # Count by category
        report.append("\nModels by Category:")
        for category in ModelCategory:
            count = len(self.list_models_by_category(category))
            if count > 0:
                report.append(f"  {category.value:15s}: {count}")

        # Validation coverage
        validated = [m for m in self.models.values() if m.validation]
        report.append(f"\nValidation Coverage:")
        report.append(f"  Validated models: {len(validated)}/{len(self.models)}")

        # Accuracy statistics
        if validated:
            accuracies = [m.validation.accuracy for m in validated]
            avg_acc = sum(accuracies) / len(accuracies)
            max_acc = max(accuracies)
            min_acc = min(accuracies)
            report.append(f"\nAccuracy Statistics:")
            report.append(f"  Average: {avg_acc:.1%}")
            report.append(f"  Best: {max_acc:.1%}")
            report.append(f"  Worst: {min_acc:.1%}")

        # Recent updates
        report.append(f"\nRecent Updates:")
        sorted_models = sorted(self.models.values(),
                             key=lambda m: m.last_updated,
                             reverse=True)
        for model in sorted_models[:3]:
            report.append(f"  {model.model_id:20s} v{model.version:5s} "
                        f"({model.last_updated.date()})")

        report.append("=" * 80 + "\n")
        return "\n".join(report)

    def get_model_details(self, model_id: str) -> str:
        """Get detailed report for a single model"""
        model = self.get_model(model_id)
        if not model:
            return f"Model not found: {model_id}"

        details = []
        details.append(f"\nMODEL: {model.model_id}")
        details.append(f"{'='*60}")
        details.append(f"Name:           {model.short_name}")
        details.append(f"Category:       {model.category.value}")
        details.append(f"Status:         {model.status.value}")
        details.append(f"Version:        {model.version}")
        details.append(f"Created:        {model.created.date()}")
        details.append(f"Last Updated:   {model.last_updated.date()}")
        details.append(f"Maintainer:     {model.maintainer}")

        if model.description:
            details.append(f"\nDescription:")
            details.append(f"  {model.description}")

        if model.dimensions:
            details.append(f"\nDimensions:")
            for dim in model.dimensions:
                details.append(f"  {dim.symbol}: {dim.name} (weight: {dim.weight:.0%})")

        if model.validation:
            details.append(f"\nValidation:")
            details.append(f"  Accuracy:    {model.validation.accuracy:.1%}")
            details.append(f"  Confidence:  {model.validation.confidence.value}")
            details.append(f"  Data Points: {model.validation.data_points}")
            if model.validation.rmse:
                details.append(f"  RMSE:        {model.validation.rmse:.3f}")

        details.append("=" * 60 + "\n")
        return "\n".join(details)

    def get_registry_status(self) -> str:
        """Get overall registry health status"""
        status = []
        status.append("\n" + "=" * 80)
        status.append("REGISTRY STATUS")
        status.append("=" * 80)

        # Validation check
        all_valid = True
        validation_results = self.validate_all_models()
        for model_id, (valid, errors) in validation_results.items():
            if not valid:
                all_valid = False
                status.append(f"✗ {model_id}: {errors[0]}")
            else:
                status.append(f"✓ {model_id}: Valid")

        # Dimension weight check
        weight_issues = self.check_dimension_weights_valid()
        if weight_issues:
            status.append("\nDimension Weight Issues:")
            for model_id, total in weight_issues.items():
                status.append(f"  ✗ {model_id}: Total weight = {total:.2f} (should be ~1.0)")

        if all_valid and not weight_issues:
            status.append("\n✓ All models valid!")

        status.append("=" * 80 + "\n")
        return "\n".join(status)


# ============================================================================
# MAIN: Example usage
# ============================================================================

if __name__ == "__main__":
    print("EBF Model Registry Loader")
    print("=" * 80)

    # Initialize registry
    registry = ModelRegistry()

    # Print summary
    print(registry.get_portfolio_summary())

    # Validate all models
    print("Validating all models...")
    results = registry.validate_all_models()
    for model_id, (valid, errors) in results.items():
        if valid:
            print(f"✓ {model_id}: VALID")
        else:
            print(f"✗ {model_id}: ERRORS")
            for error in errors:
                print(f"  - {error}")

    # Print registry status
    print(registry.get_registry_status())

    # Example: Get details on PSF 2.0
    if "PSF-2.0" in registry.models:
        print(registry.get_model_details("PSF-2.0"))
