from shapely.geometry import MultiPolygon

from models.validation import Issue, IssueCode, Severity
from utils.geometry_tools import GeometryTools
from utils.path_tracker import PathTracker


def validate_multipolygon_intersections(geom: MultiPolygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []

    intersect_polygons = GeometryTools.find_intersecting_polygons(geom)

    if intersect_polygons:
        issue = Issue(
            message="Polygons in MultiPolygon intersect.",
            issue_code=IssueCode.GEOMETRY_SELF_INTERSECTION,
            severity=Severity.ERROR,
            path=path_tracker.current(),
            detail={
                "intersecting_polygons": intersect_polygons,
            },
            repairable=True,
            repair_hint=("Adjust the coordinates of the intersecting polygons or split them to remove overlaps."),
            repair_context={"intersecting_polygons": intersect_polygons, "geometry": geom},
        )
        issues.append(issue)

    return issues
