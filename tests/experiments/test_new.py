"""Test module for creation of drifts."""

# pylint: disable=redefined-outer-name

from unittest import mock

import pytest

import drift_monitor


@pytest.fixture(scope="function", autouse=True)
def mocks(request_mock, experiment):
    """Mock the requests module."""
    request_mock.post.return_value = mock.MagicMock(json=experiment.copy)


@pytest.fixture(scope="function")
def response(request_mock, experiment):
    """Create a drift run on the drift monitor server."""
    return drift_monitor.new_experiment(
        name=experiment.get("name"),
        description=experiment.get("description"),
        public=experiment.get("public", None),
        permissions=experiment.get("permissions", None),
    )


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
def test_request(request_mock, response):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
def test_returns(response, experiment):
    """Test correct return values from new experiment"""
    assert response == experiment
