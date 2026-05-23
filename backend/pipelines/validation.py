from abc import ABC, abstractmethod
from typing import Any

from models.application import PipelineResult
from models.validation import Issue, IssueCode, Severity
from pipelines.base import BasePipeline
from utils.path_tracker import PathTracker


class ValidationPipeline(BasePipeline, ABC):
    def __init__(self, config):
        super().__init__(config=config)
        self.path_tracker = PathTracker("root")
        self.issues: list[Issue] = []

    @staticmethod
    def create_issue(
        message: str,
        issue_code: IssueCode,
        severity: Severity = Severity.ERROR,
        path: str | None = None,
        detail: dict | None = None,
    ) -> Issue:
        return Issue(
            message=message,
            issue_code=issue_code,
            severity=severity,
            path=path,
            detail=detail,
        )

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)

    def create_and_add_issue(
        self,
        message: str,
        issue_code: IssueCode,
        severity: Severity = Severity.ERROR,
        path: str | None = None,
        detail: dict | None = None,
    ) -> None:
        issue = Issue(
            message=message,
            issue_code=issue_code,
            severity=severity,
            path=path,
            detail=detail,
        )
        self.add_issue(issue)

    @abstractmethod
    def run(self, data: Any) -> PipelineResult:
        pass
