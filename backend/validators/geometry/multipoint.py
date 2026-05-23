from shapely.geometry import MultiPoint

from models.validation import Issue, IssueCode, Severity
from utils.geometry_tools import GeometryTools
from utils.path_tracker import PathTracker


def validate_multipoint_duplicate_points(geom: MultiPoint, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    dup_points, dup_indices = GeometryTools.find_duplicate_geometries(geom)

    if dup_points:
        issue = Issue(
            message="MultiPoint geometry contains duplicate points.",
            issue_code=IssueCode.GEOMETRY_DUPLICATE_GEOM,
            severity=Severity.WARNING,
            path=path_tracker.current(),
            detail={"duplicate_indices": dup_indices, "sample_geoms": dup_points},
            repair_hint="Remove the points at the duplicate indices to ensure all points are unique.",
            repairable=True,
            repair_context={"duplicate_indices": dup_indices},
        )
        issues.append(issue)

    return issues
