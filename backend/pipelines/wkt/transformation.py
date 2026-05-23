from pipelines.transformation import TransformationPipeline
from typing import Any
from models.application import PipelineResult


class WKTTransformationPipeline(TransformationPipeline):
    def run(self, data: Any) -> PipelineResult:
        return PipelineResult(success=False)
