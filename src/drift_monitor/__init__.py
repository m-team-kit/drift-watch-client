"""Drift Monitor Client package.
This package contains the client code for the drift monitor service.
"""

from typing import Any, Dict, List, Optional

import requests

from drift_monitor import models, queries, utils


class DriftMonitor:
    """Drift Monitor context.
    This class is a context manager for the drift monitor service. It is used
    as an abstraction for the user to interact with the drift monitor service.

    When the context is entered, the drift monitor sends a POST request to the
    server to create a drift run. When the context is exited, the drift monitor
    sends a PUT request to the server to complete the drift run.

    Args:
        experiment (str): The name of the experiment.
        model_id (str): The model ID to monitor.
        tags (list, optional): The tags for the drift. Defaults to None.

    Example:
        >>> with DriftMonitor("experiment_1", "model_1") as monitor:
        ...    hypothesis_result, parameters = concept_detector()
        ...    monitor(detected, detection_parameters)
    """

    def __init__(
        self,
        experiment_name: str,
        model_id: str,
        tags: Optional[List[str]] = None,
    ):
        self._experiment_name: str = experiment_name
        self._experiment: models.Experiment | None = None
        self._attributes = {"model": model_id, "tags": tags or []}
        self._drift: models.Drift | None = None

    def __enter__(self) -> "DriftMonitor":
        self._experiment = find_experiment(self._experiment_name)
        attributes = {"job_status": "Running", **self._attributes}
        self._drift = queries.post_drift(self._experiment, attributes)
        return self

    def __call__(
        self,
        detected: bool,
        parameters: Dict[str, Any],
    ) -> None:
        """Prepare drift detection results for transmission to server.

        Args:
            detected (bool): Whether concept drift was detected.
            parameters (dict): The parameter values from detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self._experiment is None:
            raise RuntimeError("Drift monitor context not started.")
        if self._drift is None:
            raise RuntimeError("Drift removed while context active.")
        parameters = utils.convert_to_serializable(parameters)
        self._drift.drift_detected = bool(detected)  # Ensure serialization
        self._drift.parameters = parameters

    def __exit__(
        self,
        exc_type: Optional[type],
        _exc_value: Optional[BaseException],
        _traceback: Optional[Any],
    ) -> None:
        if self._experiment is None:
            raise RuntimeError("Drift monitor context not started.")
        if self._drift is None:
            raise RuntimeError("Drift removed while context active.")
        if exc_type:
            self._drift.job_status = "Failed"  # New status
            self._drift = queries.put_drift(self._experiment, self._drift)
        else:
            self._drift.job_status = "Completed"
            self._drift = queries.put_drift(self._experiment, self._drift)
        self._experiment = None  # Reset drift object


def register(accept_terms: bool = False) -> None:
    """Registers the token user in the application database.
    By using this function, you accept that the user derived from the token
    will be registered in the application database and agree to the terms of
    service.

    Args:
        accept_terms (bool, optional): Whether to accept the terms of service.
            Defaults to False.

    Raises:
        ValueError: If the user is already registered or terms are not accepted.
    """
    if not accept_terms:
        raise ValueError("You must accept the terms of service.")
    try:
        queries.post_user()
    except requests.HTTPError as error:
        if error.response.status_code == 409:
            queries.update_user()
            return  # User already registered
        raise error


def find_experiment(experiment_name: str) -> models.Experiment:
    """Get an experiment from the drift monitor server.

    Args:
        experiment_name (str): The name of the experiment.

    Returns:
        dict: The experiment object or None if not found.

    Raises:
        ValueError: If the experiment is not found.
    """
    search_query = {"name": experiment_name}
    experiments, _ = queries.search_experiment(search_query)
    if experiments is []:
        raise ValueError("Experiment not found.")
    return experiments[0]  # Return first result


def new_experiment(
    name: str,
    description: str,
    public: bool = False,
    permissions: Optional[Dict[str, Any]] = None,
) -> models.Experiment:
    """Create a new experiment in the drift monitor service.

    Args:
        name (str): The name of the experiment.
        description (str): The description of the experiment.
        public (bool, optional): Whether the experiment is public.
            Defaults to False.
        permissions (dict, optional): The permissions for the experiment.
            Defaults to None.

    Returns:
        dict: The experiment object.
    """
    try:
        return queries.post_experiment(
            {
                "name": name,
                "description": description,
                "public": public,
                "permissions": permissions if permissions else [],
            }
        )
    except requests.HTTPError as error:
        if error.response.status_code == 409:
            raise ValueError("Experiment already exists.") from error
        raise error
