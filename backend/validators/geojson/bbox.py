from configuration.geojson.validation import GeoJSONValidationConfig
from models.validation import Issue, IssueCode, Severity
from utils.geo_tools import GeoTools
from utils.path_tracker import PathTracker


class BBoxValidator:
    def __init__(
        self,
        config: GeoJSONValidationConfig,
        path_tracker: PathTracker | None = None,
    ):
        self.path_tracker = path_tracker or PathTracker()
        self.config = config
        self.issues: list[Issue] = []

    def create_and_add_issue(
        self,
        message: str,
        issue_code: IssueCode,
        detail: dict,
        description: str = "",
        severity: Severity = Severity.ERROR,
        repair_hint: str | None = None,
        repairable: bool = False,
    ):
        self.issues.append(
            Issue(
                message=message,
                description=description,
                issue_code=issue_code,
                severity=severity,
                path=self.path_tracker.current(),
                detail=detail,
                repair_hint=repair_hint,
                repairable=repairable,
            )
        )

    def validate_bbox_length(self, bbox: list):
        if self.config.enforce_dimension == "2D":
            allowed_lengths = [4]
            length_error = (
                "Bounding box must contain exactly 4 numeric values for 2D "
                "(minLongitude, minLatitude, maxLongitude, maxLatitude)."
            )
        elif self.config.enforce_dimension == "3D":
            allowed_lengths = [6]
            length_error = (
                "Bounding box must contain exactly 6 numeric values for 3D "
                "(minLongitude, minLatitude, minAltitude, "
                "maxLongitude, maxLatitude, maxAltitude)."
            )
        else:
            allowed_lengths = [4, 6]
            length_error = (
                "Bounding box must contain either 4 (2D) or 6 (3D) numeric values: "
                "2D → (minLongitude, minLatitude, maxLongitude, maxLatitude), "
                "3D → (minLongitude, minLatitude, minAltitude, "
                "maxLongitude, maxLatitude, maxAltitude)."
            )
        if len(bbox) not in allowed_lengths:
            self.create_and_add_issue(
                message="Bounding box has an invalid number of values.",
                description=length_error,
                issue_code=IssueCode.BBOX_INVALID_LENGTH,
                detail={
                    "provided_bbox": bbox,
                    "expected_lengths": allowed_lengths,
                },
                repair_hint=(f"Provide a bounding box with {' or '.join(map(str, allowed_lengths))} numeric values."),
                repairable=True,
            )

    def bbox_contains_valid_numbers(self, bbox: list) -> bool:
        invalid_items = [item for item in bbox if not GeoTools.is_finite_number(item)]
        if invalid_items:
            self.create_and_add_issue(
                message="Bounding box contains invalid (non-finite) numeric values.",
                issue_code=IssueCode.BBOX_NOT_FINITE_VALUES,
                detail={
                    "provided_bbox": bbox,
                    "sample_invalid_values": invalid_items[:3],
                },
                repair_hint="Ensure all bounding box values are finite numbers.",
                repairable=True,
            )
            return False
        return True

    def validate_bbox2d(self, bbox: list):
        min_lon, min_lat, max_lon, max_lat = bbox

        if self.config.coord_type == "geographic":
            coords_error = GeoTools.validate_lon_lat_coords(min_lon, min_lat, max_lon, max_lat)
            if coords_error:
                self.create_and_add_issue(
                    message="Invalid bounding box values.",
                    description="For geographic coordinates, longitude must be "
                    "between -180 and 180, and latitude must be between -90 and 90.",
                    issue_code=IssueCode.BBOX_INVALID_COORDS,
                    detail={
                        "provided_bbox": bbox,
                        "coord_type": "geographic",
                        "reason": coords_error,
                    },
                    repair_hint=("Ensure longitude is between -180 and 180 and latitude is between -90 and 90."),
                    repairable=True,
                )

    def validate_bbox3d(self, bbox: list):
        min_lon, min_lat, min_alt, max_lon, max_lat, max_alt = bbox
        self.validate_bbox2d([min_lon, min_lat, max_lon, max_lat])
        # 3D altitude checks can be added later

    def validate(self, bbox: list) -> list[Issue]:
        self.issues = []  # reset per validation call

        with self.path_tracker.track("bbox"):
            self.validate_bbox_length(bbox)

            if not self.bbox_contains_valid_numbers(bbox):
                return self.issues

            if len(bbox) not in (4, 6):
                return self.issues

            if len(bbox) == 4:
                self.validate_bbox2d(bbox)
            else:
                self.validate_bbox3d(bbox)

        return self.issues
