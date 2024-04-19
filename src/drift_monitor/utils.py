"""Utility functions for drift monitor."""

import requests

from drift_monitor.config import settings


def create_drift(model, token):
    """Create a drift run on the drift monitor server."""
    response = requests.post(
        settings.DRIFT_MONITOR_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={"model_id": model, "status": "Running"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def complete_drift(drift, token):
    """Complete a drift run on the drift monitor server."""
    response = requests.put(
        f"{settings.DRIFT_MONITOR_URL}/{drift['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={**drift, "status": "Completed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
    )
    response.raise_for_status()


def fail_drift(drift, token):
    """Fail a drift run on the drift monitor server."""
    response = requests.put(
        f"{settings.DRIFT_MONITOR_URL}/{drift['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={**drift, "status": "Failed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
    )
    response.raise_for_status()
