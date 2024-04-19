"""Root conftest.py file for pytest configuration."""

from pytest import fixture
from drift_monitor import function_1


@fixture(scope="session")
def fixture_1():
    """Return 1."""
    return function_1()
