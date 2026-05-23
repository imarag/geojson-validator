from shapely.geometry import LineString

from models.validation import Issue, IssueCode, Severity
from utils.geometry_tools import GeometryTools
from utils.path_tracker import PathTracker


def validate_linestring_consecutive_dups(geom: LineString, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    # Find consecutive duplicate points and their indices
    dup_points, dup_indices = GeometryTools.find_linestring_consecutive_point_dups(geom)

    if dup_points:
        issue = Issue(
            message="Found duplicate consecutive points in the LineString geometry.",
            issue_code=IssueCode.GEOMETRY_DUPLICATE_GEOM,
            severity=Severity.WARNING,
            path=path_tracker.current(),
            detail={"duplicate_indices": dup_indices, "sample_geoms": dup_points},
            repairable=True,
            repair_context={"duplicate_indices": dup_indices},
            repair_hint=("Remove consecutive duplicate points to ensure a clean LineString."),
        )
        issues.append(issue)

    return issues


def validate_linestring_self_intersection(geom: LineString, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    if not geom.is_simple:
        issue = Issue(
            message="LineString is self-intersecting, which violates OGC simplicity rules.",
            issue_code=IssueCode.GEOMETRY_SELF_INTERSECTION,
            severity=Severity.ERROR,
            path=path_tracker.current(),
            repairable=True,
            repair_context={"geometry": geom},
            repair_hint="Simplify the LineString using a geometry cleaning algorithm "
            "or manually adjust points to remove self-intersections.",
            detail={"geometry_coordinates": list(geom.coords)},
        )
        issues.append(issue)

    return issues


def validate_linestring_closed(geom: LineString, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    if geom.is_closed:
        issue = Issue(
            message=(
                "LineString is closed (first and last coordinates are identical). "
                "This may indicate that a Polygon was intended."
            ),
            issue_code=IssueCode.GEOMETRY_SELF_CLOSE,
            severity=Severity.WARNING,
            path=path_tracker.current(),
            repairable=True,
            repair_context={"geometry": geom},
            repair_hint=("Check if this LineString should be a Polygon. If not, remove the duplicate closing point."),
            detail={"geometry_coordinates": list(geom.coords)},
        )
        issues.append(issue)

    return issues
