"""Test module for creation of drifts."""

# pylint: disable=redefined-outer-name

from unittest import mock

import pytest

import drift_monitor


@pytest.fixture(scope="function", autouse=True)
def mocks(request_mock, db_experiment):
    """Mock the requests module."""
    request_mock.post.return_value = mock.MagicMock(json=db_experiment.copy)


@pytest.fixture(scope="function")
def experiment(request_mock, db_experiment):
    """Create a drift run on the drift monitor server."""
    return drift_monitor.new_experiment(
        name=db_experiment.get("name"),
        description=db_experiment.get("description"),
        public=db_experiment.get("public", None),
        permissions=db_experiment.get("permissions", None),
    )


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.usefixtures("experiment")
def test_request(request_mock):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
def test_returns(experiment, db_experiment):
    """Test correct return values from new experiment"""
    assert experiment.__dict__ == db_experiment
