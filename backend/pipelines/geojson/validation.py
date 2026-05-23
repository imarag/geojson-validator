import json
from typing import Any

from shapely.geometry import shape

from configuration.geojson.validation import GeoJSONValidationConfig
from exceptions import ValidationError
from models.application import PipelineResult
from models.geojson import geometry_types
from models.validation import Issue, IssueCode, ParamSpec, Severity
from pipelines.validation import ValidationPipeline
from validators.geojson.bbox import BBoxValidator
from validators.geojson.common import validate_crs, validate_foreign_keys
from validators.geojson.structure import (
    geom_type_coord_dim_consistent,
    validate_coords_structure,
    validate_geojson_input,
    validate_geojson_structure,
    validate_key_param,
    validate_type_param,
)
from validators.geometry.base import GeometryValidator


class GeoJSONValidationPipeline(ValidationPipeline):
    def __init__(self, config: GeoJSONValidationConfig):
        super().__init__(config=config)
        self.config = config
        self.issues: list[Issue] = []

    def structure_valid(self, geojson: dict) -> bool:
        issues = validate_geojson_structure(geojson, self.config.max_top_level_keys, self.path_tracker)
        if issues:
            self.issues += issues
            return False
        return True

    def validate_bbox_if_exists(self, geojson: dict):
        if "bbox" not in geojson:
            return

        bbox_issues = self.validate_param(geojson, ParamSpec(name="bbox", dtype=list))
        if bbox_issues:
            return

        if self.config.check_bbox:
            bbox_validator = BBoxValidator(self.config, self.path_tracker)
            bbox_issues = bbox_validator.validate(geojson["bbox"])
            self.issues += bbox_issues

    def validate_crs_if_exists(self, geojson: dict):
        if not self.config.allow_crs_key:
            issues = validate_crs(geojson, self.path_tracker)
            self.issues += issues

    def check_foreign_keys(self, geojson: dict, geojson_type: str):
        issues = validate_foreign_keys(geojson, geojson_type, self.config, self.path_tracker)
        self.issues += issues

    def validate_param(self, geojson: dict, param_spec: ParamSpec) -> list[Issue]:
        if param_spec.optional and param_spec.name not in geojson:
            return []
        param_issues = validate_key_param(geojson, param_spec, Severity.ERROR, self.path_tracker)
        if param_issues:
            self.issues += param_issues
            return param_issues
        return []

    def coordinates_structure_valid(self, coords: list[Any]) -> bool:
        with self.path_tracker.track("coordinates"):
            coords_issues = validate_coords_structure(coords, self.path_tracker, self.config.enforce_dimension)
            if coords_issues:
                self.issues += coords_issues
                return False
        return True

    def features_key_valid(self, geojson: dict) -> bool:
        features_issues = self.validate_param(geojson, ParamSpec(name="features", dtype=list))
        return len(features_issues) == 0

    def geometry_key_valid(self, geojson: dict) -> bool:
        geometry_issues = self.validate_param(geojson, ParamSpec(name="geometry", dtype=(dict, type(None))))
        return len(geometry_issues) == 0

    def geometry_type_key_valid(self, geojson: dict) -> bool:
        type_issues = self.validate_param(geojson, ParamSpec(name="type", dtype=str, allowed_values=geometry_types))
        return len(type_issues) == 0

    def geometries_key_valid(self, geojson: dict) -> bool:
        geometries_issues = self.validate_param(geojson, ParamSpec(name="geometries", dtype=list))
        return len(geometries_issues) == 0

    def coordinates_key_valid(self, geojson: dict) -> bool:
        coordinates_issues = self.validate_param(geojson, ParamSpec(name="coordinates", dtype=list))
        return len(coordinates_issues) == 0

    def geom_type_align_with_coord_dim(self, geojson: dict) -> bool:
        dim_issues = geom_type_coord_dim_consistent(geojson, self.path_tracker)
        if dim_issues:
            self.issues += dim_issues
            return False
        return True

    def validate_feature_keys(self, geojson: dict):
        param_specs = [
            ParamSpec(name="properties", dtype=dict),
            ParamSpec(name="id", dtype=(str, int, type(None)), optional=True),
            ParamSpec(name="type", dtype=str, allowed_values=["Feature"]),
        ]
        for param_spec in param_specs:
            self.validate_param(geojson, param_spec)

    def validate_feature_collection(self, feature_col: dict):
        if not self.structure_valid(feature_col):
            return

        self.validate_bbox_if_exists(feature_col)
        self.validate_crs_if_exists(feature_col)
        self.check_foreign_keys(feature_col, "FeatureCollection")

        # no need to check type - already checked in root

        # if features invalid abort
        if not self.features_key_valid(feature_col):
            return

        with self.path_tracker.track("features"):
            for n, feature in enumerate(feature_col["features"]):
                with self.path_tracker.track(n):
                    self.validate_feature(feature)

    def validate_feature(self, feature: dict):
        if not self.structure_valid(feature):
            return

        self.validate_crs_if_exists(feature)
        self.validate_bbox_if_exists(feature)
        self.check_foreign_keys(feature, "Feature")

        self.validate_feature_keys(feature)

        # if geometry invalid abort
        if not self.geometry_key_valid(feature):
            return

        with self.path_tracker.track("geometry"):
            self.validate_geometry(feature["geometry"])

    def validate_geometry(self, geom: dict):
        if not self.structure_valid(geom):
            return

        self.validate_crs_if_exists(geom)
        self.validate_bbox_if_exists(geom)

        # if type invalid abort
        if not self.geometry_type_key_valid(geom):
            return

        geom_type = geom["type"]
        if geom_type == "GeometryCollection":
            self.validate_geometry_collection(geom)
        else:
            self.validate_single_geometry(geom)

    def validate_geometry_collection(self, geom_col: dict):
        # if geometries invalid abort
        if not self.geometries_key_valid(geom_col):
            return

        self.check_foreign_keys(geom_col, "GeometryCollection")

        with self.path_tracker.track("geometries"):
            for n, geom in enumerate(geom_col["geometries"]):
                with self.path_tracker.track(n):
                    self.validate_geometry(geom)

    def validate_single_geometry(self, single_geom: dict):
        # if coordinates invalid abort

        if not self.coordinates_key_valid(single_geom):
            return

        self.check_foreign_keys(single_geom, "SingleGeometry")

        if not self.coordinates_structure_valid(single_geom["coordinates"]):
            return

        if not self.geom_type_align_with_coord_dim(single_geom):
            return

        try:
            shapely_object = shape(single_geom)
        except Exception:
            self.issues.append(
                Issue(
                    message="Invalid geometry object.",
                    description="The geometry object could not be parsed. "
                    "This may be due to invalid coordinate values or an "
                    "incorrect structure.",
                    issue_code=IssueCode.GEOMETRY_INVALID,
                    severity=Severity.ERROR,
                    path=self.path_tracker.current(),
                )
            )
            return

        geom_validator = GeometryValidator(self.config.geometry, self.path_tracker)
        with self.path_tracker.track("coordinates"):
            geom_issues = geom_validator.validate_geometry(shapely_object)
            self.issues += geom_issues

    def parse_geojson_input(self, data: Any):
        try:
            return json.loads(data)
        except Exception:
            issue = Issue(
                message="Invalid JSON object.",
                issue_code=IssueCode.STRUCTURE_UNSUPPORTED_TYPE,
                severity=Severity.CRITICAL,
                description=(
                    "The input must be a valid JSON object containing key–value pairs. "
                    "Use double quotes instead of single quotes. Replace NaN, None, or missing "
                    "values with null. Boolean values must be lowercase (true/false). "
                    "Finally, remove any trailing commas from objects or arrays."
                ),
                path=self.path_tracker.current(),
            )
        raise ValidationError(issue)

    def run(self, data: Any) -> PipelineResult:
        data = self.parse_geojson_input(data)

        self.logger.info("Step 1: Validate input GeoJSON structure.")
        validate_geojson_input(data, self.path_tracker)

        self.logger.info("Step 2: Validate GeoJSON 'type' parameter existence.")
        validate_type_param(data, self.path_tracker)

        # set the root of the path tracker
        self.path_tracker.root_part = data["type"]

        self.logger.info("Step 3: Validate GeoJSON content.")
        if data["type"] == "FeatureCollection":
            self.validate_feature_collection(data)
        elif data["type"] == "Feature":
            self.validate_feature(data)
        else:
            self.validate_geometry(data)

        return PipelineResult(success=True, errors=[], result=self.issues)
