from abc import ABC, abstractmethod
from typing import Any

from configuration.base import BaseConfig
from core.logger import get_logger
from models.application import PipelineResult
from utils.geo_tools import GeoTools


class BasePipeline(ABC):
    def __init__(self, config: BaseConfig):
        self.logger = get_logger(__name__)
        self.geo_tools = GeoTools()
        self.config = config

    @abstractmethod
    def run(self, data: Any) -> PipelineResult:
        pass
