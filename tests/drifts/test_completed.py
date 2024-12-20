"""Test module for creation of experiments."""

from unittest import mock

import pytest

from drift_monitor import DriftMonitor, models


@pytest.fixture(scope="function", autouse=True)
def find_mock():
    """Patch requests module with MagicMocks."""
    with mock.patch("drift_monitor.find_experiment") as find:
        yield find


@pytest.fixture(scope="function", autouse=True)
def mocks(request_mock, find_mock, db_experiment, db_drift):
    """Mock the requests module."""
    request_mock.post.return_value = mock.MagicMock(json=db_drift.copy)
    request_mock.put.return_value = mock.MagicMock(json=db_drift.copy)
    find_mock.return_value = models.Experiment(db_experiment)


@pytest.fixture(scope="function")
def monitor(mocks, experiment_name, db_drift):
    """Create a drift run on the drift monitor server."""
    with DriftMonitor(experiment_name, db_drift["model"]) as _monitor:
        pass
    return _monitor


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.parametrize("drift_id", ["00000000-0000-0000-0000-000000000001"])
@pytest.mark.usefixtures("monitor")
def test_request(request_mock):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1
    assert request_mock.put.call_count == 1


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.parametrize("drift_id", ["00000000-0000-0000-0000-000000000001"])
@pytest.mark.usefixtures("monitor")
def test_status(request_mock):
    """Test the drift run was completed on the server."""
    assert request_mock.post.call_args[1]["json"]["job_status"] == "Running"
    assert request_mock.put.call_args[1]["json"]["job_status"] == "Completed"
