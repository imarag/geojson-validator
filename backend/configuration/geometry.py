from dataclasses import dataclass
from typing import Annotated

from configuration.base import BaseConfig


@dataclass
class GeometryConfig(BaseConfig):
    min_distance_between_points: Annotated[
        float | None,
        {
            "label": "Minimum Distance Between Points",
            "description": "Minimum distance (in the same units as the coordinates) that each point in a MultiPoint geometry must maintain from all other points.",
            "type": "number",
            "min": 0,
            "step": 0.01,
        },
    ] = 0

    allow_multipoint_duplicates: Annotated[
        bool,
        {
            "label": "Allow MultiPoint Duplicates",
            "description": "Whether duplicate points in MultiPoint geometries are allowed.",
            "type": "checkbox",
        },
    ] = True

    allow_linestring_self_intersection: Annotated[
        bool,
        {
            "label": "Allow LineString Self-Intersection",
            "description": "Allow LineStrings that self-intersect.",
            "type": "checkbox",
        },
    ] = False

    allow_linestring_closed: Annotated[
        bool,
        {
            "label": "Allow LineString Closed Loops",
            "description": "Allow LineStrings that are closed loops.",
            "type": "checkbox",
        },
    ] = True

    allow_linestring_consecutive_point_dups: Annotated[
        bool,
        {
            "label": "Allow LineString Consecutive Duplicates",
            "description": "Allow LineString to have duplicated consecutive points.",
            "type": "checkbox",
        },
    ] = False

    allow_multilinestring_duplicates: Annotated[
        bool,
        {
            "label": "Allow MultiLineString Duplicates",
            "description": "Whether duplicate lines in MultiLineString geometries are allowed.",
            "type": "checkbox",
        },
    ] = True

    allow_multilinestring_lines_intersect: Annotated[
        bool,
        {
            "label": "Allow MultiLineString Intersections",
            "description": "Whether to allow lines in MultiLineString geometries to intersect each other.",
            "type": "checkbox",
        },
    ] = True

    allow_zero_area_polygon: Annotated[
        bool,
        {
            "label": "Allow Zero Area Polygon",
            "description": "Allow Polygon with zero area.",
            "type": "checkbox",
        },
    ] = False

    allow_non_simple_polygons: Annotated[
        bool,
        {
            "label": "Allow Non-Simple Polygons",
            "description": "Allow polygons that are non-simple (self-intersecting).",
            "type": "checkbox",
        },
    ] = True

    check_exterior_ccw: Annotated[
        bool,
        {
            "label": "Check Exterior Counter-Clockwise",
            "description": "Check that exterior ring is counter-clockwise.",
            "type": "checkbox",
        },
    ] = False

    check_interior_cw: Annotated[
        bool,
        {
            "label": "Check Interior Clockwise",
            "description": "Check that interior rings are clockwise.",
            "type": "checkbox",
        },
    ] = False

    allow_polygons_self_intersection: Annotated[
        bool,
        {
            "label": "Allow Polygon Self-Intersection",
            "description": "Polygons may self-intersect.",
            "type": "checkbox",
        },
    ] = False
