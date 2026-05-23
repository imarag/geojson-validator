from configuration.base import BaseConfig
from configuration.geojson.repair import GeoJSONRepairConfig
from configuration.geojson.transformation import GeoJSONTransformationConfig
from configuration.geojson.validation import GeoJSONValidationConfig
from configuration.wkt.repair import WKTRepairConfig
from configuration.wkt.transformation import WKTTransformationConfig
from configuration.wkt.validation import WKTValidationConfig
from exceptions import InputError, ProcessingError
from models.application import OperationType, SourceType
from pipelines.base import BasePipeline
from pipelines.geojson.repair import GeoJSONRepairPipeline
from pipelines.geojson.transformation import GeoJSONTransformationPipeline
from pipelines.geojson.validation import GeoJSONValidationPipeline
from pipelines.wkt.repair import WKTRepairPipeline
from pipelines.wkt.transformation import WKTTransformationPipeline
from pipelines.wkt.validation import WKTValidationPipeline


class PipelineRegistry:
    """
    Simple registry for mapping (source_type, operation) to pipeline classes.
    """

    def __init__(self):
        """Initialize registry with pipeline mappings."""
        self._load_pipelines()
        self._load_configurations()

    def _load_pipelines(self):
        """Load all pipeline classes."""
        self._pipelines = {
            (SourceType.GEOJSON, OperationType.VALIDATION): GeoJSONValidationPipeline,
            (SourceType.GEOJSON, OperationType.REPAIR): GeoJSONRepairPipeline,
            (SourceType.GEOJSON, OperationType.TRANSFORMATION): GeoJSONTransformationPipeline,
            (SourceType.WKT, OperationType.VALIDATION): WKTValidationPipeline,
            (SourceType.WKT, OperationType.REPAIR): WKTRepairPipeline,
            (SourceType.WKT, OperationType.TRANSFORMATION): WKTTransformationPipeline,
        }

    def _load_configurations(self):
        """Load all configuration classes."""
        self._configurations = {
            (SourceType.GEOJSON, OperationType.VALIDATION): GeoJSONValidationConfig,
            (SourceType.GEOJSON, OperationType.REPAIR): GeoJSONRepairConfig,
            (SourceType.GEOJSON, OperationType.TRANSFORMATION): GeoJSONTransformationConfig,
            (SourceType.WKT, OperationType.VALIDATION): WKTValidationConfig,
            (SourceType.WKT, OperationType.REPAIR): WKTRepairConfig,
            (SourceType.WKT, OperationType.TRANSFORMATION): WKTTransformationConfig,
        }

    def get_pipeline(self, operation: OperationType, source_type: SourceType) -> type[BasePipeline]:
        """
        Get and instantiate a pipeline.
        """
        key = (source_type, operation)

        # Check if exists
        if key not in self._pipelines:
            raise InputError(
                f"No pipeline found for operation '{operation.value}' with source type '{source_type.value}'"
            )

        return self._pipelines[key]

    def get_configuration(self, operation: OperationType, source_type: SourceType) -> type[BaseConfig]:
        """
        Get and instantiate a configuration.
        """
        key = (source_type, operation)

        # Check if exists
        if key not in self._configurations:
            raise InputError(
                f"No config found for operation '{operation.value}' with source type '{source_type.value}'"
            )

        return self._configurations[key]
