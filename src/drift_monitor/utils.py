"""Utility functions for drift monitor."""

import requests

from drift_monitor.config import settings, monitor_url


def create_drift(model, token):
    """Create a drift run on the drift monitor server."""
    response = requests.post(
        url=f"{monitor_url}/drift",
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
        url=f"{monitor_url}/drift/{drift['id']}",
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
        url=f"{monitor_url}/drift/{drift['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={**_drift, "job_status": "Failed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def register(token):
    """Registers the token user in the application database."""
    response = requests.post(
        url=f"{monitor_url}/user",
        headers={"Authorization": f"Bearer {token}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def update_email(token):
    """Update the email of the token user in the application database."""
    response = requests.put(
        url=f"{monitor_url}/user/self",
        headers={"Authorization": f"Bearer {token}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
