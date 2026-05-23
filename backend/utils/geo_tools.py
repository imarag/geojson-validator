import decimal
import json
import math
from typing import Any, Generator, List

from shapely import from_geojson
from shapely.errors import ShapelyError
from shapely.geometry import (
    GeometryCollection,
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry


class GeoTools:
    """Utility class for GeoJSON/Shapely geometry operations and validation."""

    def __init__(self):
        pass

    @staticmethod
    def get_ascii_control_chars(s: str) -> list[str]:
        return [ch for ch in s if ord(ch) < 32 or ord(ch) == 127]

    @staticmethod
    def is_finite_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    @staticmethod
    def all_finite_numbers(values: list[Any]) -> bool:
        return isinstance(values, list) and all(GeoTools.is_finite_number(v) for v in values)

    @staticmethod
    def count_number_decimals(num: float | str, normalize=False) -> int:
        try:
            d = decimal.Decimal(str(num))
        except decimal.InvalidOperation:
            return -1
        if normalize:
            d = d.normalize()
        return -d.as_tuple().exponent if d.as_tuple().exponent < 0 else 0

    @staticmethod
    def validate_lon_lat(lon: float, lat: float) -> str | None:
        if not GeoTools.is_finite_number(lon):
            return "Longitude is not a finite number."
        if not GeoTools.is_finite_number(lat):
            return "Latitude is not a finite number."
        if not -180 <= lon <= 180:
            return f"Longitude {lon} out of range. Must be between -180 and 180."
        if not -90 <= lat <= 90:
            return f"Latitude {lat} out of range. Must be between -90 and 90."
        return None

    @staticmethod
    def validate_lon_lat_coords(lon1: float, lat1: float, lon2: float, lat2: float) -> str | None:
        err = GeoTools.validate_lon_lat(lon1, lat1)
        if err:
            return f"Lower-left coordinates invalid: {err}"
        err = GeoTools.validate_lon_lat(lon2, lat2)
        if err:
            return f"Upper-right coordinates invalid: {err}"
        if not (lon1 < lon2):
            return f"Invalid longitude range: {lon1} must be less than {lon2}."
        if not (lat1 < lat2):
            return f"Invalid latitude range: {lat1} must be less than {lat2}."
        return None

    @staticmethod
    def validate_elevation(elevation: float) -> str | None:
        if not GeoTools.is_finite_number(elevation):
            return "Elevation is not a finite number."
        return None

    @staticmethod
    def validate_elevation_values(min_elev: float, max_elev: float) -> str | None:
        err = GeoTools.validate_elevation(min_elev)
        if err:
            return f"Invalid minimum elevation: {err}"
        err = GeoTools.validate_elevation(max_elev)
        if err:
            return f"Invalid maximum elevation: {err}"
        if min_elev >= max_elev:
            return "Invalid elevation range. Minimum elevation must be less than maximum elevation."
        return None

    @staticmethod
    def validate_numeric_structure(data, total_numbers_list: list[int] | int | None = None) -> str | None:
        """
        Validate nested coordinate arrays:
        - all numbers,
        - consistent nesting,
        - valid length if specified.
        """

        if not isinstance(data, (list, tuple)) or not data:
            return "Input must be a non-empty array of numbers or nested arrays of numbers."

        if total_numbers_list is None:
            total_numbers_list = []
        elif isinstance(total_numbers_list, int):
            total_numbers_list = [total_numbers_list]

        lengths_seen = set()

        def validate(item) -> str | None:
            if isinstance(item, (int, float)):
                if not GeoTools.is_finite_number(item):
                    return f"Found non-finite number in coordinates: {item}."
                return None

            if not isinstance(item, (list, tuple)):
                return f"Found invalid structure: expected a list or tuple: {item}"

            if not item:
                return "There is an empty array inside the data."

            # Leaf: all numbers
            if all(isinstance(x, (int, float)) for x in item):
                if total_numbers_list and len(item) not in total_numbers_list:
                    return f"Invalid coordinate length. Must be one of {total_numbers_list}."
                lengths_seen.add(len(item))
                return None

            # Nested: all arrays
            if all(isinstance(x, (list, tuple)) for x in item):
                for x in item:
                    err = validate(x)
                    if err:
                        return err
                return None

            # Mixed types
            mixed_types = ", ".join(set(type(x).__name__ for x in item))
            return f"The array contains invalid or mixed types at the same level: {mixed_types}."

        err_msg = validate(data)
        if err_msg:
            return err_msg

        if len(lengths_seen) > 1:
            return f"Coordinate arrays must have a consistent length, but found lengths: {lengths_seen}."

        return None

    @staticmethod
    def get_coord_depth(coords):
        if isinstance(coords, (list, tuple)):
            if not coords:
                return None
            inner_depths = {GeoTools.get_coord_depth(c) for c in coords}
            if len(inner_depths) != 1:
                return None
            depth = inner_depths.pop()
            return None if depth is None else depth + 1
        elif GeoTools.is_finite_number(coords):
            return 0
        return None

    @staticmethod
    def unique_coordinates_counts(coords: list | tuple) -> set[int]:
        unique_counts: set[int] = set()

        def count_numbers(sub_coords: list | tuple):
            if all(GeoTools.is_finite_number(item) for item in sub_coords):
                unique_counts.add(len(sub_coords))
            elif all(isinstance(item, (list, tuple)) for item in sub_coords):
                for item in sub_coords:
                    count_numbers(item)
            else:
                unique_counts.add(-1)

        if isinstance(coords, (list, tuple)):
            count_numbers(coords)

        return unique_counts

    @staticmethod
    def flatten_nested_number_lists(coords: list) -> list[list]:
        """Flatten nested coordinate arrays to individual points."""
        if not isinstance(coords, list):
            return []
        if coords and isinstance(coords[0], (int, float)):
            return [coords]
        result = []
        for item in coords:
            result.extend(GeoTools.flatten_nested_number_lists(item))
        return result

    @staticmethod
    def check_key_leading_trailing_spaces(key: str) -> str | None:
        leading_space = key[0].isspace()
        trailing_space = key[-1].isspace()
        if leading_space or trailing_space:
            if leading_space and trailing_space:
                return f"Leading and trailing spaces detected in key '{key}'."
            elif leading_space:
                return f"Leading spaces detected in key '{key}'."
            else:
                return f"Trailing spaces detected in key '{key}'."

    @staticmethod
    def validate_json_key_value(geojson: dict[Any, Any], key: Any, max_length: int = 50) -> list[str]:
        issues: list[str] = []
        if not isinstance(geojson, dict):
            issues.append(f"Expected a JSON object (dict), got {type(geojson).__name__}.")
            return issues
        if not isinstance(key, str):
            issues.append(f"Invalid key: {key!r} (type {type(key).__name__}). Keys must be strings.")
            return issues
        if key not in geojson:
            issues.append(f"Key '{key}' not found in the JSON object.")
            return issues
        if key.strip() == "":
            issues.append("Invalid key: key cannot be empty or only whitespace.")
        key_spaces_err = GeoTools.check_key_leading_trailing_spaces(key)
        if key_spaces_err:
            issues.append(key_spaces_err)
        if len(key) > max_length:
            issues.append(f"Found key '{key}' with too many characters (max {max_length}).")
        control_chars = GeoTools.get_ascii_control_chars(key)
        if control_chars:
            issues.append(f"Found invalid character(s) in key '{key}': {control_chars}.")
        value = geojson[key]
        if value is None or isinstance(value, (bool, int, str, dict, list)):
            pass
        elif isinstance(value, float):
            if math.isnan(value):
                issues.append(f"Invalid number at key '{key}': NaN is not allowed.")
            if math.isinf(value):
                issues.append(f"Invalid number at key '{key}': Infinity is not allowed.")
        else:
            issues.append(f"Non-JSON-serializable value at key '{key}': type={type(value).__name__}.")
        return issues

    @staticmethod
    def get_linestring_endpoints(line: LineString) -> tuple[Point, Point]:
        if not isinstance(line, LineString):
            raise ValueError("Invalid geometry passed. Expects LineString")
        return Point(line.coords[0]), Point(line.coords[-1])

    @staticmethod
    def find_duplicate_geometries(geometry: BaseGeometry, max_examples: int = 3) -> dict | None:
        """Find duplicate geometries within Multi* geometries or single geometry."""
        geoms: List[BaseGeometry] = []
        if isinstance(geometry, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            geoms.extend(list(geometry.geoms))
        else:
            geoms.append(geometry)
        duplicate_pairs = []
        total_dups = 0
        for i in range(len(geoms)):
            for j in range(i):
                if geoms[i].bounds != geoms[j].bounds:
                    continue
                if geoms[i].equals(geoms[j]):
                    total_dups += 1
                    if len(duplicate_pairs) < max_examples:
                        duplicate_pairs.append((j, i))
        if total_dups == 0:
            return None
        return {
            "geometry_type": geoms[0].geom_type if geoms else None,
            "duplicate_count": total_dups,
            "total_geometries": len(geoms),
            "example_indices": duplicate_pairs,
        }

    @staticmethod
    def extract_coords(geom: BaseGeometry) -> Generator:
        """Yield all coordinates from any Shapely geometry, including multi-geometries and GeometryCollections."""
        if isinstance(geom, Point):
            yield list(geom.coords)[0]
        elif isinstance(geom, LineString):
            yield from (list(c) for c in geom.coords)
        elif isinstance(geom, Polygon):
            yield from (list(c) for c in geom.exterior.coords)
            for interior in geom.interiors:
                yield from (list(c) for c in interior.coords)
        elif isinstance(geom, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            for g in geom.geoms:
                yield from GeoTools.extract_coords(g)
        else:
            raise ValueError(f"Unsupported geometry type: {type(geom).__name__}")
