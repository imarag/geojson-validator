from typing import Callable

from shapely.geometry import GeometryCollection, LineString, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon
from shapely.geometry.base import BaseGeometry

from configuration.geometry import GeometryConfig
from exceptions import ValidationError
from models.geojson import geometry_types
from models.validation import Issue, IssueCode, Severity
from utils.path_tracker import PathTracker
from validators.geometry.common import validate_geometry_empty
from validators.geometry.linestring import (
    validate_linestring_closed,
    validate_linestring_consecutive_dups,
    validate_linestring_self_intersection,
)
from validators.geometry.multilinestring import (
    validate_multilinestring_duplicate_lines,
    validate_multilinestring_lines_intersect,
)
from validators.geometry.multipoint import validate_multipoint_duplicate_points
from validators.geometry.multipolygon import validate_multipolygon_intersections
from validators.geometry.polygon import (
    polygon_has_zero_area,
    validate_polygon_exterior_orientation,
    validate_polygon_exterior_self_intersection,
    validate_polygon_interiors_orientation,
    validate_polygon_interiors_self_intersection,
    validate_polygon_is_valid,
)

# TODO: check for nan or inf coordinates


class GeometryValidator:
    def __init__(self, config: GeometryConfig, path_tracker: PathTracker | None = None):
        self.path_tracker = path_tracker if path_tracker is not None else PathTracker()
        self.config = config
        self.issues: list[Issue] = []
        self.VALIDATORS: dict[type[BaseGeometry], Callable] = {
            Point: self.validate_point,
            MultiPoint: self.validate_multipoint,
            LineString: self.validate_linestring,
            MultiLineString: self.validate_multilinestring,
            Polygon: self.validate_polygon,
            MultiPolygon: self.validate_multipolygon,
            GeometryCollection: self.validate_geometry_collection,
        }

    def geometry_empty(self, geom: BaseGeometry) -> bool:
        issues = validate_geometry_empty(geom, self.path_tracker)
        if issues:
            self.issues += issues
            return True
        return False

    def validate_point(self, geom: Point):
        if self.geometry_empty(geom):
            return

    def validate_multipoint(self, geom: MultiPoint):
        if self.geometry_empty(geom):
            return

        for n, point_geom in enumerate(geom.geoms):
            with self.path_tracker.track(n):
                self.validate_point(point_geom)

        # check for duplicate points if allowed
        if not self.config.allow_multipoint_duplicates:
            issues = validate_multipoint_duplicate_points(geom, self.path_tracker)
            self.issues += issues

    def validate_linestring(self, geom: LineString):
        if self.geometry_empty(geom):
            return

        # check consecutive duplicate points in the linestring
        if not self.config.allow_linestring_consecutive_point_dups:
            issues = validate_linestring_consecutive_dups(geom, self.path_tracker)
            self.issues += issues

        # check self-intersection of linestring
        if not self.config.allow_linestring_self_intersection:
            issues = validate_linestring_self_intersection(geom, self.path_tracker)
            self.issues += issues

        # check closed linestring
        if not self.config.allow_linestring_closed:
            issues = validate_linestring_closed(geom, self.path_tracker)
            self.issues += issues

    def validate_multilinestring(self, geom: MultiLineString):
        if self.geometry_empty(geom):
            return

        for n, line_geom in enumerate(geom.geoms):
            with self.path_tracker.track(n):
                self.validate_linestring(line_geom)

        # check duplicated lines
        if not self.config.allow_multilinestring_duplicates:
            issues = validate_multilinestring_duplicate_lines(geom, self.path_tracker)
            self.issues += issues

        # check lines intersect
        if not self.config.allow_multilinestring_lines_intersect:
            issues = validate_multilinestring_lines_intersect(geom, self.path_tracker)
            self.issues += issues

    def validate_polygon(self, geom: Polygon):
        if self.geometry_empty(geom):
            return

        # check polygon zero area - abort
        issues = polygon_has_zero_area(geom, self.path_tracker)
        if issues:
            self.issues += issues
            return

        # check polygon boundaries self-intersections
        validate_polygon_exterior_self_intersection(geom, self.path_tracker)
        validate_polygon_interiors_self_intersection(geom, self.path_tracker)

        # check polygon boundaries orientation
        validate_polygon_exterior_orientation(geom, self.path_tracker)
        validate_polygon_interiors_orientation(geom, self.path_tracker)

        # TODO: check polygon ring relationship
        # self.validate_polygon_holes_inside_shell(geom)
        # self.validate_polygon_holes_overlap(geom)

        # Final authority
        validate_polygon_is_valid(geom, self.path_tracker)

    def validate_multipolygon(self, geom: MultiPolygon):
        if self.geometry_empty(geom):
            return

        for n, poly_geom in enumerate(geom.geoms):
            with self.path_tracker.track(n):
                self.validate_polygon(poly_geom)

        # validate multipolygon intersection
        validate_multipolygon_intersections(geom, self.path_tracker)

    def validate_geometry_collection(self, geom: GeometryCollection):
        if self.geometry_empty(geom):
            return

        for g in geom.geoms:
            validate_func = self.get_geom_validate_function(g)
            validate_func(g)

    def get_geom_validate_function(self, geom: BaseGeometry) -> Callable:
        for geom_type, validator in self.VALIDATORS.items():
            if isinstance(geom, geom_type):
                return validator

        issue = Issue(
            message="An unexpected error occurred while processing this geometry.",
            issue_code=IssueCode.GEOMETRY_UNSUPPORTED_TYPE,
            severity=Severity.ERROR,
            path=self.path_tracker.current(),
            detail={
                "geometry_type": geom.geom_type,
                "supported_geometry_types": geometry_types,
            },
        )

        raise ValidationError(issue)

    def validate_geometry(self, geom_object: BaseGeometry) -> list[Issue]:
        try:
            validation_func = self.get_geom_validate_function(geom_object)
            validation_func(geom_object)
        except ValidationError as exc:
            self.issues.append(exc.issue)
        return self.issues
