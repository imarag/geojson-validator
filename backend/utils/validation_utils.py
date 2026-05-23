from models.validation import Issue, IssueCode, Severity


def create_and_add_issue(
    self,
    issues,
    message: str,
    issue_code: IssueCode,
    severity: Severity = Severity.ERROR,
    detail: dict | None = None,
):
    issue = Issue(
        message=message,
        issue_code=issue_code,
        severity=severity,
        path=self.path_tracker.current(),
        detail=detail,
    )
    issues.append(issue)
