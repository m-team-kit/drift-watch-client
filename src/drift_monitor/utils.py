"""Utility functions for drift monitor."""

import requests

from drift_monitor.config import settings


def create_drift(model, token):
    """Create a drift run on the drift monitor server."""
    response = requests.post(
        url=f"https://{settings.DRIFT_MONITOR_DOMAIN}/api/drift",
        headers={"Authorization": f"Bearer {token}"},
        json={"model": model, "job_status": "Running"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def complete_drift(drift, token):
    """Complete a drift run on the drift monitor server."""
    _drift = {k: v for k, v in drift.items() if k != "id" and k != "datetime"}
    response = requests.put(
        url=f"https://{settings.DRIFT_MONITOR_DOMAIN}/api/drift/{drift['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={**_drift, "job_status": "Completed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def fail_drift(drift, token):
    """Fail a drift run on the drift monitor server."""
    _drift = {k: v for k, v in drift.items() if k != "id" and k != "datetime"}
    response = requests.put(
        url=f"{settings.DRIFT_MONITOR_DOMAIN}/api/drift/{drift['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={**drift, "job_status": "Failed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
