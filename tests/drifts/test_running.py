"""Test module for creation of experiments."""

from unittest import mock

import pytest

from drift_monitor import DriftMonitor


@pytest.fixture(scope="function", autouse=True)
def find_mock():
    """Patch requests module with MagicMocks."""
    with mock.patch("drift_monitor.find_experiment") as find:
        yield find


@pytest.fixture(scope="function", autouse=True)
def mocks(request_mock, find_mock, experiment, drift):
    """Mock the requests module."""
    request_mock.post.return_value = mock.MagicMock(json=drift.copy)
    find_mock.return_value = experiment


@pytest.fixture(scope="function")
def monitor(mocks, experiment_name, drift):
    """Create a drift run on the drift monitor server."""
    with DriftMonitor(experiment_name, drift["model"]) as _monitor:
        yield _monitor


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.parametrize("drift_id", ["00000000-0000-0004-0001-000000000004"])
def test_request(request_mock, monitor):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.parametrize("drift_id", ["00000000-0000-0004-0001-000000000004"])
def test_status(request_mock, monitor):
    """Test the drift run was completed on the server."""
    assert monitor._drift["job_status"] == "Running"
