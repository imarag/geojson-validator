from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

from models.validation import ParamSpec

type GeoJSON = dict[str, Any]
type BBox = list
type Coords = list
type GeometryType = Literal[
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
]
type GeoJsonType = Literal[GeometryType] | Literal["FeatureCollection", "Feature"]
type SingleGeometryType = Literal[
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


class GeoJsonBase(BaseModel):
    class Config:
        extra = "ignore"  # 'ignore', 'allow', or 'forbid'


class SingleGeometrySchema(GeoJsonBase):
    type: SingleGeometryType
    coordinates: Coords


class GeometryCollectionSchema(GeoJsonBase):
    type: Literal["GeomppetryCollection"]
    geometries: list
    bbox: BBox | None = None


class PointSchema(GeoJsonBase):
    type: Literal["Point"]
    coordinates: Coords


class MultiPointSchema(GeoJsonBase):
    type: Literal["MultiPoint"]
    coordinates: list[Coords]


class LineStringSchema(GeoJsonBase):
    type: Literal["LineString"]
    coordinates: list[Coords]


class MultiLineStringSchema(GeoJsonBase):
    type: Literal["MultiLineString"]
    coordinates: list[list[Coords]]


class PolygonSchema(GeoJsonBase):
    type: Literal["Polygon"]
    coordinates: list[list[Coords]]


class MultiPolygonSchema(GeoJsonBase):
    type: Literal["MultiPolygon"]
    coordinates: list[list[list[Coords]]]


class GeometrySchema(GeoJsonBase):
    type: GeometryType
    coordinates: list
    geometries: list
    bbox: BBox | None = None


class FeatureSchema(GeoJsonBase):
    type: Literal["Feature"]
    geometry: dict | None
    properties: dict[str, Any] | None
    id: str | int | None = None
    bbox: BBox | None = None


class FeatureCollectionSchema(GeoJsonBase):
    type: Literal["FeatureCollection"]
    features: list
    bbox: BBox | None = None


geometry_types = [
    "Point",
    "LineString",
    "Polygon",
    "MultiPoint",
    "MultiLineString",
    "MultiPolygon",
    "GeometryCollection",
]

geojson_types = geometry_types + ["FeatureCollection", "Feature"]
single_geometry_types = geometry_types[:6]
case_mapping = {
    "featurecollection": "FeatureCollection",
    "feature": "Feature",
    "geometrycollection": "GeometryCollection",
    "point": "Point",
    "linestring": "LineString",
    "polygon": "Polygon",
    "multipoint": "MultiPoint",
    "multilinestring": "MultiLineString",
    "multipolygon": "MultiPolygon",
}

geojson_schema_mapping = {
    "Point": PointSchema,
    "LineString": LineStringSchema,
    "Polygon": PolygonSchema,
    "MultiPoint": MultiPointSchema,
    "MultiLineString": MultiLineStringSchema,
    "MultiPolygon": MultiPolygonSchema,
    "GeometryCollection": GeometryCollectionSchema,
    "FeatureCollection": FeatureCollectionSchema,
    "Feature": FeatureSchema,
}

OPTIONAL_KEYS = ["bbox", "id"]
REQUIRED_KEYS = {
    "FeatureCollection": ["type", "features"],
    "Feature": ["type", "geometry", "properties"],
    "GeometryCollection": ["type", "geometries"],
    "SingleGeometry": ["type", "coordinates"],
    "Point": ["type", "coordinates"],
    "LineString": ["type", "coordinates"],
    "Polygon": ["type", "coordinates"],
    "MultiPoint": ["type", "coordinates"],
    "MultiLineString": ["type", "coordinates"],
    "MultiPolygon": ["type", "coordinates"],
    "": ["type"],  # fallback for unknown / general type
}
GEOMETRY_DEPTH = {
    "Point": 1,
    "MultiPoint": 2,
    "LineString": 2,
    "MultiLineString": 3,
    "Polygon": 3,
    "MultiPolygon": 4,
}
