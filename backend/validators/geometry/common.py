from shapely.geometry.base import BaseGeometry

from models.validation import Issue, IssueCode, Severity
from utils.path_tracker import PathTracker


def validate_geometry_empty(geom: BaseGeometry, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    if geom.is_empty:
        issue = Issue(
            message="The geometry is empty and cannot be processed.",
            issue_code=IssueCode.GEOMETRY_EMPTY,
            severity=Severity.ERROR,
            path=path_tracker.current(),
        )
        issues.append(issue)
    return issues
