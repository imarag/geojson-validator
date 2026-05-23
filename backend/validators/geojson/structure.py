from typing import Any

from exceptions import ValidationError
from models.geojson import GEOMETRY_DEPTH, geojson_types
from models.validation import Issue, IssueCode, ParamSpec, Severity, format_expected_types
from utils.geo_tools import GeoTools
from utils.path_tracker import PathTracker


def validate_key_param(
    obj: dict,
    param_spec: ParamSpec,
    severity: Severity,
    path_tracker: PathTracker,
    **kwargs,
) -> list[Issue]:
    issues: list[Issue] = []
    param_name = param_spec.name

    # ---------- Missing key ----------
    if param_name not in obj:
        detail_dict: dict[str, Any] = {"missing_field": param_name}
        repair_hint = f"Add the '{param_name}' field to the object."

        if param_spec.allowed_values:
            detail_dict["allowed_values"] = param_spec.allowed_values
            allowed_str = ", ".join(map(str, param_spec.allowed_values))
            repair_hint += f" Allowed values: {allowed_str}."

        issue = Issue(
            message=f"Missing field '{param_name}'.",
            description=(
                f"The required field '{param_name}' is missing from the object. "
                "Every GeoJSON object must include this field to conform to the expected schema."
            ),
            issue_code=IssueCode.KEY_MISSING,
            severity=severity,
            path=path_tracker.current(),
            repair_hint=repair_hint,
            detail=detail_dict,
        )
        issues.append(issue)
        return issues

    value = obj[param_name]

    # ---------- Type check ----------
    if not isinstance(param_spec.dtype, (type, tuple, list)):
        raise TypeError(f"Invalid dtype for param '{param_name}': {param_spec.dtype}")

    if not isinstance(value, param_spec.dtype):
        if isinstance(param_spec.dtype, (tuple, list)):
            type_names = ", ".join(format_expected_types(t) for t in param_spec.dtype)
            message = f"Field '{param_name}' must be one of types: {type_names}."
            repair_hint = f"Set the '{param_name}' field to one of the types: {type_names}."
            expected_type_detail = [format_expected_types(t) for t in param_spec.dtype]
        else:
            expected = format_expected_types(param_spec.dtype)
            message = f"Field '{param_name}' must be of type {expected}."
            repair_hint = f"Set the '{param_name}' field to type {expected}."
            expected_type_detail = expected

        issue = Issue(
            message=message,
            description=(
                f"The field '{param_name}' has an invalid type. "
                "It must match the expected type(s) as defined in the schema."
            ),
            issue_code=IssueCode.KEY_UNSUPPORTED_TYPE,
            severity=severity,
            path=path_tracker.current(),
            repair_hint=repair_hint,
            detail={
                "expected_type": expected_type_detail,
                "provided_type": format_expected_types(type(value)),
            },
        )
        issues.append(issue)
        return issues

    # ---------- Allowed values ----------
    if param_spec.allowed_values is not None and value not in param_spec.allowed_values:
        allowed_str = ", ".join(map(str, param_spec.allowed_values))
        issue = Issue(
            message=f"Invalid value '{value}' for field '{param_name}'.",
            description=(
                f"The value '{value}' is not allowed for the field '{param_name}'. "
                f"Only the following values are permitted: {allowed_str}."
            ),
            issue_code=IssueCode.KEY_INVALID_VALUE,
            severity=severity,
            path=path_tracker.current(),
            repair_hint=f"Use one of the allowed values for '{param_name}'.",
            detail={
                "received_value": value,
                "allowed_values": list(param_spec.allowed_values),
            },
        )
        issues.append(issue)

    return issues


