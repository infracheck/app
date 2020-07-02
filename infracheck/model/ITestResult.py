import typing as t


class ITestResult(object):
    # TODO Implement
    pass


class TestResult(t.TypedDict):
    succeeded: int
    failures: int
    errors: int
    total: int
    message: str
    data: t.Any
