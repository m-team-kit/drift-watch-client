"""Drift Monitor Client package.
This package contains the client code for the drift monitor service.
"""

import requests

from drift_monitor import queries, utils


class DriftMonitor:
    """Drift Monitor context.
    This class is a context manager for the drift monitor service. It is used
    as an abstraction for the user to interact with the drift monitor service.

    When the context is entered, the drift monitor sends a POST request to the
    server to create a drift run. When the context is exited, the drift monitor
    sends a PUT request to the server to complete the drift run.

    Args:
        experiment_name (str): The name of the experiment.
        model_id (str): The model ID to monitor.

    Example:
        >>> with DriftMonitor("experiment_1", "model_1") as monitor:
        ...    detected, detection_parameters = concept_detector()
        ...    monitor.concept(detected, detection_parameters)
        ...    detected, detection_parameters = data_detector()
        ...    monitor.data(detected, detection_parameters)
    """

    def __init__(self, experiment_name, model_id):
        self.experiment_name = experiment_name
        self._model_id = model_id
        self._drift = None

    def concept(self, detected, parameters):
        """Prepare concept drift detection results to the server.

        Args:
            detected (bool): Whether concept drift was detected.
            detection_parameters (dict): The parameters used for detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self._drift is None:
            raise RuntimeError("Drift monitor context not started.")
        detected = bool(detected)  # Ensure correct serialization
        parameters = utils.convert_to_serializable(parameters)
        concept_drift = {"drift": detected, "parameters": parameters}
        self._drift["concept_drift"] = concept_drift

    def data(self, detected, parameters):
        """Prepare data drift detection results to the server.

        Args:
            detected (bool): Whether data drift was detected.
            detection_parameters (dict): The parameters used for detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self._drift is None:
            raise RuntimeError("Drift monitor context not started.")
        detected = bool(detected)  # Ensure correct serialization
        parameters = utils.convert_to_serializable(parameters)
        data_drift = {"drift": detected, "parameters": parameters}
        self._drift["data_drift"] = data_drift

    def __enter__(self):
        self._drift = create_drift(self.experiment, self._model_id)
        return self

    def __exit__(self, exc_type, _exc_value, _traceback):
        if exc_type:
            fail_drift(self.experiment, self._drift)
        else:
            complete_drift(self.experiment, self._drift)

    @property
    def experiment_name(self):
        """Get the experiment name."""
        return self.__experiment["name"]

    @experiment_name.setter
    def experiment_name(self, value):
        """Set the experiment name."""
        self.__experiment = find_experiment(value)
        if self.__experiment is None:
            raise ValueError("Experiment not found.")

    @property
    def experiment(self):
        """Get the experiment object."""
        return self.__experiment


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
    experiment, _ = queries.search_experiment({"name": experiment_name})
    return experiment[0] if experiment else None


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
    attributes = {  # Create a new experiment object
        "name": name,
        "description": description,
        "public": public,
        "permissions": permissions if permissions else {},
    }
    try:
        return queries.post_experiment(attributes)
    except requests.HTTPError as error:
        if error.response.status_code == 409:
            raise ValueError("Experiment already exists.") from error
        raise error


def create_drift(experiment, model_id):
    """Create a new drift run on the drift monitor server.

    Args:
        experiment (dict): The experiment object.
        model_id (str): The model ID to monitor.

    Returns:
        dict: The drift run object.
    """
    attributes = {"model_id": model_id, "job_status": "Running"}
    return queries.post_drift(experiment, attributes)


def fail_drift(experiment, drift):
    """Fail a drift run on the drift monitor server.

    Args:
        experiment (dict): The experiment object.
        drift (dict): The drift run object.

    Returns:
        dict: The updated drift run object.
    """
    _drift = {k: v for k, v in drift.items() if k not in {"id", "created_at"}}
    attributes = {**_drift, "job_status": "Failed"}
    return queries.put_drift(experiment, drift["id"], attributes)


def complete_drift(experiment, drift):
    """Complete a drift run on the drift monitor server.

    Args:
        experiment (dict): The experiment object.
        drift (dict): The drift run object.

    Returns:
        dict: The updated drift run object.
    """
    _drift = {k: v for k, v in drift.items() if k not in {"id", "created_at"}}
    attributes = {**_drift, "job_status": "Completed"}
    return queries.put_drift(experiment, drift["id"], attributes)
