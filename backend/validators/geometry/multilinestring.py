from shapely.geometry import MultiLineString

from models.validation import Issue, IssueCode, Severity
from utils.geometry_tools import GeometryTools
from utils.path_tracker import PathTracker


def validate_multilinestring_duplicate_lines(geom: MultiLineString, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    # Find duplicate lines along with their indices
    dup_lines, dup_indices = GeometryTools.find_duplicate_geometries(geom)

    if dup_lines:
        issue = Issue(
            message="MultiLineString geometry contains duplicate lines.",
            issue_code=IssueCode.GEOMETRY_DUPLICATE_GEOM,
            severity=Severity.ERROR,
            path=path_tracker.current(),
            detail={"duplicate_indices": dup_indices, "sample_geometries": dup_lines},
            repairable=True,
            repair_context={"duplicate_indices": dup_indices},
            repair_hint=(f"Remove the duplicate lines at indices {dup_indices} to ensure all lines are unique."),
        )
        issues.append(issue)

    return issues


def validate_multilinestring_lines_intersect(geom: MultiLineString, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    if not geom.is_simple:
        issue = Issue(
            message="MultiLineString geometry contains intersecting lines.",
            issue_code=IssueCode.GEOMETRY_SELF_INTERSECTION,
            severity=Severity.ERROR,
            path=path_tracker.current(),
            detail={"coords": [list(line.coords) for line in geom.geoms]},
            repairable=True,
            repair_context={"geometry": geom},
            repair_hint=(
                "Simplify or adjust the lines to remove intersections, "
                "ensuring each line is simple and does not cross another."
            ),
        )
        issues.append(issue)

    return issues
