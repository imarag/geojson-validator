from shapely.geometry import Polygon
from shapely.validation import explain_validity

from models.validation import Issue, IssueCode, Severity
from utils.geometry_tools import GeometryTools
from utils.path_tracker import PathTracker


def polygon_has_zero_area(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    if geom.area == 0:
        issues.append(
            Issue(
                message="Polygon has zero area.",
                issue_code=IssueCode.GEOMETRY_ZERO_AREA,
                severity=Severity.ERROR,
                path=path_tracker.current(),
                repairable=True,
                repair_hint="Remove or correct the polygon coordinates to create a valid non-zero area polygon.",
                detail={"area": geom.area},
                repair_context={"geometry": geom},
            )
        )
    return issues


def validate_polygon_exterior_self_intersection(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    exterior = geom.exterior
    if not exterior.is_simple:
        issues.append(
            Issue(
                message="Polygon exterior boundary intersects itself.",
                issue_code=IssueCode.GEOMETRY_SELF_INTERSECTION,
                severity=Severity.ERROR,
                path=path_tracker.current(),
                repairable=True,
                repair_hint="Simplify or adjust the exterior coordinates to remove self-intersections.",
                detail={"coords": list(exterior.coords)},
                repair_context={"geometry": geom},
            )
        )
    return issues


def validate_polygon_interiors_self_intersection(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    for i, ring in enumerate(geom.interiors):
        if not ring.is_simple:
            issues.append(
                Issue(
                    message=f"Polygon interior boundary {i} intersects itself.",
                    issue_code=IssueCode.GEOMETRY_SELF_INTERSECTION,
                    severity=Severity.ERROR,
                    path=path_tracker.current(),
                    repairable=True,
                    repair_hint=f"Simplify or adjust interior ring {i} to remove self-intersections.",
                    detail={"coords": list(ring.coords)},
                    repair_context={"geometry": geom, "ring_index": i},
                )
            )
    return issues


def validate_polygon_exterior_orientation(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    exterior = geom.exterior
    orientation = GeometryTools.get_ring_orientation(exterior)
    if orientation != "ccw":
        issues.append(
            Issue(
                message="Polygon exterior boundary orientation is not counter-clockwise.",
                issue_code=IssueCode.GEOMETRY_INVALID_ORIENTATION,
                severity=Severity.ERROR,
                path=path_tracker.current(),
                repairable=True,
                repair_hint="Reverse the exterior ring coordinates to be counter-clockwise.",
                detail={"expected_orientation": "ccw", "found_orientation": orientation},
                repair_context={"geometry": geom, "ring": "exterior"},
            )
        )
    return issues


def validate_polygon_interiors_orientation(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    for i, ring in enumerate(geom.interiors):
        orientation = GeometryTools.get_ring_orientation(ring)
        if orientation != "cw":
            issues.append(
                Issue(
                    message=f"Polygon interior boundary {i} orientation is not clockwise.",
                    issue_code=IssueCode.GEOMETRY_INVALID_ORIENTATION,
                    severity=Severity.ERROR,
                    path=path_tracker.current(),
                    repairable=True,
                    repair_hint=f"Reverse interior ring {i} coordinates to be clockwise.",
                    detail={"expected_orientation": "cw", "found_orientation": orientation},
                    repair_context={"geometry": geom, "ring_index": i},
                )
            )
    return issues


def validate_polygon_is_valid(geom: Polygon, path_tracker: PathTracker) -> list[Issue]:
    issues: list[Issue] = []
    if not geom.is_valid:
        issues.append(
            Issue(
                message="Polygon geometry is invalid.",
                issue_code=IssueCode.GEOMETRY_INVALID,
                severity=Severity.ERROR,
                path=path_tracker.current(),
                repairable=True,
                repair_hint="Use Shapely's `make_valid` or manually correct the polygon coordinates.",
                detail={"reason": explain_validity(geom)},
                repair_context={"geometry": geom},
            )
        )
    return issues
