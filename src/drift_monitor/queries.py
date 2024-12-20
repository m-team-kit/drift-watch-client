"""Query functions for drift watch server."""

from typing import List
from uuid import UUID

import marshmallow as ma
import requests

from drift_monitor import models, schemas
from drift_monitor.config import access_token, settings

# Entitlements: API Methods to list, entitlements.


def get_entitlements() -> List[str]:
    """Get the entitlements of the token user."""
    response = requests.get(
        url=f"{settings.monitor_url}/entitlements",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()["items"]


# Experiments: API Methods to list, register, edit and remove experiments.


def search_experiment(query, page=1, page_size=10):
    """Search for experiments on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/experiment/search",
        headers={"Authorization": f"Bearer {access_token()}"},
        params={"page": page, "page_size": page_size},
        json=query,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return (
        [models.Experiment(data) for data in response.json()],
        response.headers["X-Pagination"],
    )


def post_experiment(attributes) -> models.Experiment:
    """Create a new experiment on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/experiment",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=schemas.CreateExperiment().load(attributes),
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Experiment(response.json())


def get_experiment(experiment_id: UUID) -> models.Experiment:
    """Get an experiment from the drift monitor server."""
    response = requests.get(
        url=f"{settings.monitor_url}/experiment/{experiment_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Experiment(response.json())


def put_experiment(experiment: models.Experiment) -> models.Experiment:
    """Update an experiment on the drift monitor server."""
    response = requests.put(
        url=f"{settings.monitor_url}/experiment/{experiment.id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=schemas.UpdateExperiment(unknown=ma.EXCLUDE).dump(experiment),
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Experiment(response.json())


def delete_experiment(experiment_id: UUID) -> None:
    """Delete an experiment from the drift monitor server."""
    response = requests.delete(
        url=f"{settings.monitor_url}/experiment/{experiment_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return None


# Drifts: API Methods to list, create, complete and fail drift runs.


def search_drift(experiment, query, page=1, page_size=10):
    """Search for drift runs on the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.post(
        url=f"{settings.monitor_url}/{exp_route}/drift/search",
        headers={"Authorization": f"Bearer {access_token()}"},
        params={"page": page, "page_size": page_size},
        json=query,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return (
        [models.Drift(data) for data in response.json()],
        response.headers["X-Pagination"],
    )


def post_drift(experiment, attributes) -> models.Drift:
    """Create a new drift run on the drift monitor server."""
    exp_route = f"experiment/{experiment.id}"
    response = requests.post(
        url=f"{settings.monitor_url}/{exp_route}/drift",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=schemas.CreateDrift().load(attributes),
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Drift(response.json())


def get_drift(experiment, drift_id: UUID) -> models.Drift:
    """Get a drift run from the drift monitor server."""
    exp_route = f"experiment/{experiment.id}"
    response = requests.get(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Drift(response.json())


def put_drift(experiment, drift: models.Drift) -> models.Drift:
    """Update a drift run on the drift monitor server."""
    exp_route = f"experiment/{experiment.id}"
    response = requests.put(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift.id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=schemas.UpdateDrift(unknown=ma.EXCLUDE).dump(drift),
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.Drift(response.json())


def delete_drift(experiment, drift_id: UUID) -> None:
    """Delete a drift run from the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.delete(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return None


# Users: API Methods to list, register and update users.


def search_user(query, page=1, page_size=10):
    """Search for users on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/user/search",
        headers={"Authorization": f"Bearer {access_token()}"},
        params={"page": page, "page_size": page_size},
        json=query,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return (
        [models.User(data) for data in response.json()],
        response.headers["X-Pagination"],
    )


def post_user() -> models.User:
    """Create a new user on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/user",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.User(response.json())


def self_user() -> models.User:
    """Get the token user from the drift monitor server."""
    response = requests.get(
        url=f"{settings.monitor_url}/user/self",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.User(response.json())


def update_user() -> models.User:
    """Update the token user in the application database."""
    response = requests.put(
        url=f"{settings.monitor_url}/user/self",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return models.User(response.json())
