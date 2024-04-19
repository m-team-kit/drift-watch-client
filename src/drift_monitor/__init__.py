"""Drift Monitor Client package.
This package contains the client code for the drift monitor service.
"""

from drift_monitor import utils


class DriftMonitor:
    """Drift Monitor context.
    This class is a context manager for the drift monitor service. It is used
    as an abstraction for the user to interact with the drift monitor service.

    When the context is entered, the drift monitor sends a POST request to the
    server to create a drift run. When the context is exited, the drift monitor
    sends a PUT request to the server to complete the drift run.

    Args:
        model_id (str): The model ID to monitor.
        token (str): The token to authenticate with the server.

    Example:
        >>> with DriftMonitor("model_1", token="123") as monitor:
        ...    detected, detection_parameters = concept_detector()
        ...    monitor.concept(detected, detection_parameters)
        ...    detected, detection_parameters = data_detector()
        ...    monitor.data(detected, detection_parameters)
    """

    def __init__(self, model_id, token=None):
        self.model_id = model_id
        self.token = token
        self.drift = None

    def concept(self, detected, parameters):
        """Prepare concept drift detection results to the server.

        Args:
            detected (bool): Whether concept drift was detected.
            detection_parameters (dict): The parameters used for detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self.drift is None:
            raise RuntimeError("Drift monitor context not started.")
        concept_drift = {"drift": detected, "parameters": parameters}
        self.drift["concept_drift"] = concept_drift

    def data(self, detected, parameters):
        """Prepare data drift detection results to the server.

        Args:
            detected (bool): Whether data drift was detected.
            detection_parameters (dict): The parameters used for detection.

        Raises:
            RuntimeError: If the drift monitor context is not started.
        """
        if self.drift is None:
            raise RuntimeError("Drift monitor context not started.")
        data_drift = {"drift": detected, "parameters": parameters}
        self.drift["data_drift"] = data_drift

    def __enter__(self):
        self.drift = utils.create_drift(self.model_id, self.token)
        return self

    def __exit__(self, exc_type, _exc_value, _traceback):
        if exc_type:
            utils.fail_drift(self.drift, self.token)
        else:
            utils.complete_drift(self.drift, self.token)