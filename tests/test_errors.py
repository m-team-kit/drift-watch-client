"""Test example module."""

import pytest

from drift_monitor import DriftMonitor


@pytest.fixture(scope="function")
def monitor(request_mock, experiment_name, model_id):
    """Create a drift run on the drift monitor server."""
    return DriftMonitor(experiment_name, model_id)


@pytest.mark.parametrize("experiment_name", ["experiment_1"])
@pytest.mark.parametrize("model_id", ["some_model"])
def test_context(monitor):
    """Test the method concept raises out of context error."""
    with pytest.raises(RuntimeError) as excinfo:
        monitor(True, {"threshold": 0.5})
    assert str(excinfo.value) == "Drift monitor context not started."
