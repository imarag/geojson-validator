from pipelines.repair import RepairPipeline
from typing import Any
from models.application import PipelineResult


class GeoJSONRepairPipeline(RepairPipeline):
    def run(self, data: Any) -> PipelineResult:
        return PipelineResult(success=False)