def validate_geojson_input(geojson: dict, path_tracker: PathTracker):
    if not isinstance(geojson, dict):
        issue = Issue(
            message="Invalid GeoJSON type.",
            description=(
                "Input should be a valid JSON object with key-value pairs "
                'representing a GeoJSON structure (e.g., {"type": "Feature", "id": "123", ...}). '
                "Lists, arrays, and primitive values are not allowed."
            ),
            issue_code=IssueCode.STRUCTURE_UNSUPPORTED_TYPE,
            severity=Severity.CRITICAL,
            path=path_tracker.current(),
            detail={
                "provided_type": format_expected_types(type(geojson)),
                "expected_type": format_expected_types(dict),
            },
        )
        raise ValidationError(issue)

    if not geojson:
        issue = Issue(
            message="GeoJSON object is empty.",
            issue_code=IssueCode.STRUCTURE_EMPTY,
            severity=Severity.CRITICAL,
            path=path_tracker.current(),
        )
        raise ValidationError(issue)


def validate_type_param(geojson: dict, path_tracker: PathTracker):
    allowed = ", ".join(sorted(geojson_types))
    if "type" not in geojson:
        issue = Issue(
            message="Missing 'type' field.",
            description=(
                "Every GeoJSON object must define a top-level 'type' field. "
                "This field tells parsers what kind of GeoJSON object this is, "
                "such as a Feature, FeatureCollection, or a Geometry type."
            ),
            issue_code=IssueCode.KEY_MISSING,
            severity=Severity.CRITICAL,
            path=path_tracker.current(),
            repair_hint=f"Add a valid 'type' field to the GeoJSON object with one "
            f"of the supported GeoJSON types: {allowed}",
        )
        raise ValidationError(issue)

    with path_tracker.track("type"):
        geojson_type = geojson["type"]

        if not isinstance(geojson_type, str):
            issue = Issue(
                message="Invalid type for the 'type' field.",
                description=(
                    "According to the GeoJSON specification, the 'type' field "
                    "must always be a string. Using numbers, null, or other "
                    "data types makes the GeoJSON invalid and unreadable by "
                    "standard GeoJSON tools."
                ),
                issue_code=IssueCode.KEY_UNSUPPORTED_TYPE,
                severity=Severity.CRITICAL,
                path=path_tracker.current(),
                repair_hint=f"Set the 'type' field to a string value that is "
                f"one of the supported GeoJSON types: {allowed}.",
                detail={
                    "expected_type": format_expected_types(str),
                    "provided_type": format_expected_types(type(geojson_type)),
                },
            )
            raise ValidationError(issue)

        if geojson_type not in geojson_types:
            issue = Issue(
                message="Invalid value of 'type' field.",
                description=(
                    "The provided 'type' value is not recognized as a valid "
                    "GeoJSON object type. GeoJSON only allows a predefined set "
                    "of types defined by the specification."
                ),
                issue_code=IssueCode.KEY_INVALID_VALUE,
                severity=Severity.CRITICAL,
                path=path_tracker.current(),
                repair_hint=f"Set the 'type' field to a string value that is "
                f"one of the supported GeoJSON types: {allowed}.",
                detail={
                    "provided_value": geojson_type,
                    "allowed_values": allowed,
                },
            )
            raise ValidationError(issue)


