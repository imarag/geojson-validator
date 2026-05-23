from dataclasses import dataclass, field
from typing import Any, Sequence

from shapely.geometry.base import BaseGeometry


# ---------------------- INPUT ----------------------
@dataclass
class InputMissingDetail:
    reason: str = "No input provided"
    repair_hint: str = "Provide a valid GeoJSON input."


@dataclass
class InputNotJsonDetail:
    input_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Ensure the input is valid JSON, not {self.input_type.__name__}."


@dataclass
class InputNotObjectDetail:
    input_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Convert input to a JSON object (dict), not {self.input_type.__name__}."


@dataclass
class InputUnsupportedTypeDetail:
    expected_type: type | tuple[type, ...]
    input_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        exp = (
            ", ".join(t.__name__ for t in self.expected_type)
            if isinstance(self.expected_type, (tuple, list))
            else self.expected_type.__name__
        )
        self.repair_hint = f"Convert input from {self.input_type.__name__} to {exp}."


# ---------------------- KEY ----------------------
@dataclass
class KeyMissingDetail:
    missing_field: str
    example_values: list[str]
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Add the missing key '{self.missing_field}' with a value from : {self.example_values}"


@dataclass
class KeyUnsupportedTypeDetail:
    expected_type: type | tuple[type, ...] | list[type]
    input_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        exp = (
            ", ".join(t.__name__ for t in self.expected_type)
            if isinstance(self.expected_type, (tuple, list))
            else self.expected_type.__name__
        )
        self.repair_hint = f"Convert '{self.input_type.__name__}' to expected type: {exp}"


@dataclass
class KeyInvalidValueDetail:
    input_value: Any
    allowed_values: list[Any] | tuple[Any]
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Replace '{self.input_value}' with one of: {self.allowed_values}"


@dataclass
class KeyForbiddenDetail:
    forbidden_field: str
    reason: str
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Remove the forbidden key '{self.forbidden_field}'"


@dataclass
class KeyForeignDetail:
    unexpected_fields: list[str]
    allowed_fields: list[str]
    optional_fields: list[str]
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Remove unexpected keys: {self.unexpected_fields}"


# ---------------------- STRUCTURE ----------------------
@dataclass
class StructureTooLargeDetail:
    total_fields_found: int
    total_fields_allowed: int
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Reduce top-level keys to {self.total_fields_allowed} or fewer."


@dataclass
class StructureInvalidSchemaDetail:
    input_type: type
    expected_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Convert input to a {self.expected_type} type."


@dataclass
class StructureUnsupportedTypeDetail:
    expected_type: type | tuple[type, ...]
    input_type: type
    repair_hint: str = field(init=False)

    def __post_init__(self):
        exp = (
            ", ".join(t.__name__ for t in self.expected_type)
            if isinstance(self.expected_type, (tuple, list))
            else self.expected_type.__name__
        )
        self.repair_hint = f"Convert input type from {self.input_type.__name__} to {exp}"


@dataclass
class StructureEmptyDetail:
    repair_hint: str = "Provide at least one field in the object."


# ---------------------- BBOX ----------------------


@dataclass
class BBoxInvalidLength:
    reason: str
    bbox: list[float] | None = None
    repair_hint: str = field(init=False)

    def __post_init__(self) -> None:
        self.repair_hint = "Ensure bbox contains exactly four numeric values [minx, miny, maxx, maxy]."


@dataclass
class BBoxNotFiniteValues:
    bbox: list[float] | None = None
    sample_invalid_values: list[float] | None = None
    repair_hint: str = field(init=False)

    def __post_init__(self) -> None:
        self.repair_hint = (
            "Replace NaN or infinite values with valid finite coordinates, or recompute the bbox from the geometry."
        )


@dataclass
class BBoxInvalidCoords:
    bbox: list[float] | None = None
    repair_hint: str = field(init=False)

    def __post_init__(self) -> None:
        self.repair_hint = "Ensure the bbox is expressed in EPSG:4326 (longitude/latitude in degrees) and that the coordinates are ordered correctly (minx < maxx, miny < maxy), or recompute it from the geometry."


# ---------------------- GEOMETRY ----------------------
@dataclass
class GeometryDuplicateDetail:
    duplicate_indices: Sequence[int]
    sample_geoms: list[BaseGeometry]
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Remove duplicate geometries at indices: " + ", ".join(map(str, self.duplicate_indices))


@dataclass
class GeometryInvalidDetail:
    reason: str
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Fix the geometry to be valid (e.g., check self-intersections or invalid rings)."


@dataclass
class GeometryZeroAreaDetail:
    area: float
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Polygon has zero area. Ensure coordinates define a valid polygon."


@dataclass
class GeometryUnsupportedTypeDetail:
    input_type: type
    supported_types: list[type]
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Convert geometry from type {self.input_type.__name__} to one of: " + ", ".join(
            t.__name__ for t in self.supported_types
        )


@dataclass
class GeometryInvalidOrientationDetail:
    ring_type: str  # 'exterior' or 'interior'
    expected: str
    found: str
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = f"Flip the {self.ring_type} ring from '{self.found}' to '{self.expected}' orientation."


@dataclass
class GeometrySelfIntersectionDetail:
    ring_type: str | None = None  # 'exterior', 'interior', or None
    description: str | None = None
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Use shapely.buffer(0) to attempt fixing self-intersections."


@dataclass
class GeometrySelfCloseDetail:
    description: str | None = None
    repair_hint: str = field(init=False)

    def __post_init__(self):
        self.repair_hint = "Convert closed LineString to Polygon if that was intended."
