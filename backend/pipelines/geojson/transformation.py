from pipelines.transformation import TransformationPipeline
from typing import Any
from models.application import PipelineResult


class GeoJSONTransformationPipeline(TransformationPipeline):
    def run(self, data: Any) -> PipelineResult:
        return PipelineResult(success=False)
