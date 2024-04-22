"""Root conftest.py file for pytest configuration."""

# pylint: disable=redefined-outer-name

import os
from unittest import mock
import uuid

from pytest import fixture

from drift_monitor import DriftMonitor


@fixture(scope="session")
def endpoint():
    """Return the server URL."""
    return os.environ["DRIFT_MONITOR_URL"]


@fixture(scope="session")
def token(request):
    """Return the server token."""
    token = request.param if hasattr(request, "param") else "1234"
    return token


@fixture(scope="function")
def request_mock():
    """Patch requests module with MagicMocks."""
    with mock.patch("drift_monitor.utils.requests") as requests:
        yield requests


@fixture(scope="function")
def monitor(token):
    """Return a DriftMonitor instance."""
    return DriftMonitor("model_1", token)


@fixture(scope="function", autouse=True)
def post_response(request, request_mock, monitor):
    """Return a POST response and patch it in request_mock."""
    if hasattr(request, "param"):
        json = request.param
    else:
        json = {
            "id": f"{uuid.uuid4()}",
            "datetime": "2021-01-01T00:00:00Z",
            "model_id": monitor.model_id,
            "status": "Running",
        }
    request_mock.post.return_value = mock.MagicMock(json=lambda: json)
    return json


@fixture(scope="function")
def with_context(monitor):
    """Opens a context for the monitor."""
    with monitor:
        yield


@fixture(scope="function")
def after_context(monitor):
    """Closes the context for the monitor."""
    with monitor:
        monitor.concept(True, {"threshold": 0.5})
        monitor.data(True, {"threshold": 0.5})


@fixture(scope="function")
def error_context(monitor):
    """Raise an error in the context for the monitor."""
    try:
        with monitor:
            raise ValueError("An error occurred.")
    except ValueError:
        pass


@fixture(scope="function")
def with_concept_drift(monitor):
    """Add concept drift to the monitor."""
    monitor.concept(True, {"threshold": 0.5})


@fixture(scope="function")
def with_data_drift(monitor):
    """Add data drift to the monitor."""
    monitor.data(True, {"threshold": 0.5})
