from datetime import datetime
from typing import Any

from configuration.base import BaseConfig
from core.logger import get_logger
from core.parser import ParserHandler
from exceptions import GeoPipelineError, InputError, ProcessingError, ValidationError
from models.application import OperationType, PipelineResult, SourceType
from pipelines.base import BasePipeline
from registry import PipelineRegistry


class Orchestrator:
    """
    Orchestrates the complete geospatial data processing workflow.
    """

    def __init__(
        self,
        pipeline_registry: PipelineRegistry,
        parser: ParserHandler,
        config: dict | None = None,
    ):
        """
        Initialize the orchestrator.
        """
        self._validate_parser(parser)
        self._validate_registry(pipeline_registry)
        self._validate_config(config)
        self.pipeline_registry = pipeline_registry
        self.parser = parser
        self.config = config if config is not None else {}
        self.logger = get_logger(__name__)

    def _validate_parser(self, parser):
        if not callable(getattr(parser, "parse", None)):
            raise InputError("Parser must expose parse method.")

    def _validate_registry(self, registry):
        if not callable(getattr(registry, "get_pipeline", None)):
            raise InputError("Registry must expose get_pipeline(operation)")

        if not callable(getattr(registry, "get_configuration", None)):
            raise InputError("Registry must expose get_configuration(operation)")

    def _validate_config(self, config):
        if config is not None and not isinstance(config, dict):
            raise InputError("Config must be a dictionary if provided.")

    def _print_initial_run_info(self, data: Any, operation: str):
        self.logger.info("=" * 60)
        self.logger.info("Starting pipeline execution. Provided info:")
        self.logger.info(f"data type: {type(data) if data else 'NOT PROVIDED'}")
        self.logger.info(f"operation: '{operation if operation else 'NOT PROVIDED'}'")
        self.logger.info("=" * 60)

    def _print_final_run_info(self, start_time: datetime, result: PipelineResult):
        execution_time = (datetime.now() - start_time).total_seconds()
        status = (
            "✅ Pipeline completed successfully"
            if result.success
            else "❌ Pipeline failed"
        )
        self.logger.info("=" * 60)
        self.logger.info(f"{status} in {execution_time:.2f}s")
        self.logger.info("=" * 60)

    def _validate_operation(self, operation: str) -> OperationType:
        """
        Validate and convert operation string to enum.
        """
        try:
            operation_type = OperationType(operation.strip().lower())
            self.logger.info(f"Operation type: {operation_type.value}")
            return operation_type
        except ValueError as err:
            supported = OperationType.list_operations()
            raise InputError(
                f"Invalid operation '{operation}'. Supported operations: {', '.join(supported)}"
            ) from err

    def _get_pipeline(
        self, operation_type: OperationType, source_type: SourceType, config: BaseConfig
    ) -> BasePipeline:
        """
        Get appropriate pipeline from registry.
        """
        try:
            pipeline_class = self.pipeline_registry.get_pipeline(
                operation=operation_type, source_type=source_type
            )
            self.logger.info(f"Selected pipeline: {pipeline_class.__name__}")
            return pipeline_class(config)
        except InputError:
            raise
        except Exception as e:
            raise InputError("Failed to parse input data") from e

    def _parse_input(self, data: Any) -> tuple[Any, SourceType]:
        """
        Parse input data using the parser handler.
        """
        try:
            parsed_data, detected_source_type = self.parser.parse(data)
            self.logger.info(
                f"Input data parsed successfully as source type: {detected_source_type.value}"
            )
            return parsed_data, detected_source_type
        except InputError:
            raise
        except Exception as e:
            raise InputError("Failed to parse input data") from e

    def _initialize_config(
        self, operation_type: OperationType, source_type: SourceType
    ) -> BaseConfig:
        """Initialize and validate configuration."""
        try:
            pipeline_config_class = self.pipeline_registry.get_configuration(
                operation=operation_type, source_type=source_type
            )
            self.logger.info("Configuration initialized.")
            return pipeline_config_class(**self.config)
        except InputError:
            raise
        except Exception as e:
            raise InputError(f"Failed to initialize the configuration: {str(e)}") from e

    def _execute_pipeline(
        self, pipeline: BasePipeline, parsed_data: Any
    ) -> PipelineResult:
        """
        Execute the selected pipeline.
        """
        try:
            return pipeline.run(parsed_data)
        except ValidationError as e:
            return PipelineResult(success=True, errors=[], result=[e.issue])
        except Exception as e:
            raise ProcessingError(f"Pipeline execution failed: {str(e)}") from e

    def _create_error_result(self, error_message: str) -> PipelineResult:
        """
        Create error result with metadata.
        """
        return PipelineResult(success=False, errors=[error_message], result=None)

    def execute(
        self,
        data: Any,
        operation: str,
    ) -> PipelineResult:
        """
        Execute pipeline on input data.
        """
        start_time = datetime.now()

        self._print_initial_run_info(data, operation)

        try:
            self.logger.info("Step 1: Parsing input data...")
            parsed_data, detected_source_type = self._parse_input(data)

            self.logger.info(f"Step 2: Validating operation type: {operation}")
            operation_type = self._validate_operation(operation)

            self.logger.info("Step 3: Initializing configuration...")
            config = self._initialize_config(operation_type, detected_source_type)

            self.logger.info(
                f"Step 3: Selecting pipeline for {operation_type.value} + {detected_source_type.value}"
            )
            pipeline = self._get_pipeline(operation_type, detected_source_type, config)

            self.logger.info("Step 4: Executing pipeline...")
            result = self._execute_pipeline(pipeline, parsed_data)

            self._print_final_run_info(start_time=start_time, result=result)
            return result

        except GeoPipelineError as e:
            self.logger.error(f"❌ Pipeline failed: {str(e)}")
            return self._create_error_result(str(e))

        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
            return self._create_error_result(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    invalid_geojson = {
        "type": None,
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
                "properties": {"prop0": "value0"},
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [102.0, 0.0],
                        [103.0, 1.0],
                        [104.0, 0.0],
                        [105.0, 1.0],
                    ],
                },
                "properties": {"prop0": "value0", "prop1": 0.0},
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [100.0, 0.0],
                            [101.0, 0.0],
                            [101.0, 1.0],
                            [100.0, 1.0],
                            [100.0, 0.0],
                        ]
                    ],
                },
                "properties": {"prop0": "value0", "prop1": {"this": "that"}},
            },
        ],
    }

    config = {
        "check_bbox": True,
        "geometry": {
            "allow_multipoint_duplicates": True,
            "allow_multilinestring_duplicates": False,
        },
    }
    from dataclasses import asdict

    orch = Orchestrator(
        pipeline_registry=PipelineRegistry(), parser=ParserHandler(), config=config
    )
    res = orch.execute(data=invalid_geojson, operation="validation")
    for iss in res.result or []:
        iss_dict = asdict(iss)
        for key in iss_dict:
            print(key, "-> ", iss_dict[key])
        print()
