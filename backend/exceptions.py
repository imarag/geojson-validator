from models.validation import Issue


class GeoPipelineError(Exception):
    """Base exception for all pipeline-related errors."""

    # This error belongs to my app
    pass


class InputError(GeoPipelineError):
    """Invalid or unsupported user input."""

    # The user gave me something wrong
    pass


class ProcessingError(GeoPipelineError):
    """Internal processing failure (CRS, concat, transform)."""

    # My code or libraries failed while working on valid input
    pass


class ValidationError(GeoPipelineError):
    """Data validation issue (not a crash)."""

    # “The data is valid input, but it violates domain rules”
    def __init__(self, issue: Issue):
        self.issue = issue
        super().__init__(issue.message)
