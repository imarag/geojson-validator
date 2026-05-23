from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel


class IssueCode(str, Enum):
    # ---------- Input ----------
    INPUT_MISSING = "input_missing"
    INPUT_EMPTY = "input_empty"
    INPUT_NOT_JSON = "input_not_json"
    INPUT_NOT_OBJECT = "input_not_object"
    INPUT_UNSUPPORTED_TYPE = "input_unsupported_type"

    KEY_MISSING = "key_missing"
    KEY_UNSUPPORTED_TYPE = "key_unsupported_type"
    KEY_INVALID_VALUE = "key_invalid_value"
    KEY_FORBIDDEN = "key_forbidden"
    KEY_FOREIGN = "key_foreign"  # or KEY_UNKNOWN

    STRUCTURE_INVALID_SCHEMA = "structure_invalid_schema"
    STRUCTURE_EMPTY = "structure_empty"
    STRUCTURE_UNSUPPORTED_TYPE = "structure_unsupported_type"
    STRUCTURE_TOO_LARGE = "structure_too_large"

    BBOX_INVALID_LENGTH = "bbox_invalid_length"
    BBOX_INVALID_COORDS = "bbox_invalid_coords"
    BBOX_NOT_FINITE_VALUES = "bbox_not_finite_values"
    BBOX_INVALID = "bbox_invalid"

    COORDINATES_INVALID = "coordinates_invalid"

    GEOMETRY_INVALID = "geometry_invalid"
    GEOMETRY_EMPTY = "geometry_empty"
    GEOMETRY_DUPLICATE_GEOM = "geometry_duplicate_geom"
    GEOMETRY_SELF_INTERSECTION = "geometry_self_intersection"
    GEOMETRY_SELF_CLOSE = "geometry_self_close"
    GEOMETRY_UNSUPPORTED_TYPE = "geometry_unsupported_type"
    GEOMETRY_INVALID_ORIENTATION = "geometry_invalid_orientation"
    GEOMETRY_ZERO_AREA = "geometry_zero_area"


class Severity(str, Enum):
    """Severity of issues"""

    ERROR = "error"
    CRITICAL = "critical"
    WARNING = "warning"


@dataclass
class Issue:
    """Validation issue structure"""

    # User-facing
    message: str
    issue_code: IssueCode
    severity: Severity
    description: str | None = None

    # Location
    path: str | None = None

    # Repair metadata
    repair_hint: str | None = None
    detail: dict[str, Any] | None = None

    # Context
    repairable: bool = False
    repair_context: dict[str, Any] | None = None


class ParamSpec(BaseModel):
    """Dict param validation structure"""

    name: str
    dtype: type | tuple[type, ...]
    validation_function: Callable[[Any], list[Issue]] | None = None
    allowed_values: list[Any] | None = None
    important: bool = False
    optional: bool = False


def format_expected_types(dtype: type) -> str:
    TYPE_LABELS = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        tuple: "array",
        dict: "object",
        type(None): "null",
    }
    return TYPE_LABELS.get(dtype, dtype.__name__)
