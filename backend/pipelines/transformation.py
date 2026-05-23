from abc import ABC, abstractmethod
from typing import Any

from models.application import PipelineResult
from pipelines.base import BasePipeline


class TransformationPipeline(BasePipeline, ABC):
    @abstractmethod
    def run(self, data: Any) -> PipelineResult:
        pass