def validate_geojson_structure(geojson: dict, max_top_level_keys: int, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    # Check type
    if not isinstance(geojson, dict):
        issue = Issue(
            message="Invalid GeoJSON type.",
            description=(
                "Input must be a valid JSON object with key-value pairs "
                'representing a GeoJSON structure (e.g., {"type": "Feature", "id": "123", ...}). '
                "Lists, arrays, and primitive values are not allowed."
            ),
            issue_code=IssueCode.STRUCTURE_INVALID_SCHEMA,
            severity=Severity.CRITICAL,
            path=path_tracker.current(),
            detail={
                "provided_type": format_expected_types(type(geojson)),
                "expected_type": format_expected_types(dict),
            },
        )
        issues.append(issue)
        return issues

    # Check empty object
    if not geojson:
        issues.append(
            Issue(
                message="GeoJSON object is empty.",
                issue_code=IssueCode.STRUCTURE_EMPTY,
                severity=Severity.CRITICAL,
                path=path_tracker.current(),
            )
        )
        return issues

    # Check too many top-level keys
    if len(geojson) > max_top_level_keys:
        issue = Issue(
            message="GeoJSON object has too many top-level fields.",
            description=(
                "The GeoJSON object exceeds the allowed number of top-level fields. "
                "This limit is enforced for performance and safety reasons, as objects "
                "with excessive fields may impact validation speed and memory usage."
            ),
            issue_code=IssueCode.STRUCTURE_TOO_LARGE,
            severity=Severity.CRITICAL,
            path=path_tracker.current(),
            repair_hint=f"Reduce the number of top-level fields to at most {max_top_level_keys}.",
            detail={
                "total_fields_found": len(geojson),
                "total_fields_allowed": max_top_level_keys,
            },
        )
        issues.append(issue)
        return issues
    return issues


def validate_coords_structure(
    coords: list,
    path_tracker: PathTracker,
    enforce_dimension: str,
) -> list[Issue]:
    issues: list[Issue] = []

    # ---------- Determine allowed coordinate dimensions ----------
    if enforce_dimension != "ignore":
        dim = enforce_dimension.strip().upper()
        if dim.startswith("2"):
            accept_lengths = [2]
        elif dim.startswith("3"):
            accept_lengths = [3]
        else:
            accept_lengths = [2, 3]
    else:
        accept_lengths = [2, 3]

    # ---------- Validate numeric structure ----------
    structure_validation_error = GeoTools.validate_numeric_structure(coords, accept_lengths)

    if structure_validation_error:
        valid_coordinates_examples: dict[str, dict[str, str]] = {
            "Point": {
                "description": "A single position defined by one coordinate pair.",
                "example": "[x, y]",
            },
            "MultiPoint": {
                "description": "A collection of independent points.",
                "example": "[[x1, y1], [x2, y2], ...]",
            },
            "LineString": {
                "description": "A line made of two or more connected positions.",
                "example": "[[x1, y1], [x2, y2], ...]",
            },
            "MultiLineString": {
                "description": "A collection of line strings.",
                "example": "[[[x1, y1], [x2, y2], ...], ...]",
            },
            "Polygon": {
                "description": "An area defined by linear rings.",
                "example": "[[[x1, y1], [x2, y2], ...], ...]",
            },
            "MultiPolygon": {
                "description": "A collection of polygons.",
                "example": "[[[[x1, y1], [x2, y2], ...], ...], ...]",
            },
        }

        detail_dict: dict[str, Any] = {
            "reason": structure_validation_error,
            "expected_dimensions": accept_lengths,
            "expected_formats": valid_coordinates_examples,
        }

        issue = Issue(
            message="Invalid coordinates structure.",
            description=(
                "The 'coordinates' field must be a nested array of numeric values that "
                "matches the expected structure for the geometry type. "
                "All coordinate tuples must have a consistent dimensionality "
                f"({', '.join(map(str, accept_lengths))}D)."
            ),
            issue_code=IssueCode.STRUCTURE_INVALID_SCHEMA,
            severity=Severity.ERROR,
            path=path_tracker.current(),
            repair_hint=(
                "Ensure the coordinates are properly nested and that each coordinate "
                f"contains {'or '.join(map(str, accept_lengths))} numeric values."
            ),
            detail=detail_dict,
        )
        issues.append(issue)
        return issues

    return issues


def geom_type_coord_dim_consistent(geom: dict, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    geom_type = geom["type"]
    coordinates = geom["coordinates"]

    exp_depth = GEOMETRY_DEPTH[geom_type]

    coords_depth = GeoTools.get_coord_depth(coordinates)

    if coords_depth != exp_depth:
        issues.append(
            Issue(
                message="Invalid coordinates structure for geometry type.",
                description=(
                    "The nesting depth of the coordinates array does not correspond "
                    "to the expected structure for this geometry type."
                ),
                issue_code=IssueCode.COORDINATES_INVALID,
                severity=Severity.ERROR,
                path=path_tracker.current(),
                repair_hint=(
                    f"Adjust the coordinates array so that its nesting depth matches "
                    f"the expected depth ({exp_depth}) for geometry type '{geom_type}'."
                ),
                detail={
                    "expected_depth": exp_depth,
                    "found_depth": coords_depth,
                    "geometry_type": geom_type,
                },
            )
        )

    return issues
