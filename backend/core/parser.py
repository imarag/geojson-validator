import json
from io import BytesIO
from typing import Any

import geopandas as gpd

from exceptions import InputError
from models.application import SourceType


class ParserHandler:
    """
    Parses geospatial data with smart type detection.

    Supports explicit format specification or automatic detection.
    """

    def parse(self, input_data: Any) -> tuple[Any, SourceType]:
        """Auto-detect format and parse."""

        # check for GeoDataFrame
        if isinstance(input_data, gpd.GeoDataFrame):
            return input_data, SourceType.GEODATAFRAME

        # Assume dict -> GeoJSON
        if isinstance(input_data, dict):
            return self._parse_geojson_dict(input_data), SourceType.GEOJSON

        # Bytes -> use extension hint or try multiple formats
        if isinstance(input_data, bytes):
            return self._parse_bytes_auto(input_data)

        return self._parse_geojson_str(input_data), SourceType.GEOJSON

        raise InputError(f"Cannot detect format for type: {type(input_data)}")

    def _parse_bytes_auto(self, byte_data: bytes) -> tuple[Any, SourceType]:
        """Auto-detect bytes format using filename and content sniffing."""

        # Content sniffing: Try GeoJSON first (most common)
        try:
            decoded = byte_data.decode("utf-8")
            return self._parse_geojson_str(decoded), SourceType.GEOJSON
        except Exception:
            pass

        # Try GeoPandas auto-detection for binary formats
        try:
            gdf = gpd.read_file(BytesIO(byte_data))
            # Infer format from driver if possible
            return gdf, SourceType.GEODATAFRAME
        except Exception:
            raise InputError("Cannot auto-detect format from bytes")

    @staticmethod
    def _parse_geojson_dict(geojson_dict: dict) -> dict:
        """Parse and validate GeoJSON dictionary."""
        if not isinstance(geojson_dict, dict):
            raise InputError("Expected dict for GeoJSON")
        if not geojson_dict:
            raise InputError("GeoJSON dict is empty")
        return geojson_dict

    @staticmethod
    def _parse_geojson_str(geojson_str: str) -> str:
        """Parse GeoJSON string."""
        try:
            return str(geojson_str).strip()
        except json.JSONDecodeError as e:
            raise InputError(f"Invalid JSON: {e}") from e
