"""Query functions for drift watch server."""

import requests

from drift_monitor.config import access_token, settings


# Entitlements: API Methods to list, entitlements.


def get_entitlements():
    """Get the entitlements of the token user."""
    response = requests.get(
        url=f"{settings.monitor_url}/entitlements",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


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
    return response.json(), response.headers["X-Pagination"]


def post_experiment(attributes):
    """Create a new experiment on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/experiment",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=attributes,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def get_experiment(experiment_id):
    """Get an experiment from the drift monitor server."""
    response = requests.get(
        url=f"{settings.monitor_url}/experiment/{experiment_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def put_experiment(experiment_id, attributes):
    """Update an experiment on the drift monitor server."""
    response = requests.put(
        url=f"{settings.monitor_url}/experiment/{experiment_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=attributes,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def delete_experiment(experiment_id):
    """Delete an experiment from the drift monitor server."""
    response = requests.delete(
        url=f"{settings.monitor_url}/experiment/{experiment_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


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
    return response.json(), response.headers["X-Pagination"]


def post_drift(experiment, attributes):
    """Create a new drift run on the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.post(
        url=f"{settings.monitor_url}/{exp_route}/drift",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=attributes,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def get_drift(experiment, drift_id):
    """Get a drift run from the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.get(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def put_drift(experiment, drift_id, attributes):
    """Update a drift run on the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.put(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=attributes,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def delete_drift(experiment, drift_id):
    """Delete a drift run from the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.delete(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift_id}",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


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
    return response.json(), response.headers["X-Pagination"]


def post_user():
    """Create a new user on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/user",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def self_user():
    """Get the token user from the drift monitor server."""
    response = requests.get(
        url=f"{settings.monitor_url}/user/self",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def update_user():
    """Update the token user in the application database."""
    response = requests.put(
        url=f"{settings.monitor_url}/user/self",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()
