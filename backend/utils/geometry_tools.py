import math
from shapely.geometry.base import BaseGeometry
from shapely.geometry import (
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
    LinearRing,
)


class GeometryTools:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_coord(x):
        return isinstance(x, (int, float)) and not math.isnan(x) and not math.isinf(x)

    @staticmethod
    def get_ring_orientation(geom: LinearRing) -> str:
        if not isinstance(geom, LinearRing):
            raise ValueError("A LinearRing must be passed to use this option.")
        return "ccw" if geom.is_ccw else "cw"

    @staticmethod
    def find_linestring_consecutive_point_dups(geom: LineString) -> tuple[list[BaseGeometry], list[int]]:
        """Return consecutive duplicate points and their indices."""
        dup_points: list[BaseGeometry] = []
        dup_indices: list[int] = []

        coords = list(geom.coords)
        prev = coords[0]

        for i, curr in enumerate(coords[1:], start=1):
            if curr == prev:
                dup_points.append(Point(curr))
                dup_indices.append(i)
            prev = curr

        return dup_points, dup_indices

    @staticmethod
    def find_intersecting_polygons(geom: MultiPolygon) -> list[tuple[Polygon, Polygon]]:
        intersecting_pairs: list[tuple[Polygon, Polygon]] = []
        polygons = list(geom.geoms)

        for i in range(len(polygons)):
            for j in range(i + 1, len(polygons)):
                if polygons[i].intersects(polygons[j]):
                    intersecting_pairs.append((polygons[i], polygons[j]))

        return intersecting_pairs

    @staticmethod
    def geometry_empty(geom: BaseGeometry) -> bool:
        """Check if the geometry is empty."""
        return geom.is_empty

    @staticmethod
    def find_duplicate_geometries(geometry: BaseGeometry) -> tuple[list[BaseGeometry], list[int]]:
        dup_geoms: list[BaseGeometry] = []
        dup_indices: list[int] = []

        if not isinstance(geometry, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            return dup_geoms, dup_indices

        geoms_list = list(geometry.geoms)
        seen = []
        for i, geom in enumerate(geoms_list):
            for j, other_geom in enumerate(seen):
                if geom.bounds != other_geom.bounds:
                    continue
                if geom.equals(other_geom):
                    dup_geoms.append(geom)
                    dup_indices.append(i)
                    break  # stop after first match
            seen.append(geom)

        return dup_geoms, dup_indices
