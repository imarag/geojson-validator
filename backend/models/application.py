from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class OperationType(str, Enum):
    """Types of operations supported by the pipeline."""

    VALIDATION = "validation"
    REPAIR = "repair"
    TRANSFORMATION = "transformation"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def list_operations(cls) -> list[str]:
        return [op.value for op in cls]


class SourceType(str, Enum):
    """Types of geospatial data sources."""

    GEOJSON = "geojson"
    SHAPEFILE = "shapefile"
    GEOPACKAGE = "geopackage"
    GEODATAFRAME = "geodataframe"
    KML = "kml"
    WKT = "wkt"
    AUTO = "auto"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def list_source_types(cls) -> list[str]:
        return [op.value for op in cls]


class ValidationStatus(str, Enum):
    """Status of validation results."""

    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"


class RepairStrategy(str, Enum):
    """Strategies for repairing geometries."""

    BUFFER_ZERO = "buffer_zero"
    SIMPLIFY = "simplify"
    REMOVE_INVALID = "remove_invalid"
    FIX_TOPOLOGY = "fix_topology"


class TransformationType(str, Enum):
    """Types of transformations."""

    BUFFER = "buffer"
    SIMPLIFY = "simplify"
    REPROJECT = "reproject"
    CLIP = "clip"
    UNION = "union"
    INTERSECTION = "intersection"
    DIFFERENCE = "difference"


@dataclass
class PipelineResult:
    """Result from pipeline execution."""

    success: bool
    errors: list[str] = field(default_factory=list)
    result: Any = None

    def has_errors(self) -> bool:
        """Check if result has errors."""
        return len(self.errors) > 0

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "errors": self.errors,
            "result": self.result,
        }


@dataclass
class ValidationResult(PipelineResult):
    """Result from validation operation."""

    validation_status: ValidationStatus = ValidationStatus.VALID
    issues: list[int] = field(default_factory=list)


@dataclass
class RepairResult(PipelineResult):
    """Result from repair operation."""

    repaired_count: int = 0
    failed_count: int = 0
    strategy_used: RepairStrategy | None = None

    def increment_repaired(self) -> None:
        """Increment count of repaired features."""
        self.repaired_count += 1

    def increment_failed(self) -> None:
        """Increment count of failed repairs."""
        self.failed_count += 1


@dataclass
class TransformationResult(PipelineResult):
    """Result from transformation operation."""

    transformation_type: TransformationType | None = None
    features_transformed: int = 0

    def increment_transformed(self) -> None:
        """Increment count of transformed features."""
        self.features_transformed += 1


@dataclass
class PipelineConfig:
    """Configuration for pipeline execution."""

    operation: OperationType
    source_type: SourceType
    strict_validation: bool = True
    max_errors: int = 100
    timeout_seconds: int | None = None

    # Validation specific
    validate_geometry: bool = True
    validate_schema: bool = True

    # Repair specific
    repair_strategy: RepairStrategy = RepairStrategy.BUFFER_ZERO

    # Transformation specific
    transformation_type: TransformationType | None = None
    transformation_params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "operation": self.operation.value,
            "source_type": self.source_type.value,
            "strict_validation": self.strict_validation,
            "max_errors": self.max_errors,
            "timeout_seconds": self.timeout_seconds,
            "validate_geometry": self.validate_geometry,
            "validate_schema": self.validate_schema,
            "repair_strategy": self.repair_strategy.value if self.repair_strategy else None,
            "transformation_type": self.transformation_type.value if self.transformation_type else None,
            "transformation_params": self.transformation_params,
        }
