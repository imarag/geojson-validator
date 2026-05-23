from pipelines.validation import ValidationPipeline
from typing import Any
from models.application import PipelineResult


class WKTValidationPipeline(ValidationPipeline):
    def run(self, data: Any) -> PipelineResult:
        return PipelineResult(success=False)
