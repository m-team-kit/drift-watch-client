"""Drift Monitor Client package.
This package contains the client code for the drift monitor service.
"""

import requests
from drift_monitor import queries, utils, schemas, models


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

    def __init__(self, experiment_name, model_id, tags=None):
        self._experiment_name = experiment_name
        self._experiment = None
        self._attributes = {"model": model_id, "tags": tags or []}
        self._drift = None

    def __enter__(self):
        self._experiment = find_experiment(self._experiment_name)
        attributes = {"job_status": "Running", **self._attributes}
        self._drift = queries.post_drift(self._experiment, attributes)
        return self

    def __call__(self, detected, parameters):
        """Prepare drift detection results for transmission to server.

        Args:
            detected (bool): Whether concept drift was detected.
            parameters (dict): The parameter values from detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self._experiment is None:
            raise RuntimeError("Drift monitor context not started.")
        detected = bool(detected)  # Ensure correct serialization
        parameters = utils.convert_to_serializable(parameters)
        self._drift["drift_detected"] = bool(detected)
        self._drift["parameters"] = parameters

    def __exit__(self, exc_type, _exc_value, _traceback):
        if exc_type:
            self._drift["job_status"] = "Failed"  # New status
            self._drift = queries.put_drift(self._experiment, self._drift)
        else:
            self._drift["job_status"] = "Completed"
            self._drift = queries.put_drift(self._experiment, self._drift)
        self._experiment = None  # Reset drift object


def register(accept_terms=False):
    """Registers the token user in the application database.
    By using this function, you accept that the user derived from the token
    will be registered in the application database and agree to the terms of
    service.
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


def find_experiment(experiment_name):
    """Get an experiment from the drift monitor server.

    Args:
        experiment_name (str): The name of the experiment.

    Returns:
        dict: The experiment object or None if not found.
    """
    search_query = {"name": experiment_name}
    experiments, _ = queries.search_experiment(search_query)
    return experiments[0] if experiments else None


def new_experiment(name, description, public=False, permissions=None):
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
                "permissions": permissions if permissions else {},
            }
        )
    except requests.HTTPError as error:
        if error.response.status_code == 409:
            raise ValueError("Experiment already exists.") from error
        raise error
