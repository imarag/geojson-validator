from configuration.geojson.validation import GeoJSONValidationConfig
from models.geojson import OPTIONAL_KEYS, REQUIRED_KEYS
from models.validation import Issue, IssueCode, Severity
from utils.path_tracker import PathTracker


def validate_crs(geojson: dict, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    if "crs" in geojson:
        issue = Issue(
            message="Deprecated 'crs' field found in GeoJSON.",
            description=(
                "According to RFC 7946, the `crs` member is no "
                "longer supported in GeoJSON. All GeoJSON coordinates are assumed "
                "to be in WGS84 (EPSG:4326). If a `crs` field is found, it is considered "
                "forbidden and should be removed."
            ),
            issue_code=IssueCode.KEY_FORBIDDEN,
            severity=Severity.WARNING,
            path=path_tracker.current(),
            repair_hint="Remove the 'crs' field from the GeoJSON object.",
            repairable=True,
        )
        issues.append(issue)

    return issues


def validate_foreign_keys(
    geojson: dict, geojson_type: str, config: GeoJSONValidationConfig, path_tracker: PathTracker
) -> list[Issue]:
    issues: list[Issue] = []

    if config.allow_foreign_keys:
        return issues

    required_keys_list = REQUIRED_KEYS[geojson_type]

    # Determine unexpected keys (excluding crs, handled separately)
    foreign_keys = set(geojson.keys()) - set(required_keys_list) - set(OPTIONAL_KEYS) - {"crs"}

    if foreign_keys:
        issue = Issue(
            message="Unexpected fields found in GeoJSON object.",
            description=(
                "The GeoJSON object contains fields that are not part of the allowed schema. "
                "These unexpected fields may interfere with validation or processing. "
                "Only the required and optional fields defined for this GeoJSON type are permitted. "
                "Foreign keys are disallowed unless explicitly enabled in the configuration."
            ),
            issue_code=IssueCode.KEY_FOREIGN,
            severity=Severity.WARNING,
            path=path_tracker.current(),
            repair_hint=("Remove or rename these unexpected fields so the object only contains the allowed keys."),
            detail={
                "unexpected_fields": sorted(foreign_keys),
                "allowed_fields": sorted(required_keys_list + OPTIONAL_KEYS),
            },
            repairable=True,
            repair_context={
                "unexpected_keys": sorted(foreign_keys),
                "required_keys": sorted(required_keys_list),
                "optional_keys": sorted(OPTIONAL_KEYS),
            },
        )
        issues.append(issue)

    return issues


# def validate_object_key(geojson: dict, config: GeoJSONValidationConfig, path_tracker: PathTracker) -> list[Issue]:
#     issues: list[Issue] = []
#     for key in geojson:
#         with path_tracker.track(key):
#             key_val_errors = GeoTools.validate_json_key_value(geojson, key, config.max_key_length)
#             if len(key_val_errors) > 0:
#                 issue = Issue(
#                     message=f"There are issues with the field '{key}' or its value.",
#                     issue_code=IssueCode.KEY_INVALID,
#                     severity=Severity.ERROR,
#                     path=path_tracker.current(),
#                     detail={"field_value_issues": key_val_errors},
#                 )
#                 issues.append(issue)
#     return issues
