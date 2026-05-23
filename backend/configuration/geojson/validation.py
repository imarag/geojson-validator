from dataclasses import dataclass, field
from typing import Annotated, Literal, get_args, get_origin

from configuration.base import BaseConfig
from configuration.geometry import GeometryConfig


@dataclass
class GeoJSONValidationConfig(BaseConfig):
    max_key_length: Annotated[
        int,
        {
            "label": "Maximum Key Length",
            "description": "Maximum allowed length for keys in GeoJSON objects.",
            "type": "number",
            "min": 1,
            "max": 500,
            "step": 1,
        },
    ] = 50

    max_top_level_keys: Annotated[
        int,
        {
            "label": "Max Top Level Keys",
            "description": "Maximum number of top-level keys in a GeoJSON object.",
            "type": "number",
            "min": 1,
            "max": 5000,
            "step": 1,
        },
    ] = 1000

    # ---------- GeoJSON-level ----------
    allow_foreign_keys: Annotated[
        bool,
        {
            "label": "Allow Foreign Keys",
            "description": "Whether foreign keys are permitted in GeoJSON objects.",
            "type": "checkbox",
        },
    ] = False

    allow_crs_key: Annotated[
        bool,
        {
            "label": "Allow CRS Key",
            "description": "Whether the 'crs' key is allowed in GeoJSON objects.",
            "type": "checkbox",
        },
    ] = False

    check_bbox: Annotated[
        bool,
        {
            "label": "Check BBox",
            "description": "Validate bbox if it exists; skip validation if absent.",
            "type": "checkbox",
        },
    ] = True

    enforce_dimension: Annotated[
        Literal["2D", "3D", "ignore"],
        {
            "label": "Enforce Dimension",
            "description": "Enforce coordinate dimension: '2D', '3D', or 'ignore' to skip dimension checking.",
            "type": "select",
            "options": [
                {"label": "2D", "value": "2D"},
                {"label": "3D", "value": "3D"},
                {"label": "Ignore", "value": "ignore"},
            ],
        },
    ] = "ignore"

    # ---------- Coordinate-level ----------
    coord_type: Annotated[
        Literal["geographic", "projected"],
        {
            "label": "Coordinate Type",
            "description": "Coordinate system type: 'geographic' or 'projected'.",
            "type": "select",
            "options": [
                {"label": "Geographic", "value": "geographic"},
                {"label": "Projected", "value": "projected"},
            ],
        },
    ] = "geographic"

    # ---------- Geometry (shared) ----------
    geometry: GeometryConfig = field(default_factory=GeometryConfig)

    def __post_init__(self):
        if isinstance(self.geometry, dict):
            self.geometry = GeometryConfig(**self.geometry)
