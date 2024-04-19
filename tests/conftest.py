"""Root conftest.py file for pytest configuration."""

# pylint: disable=redefined-outer-name

from pytest import fixture
from drift_monitor import DriftMonitor
from unittest import mock


@fixture(scope="package")
def mock_server(request):
    """Patch request module to mock a server."""
    json = request.param if hasattr(request, "param") else {}
    response = mock.MagicMock(json=lambda: json)
    server = mock.MagicMock(return_value=response)
    return server


@fixture(scope="package")
def patch_requests(mock_server):
    """Patch requests module."""
    with mock.patch("drift_monitor.utils.requests") as requests:
        requests.return_value = mock_server
        yield requests


@fixture(scope="module")
def monitor():
    """Return a DriftMonitor instance."""
    return DriftMonitor("model_1", token="1234")


@fixture(scope="module")
def with_context(monitor):
    """Opens a context for the monitor."""
    with monitor:
        yield monitor


@fixture(scope="module")
def with_concept_drift(monitor):
    """Add concept drift to the monitor."""
    monitor.concept(True, {"threshold": 0.5})


@fixture(scope="module")
def with_data_drift(monitor):
    """Add data drift to the monitor."""
    monitor.data(True, {"threshold": 0.5})
