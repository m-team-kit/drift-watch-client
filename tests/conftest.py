"""Root conftest.py file for pytest configuration."""

# pylint: disable=redefined-outer-name

import datetime as dt
import json
import os
from unittest import mock

import jwt
from pytest import fixture


@fixture(scope="session")
def endpoint():
    """Return the server URL."""
    return os.environ["DRIFT_MONITOR_URL"]


@fixture(scope="function")
def db_experiments():
    """Load experiments from JSON file at tests/database."""
    path = "tests/database/test-experiments.json"
    return {exp["name"]: exp for exp in load_json(path)}


@fixture(scope="function")
def db_drifts(experiment_name):
    """Load drifts from JSON file at tests/database."""
    path = f"tests/database/{experiment_name}.json"
    return {drift["id"]: drift for drift in load_json(path)}


def load_json(path):
    """Load data from a JSON files at tests/database."""
    with open(path, encoding="utf-8") as file:
        return json.loads(_data := file.read())


@fixture(scope="session")
def token(request):
    """Return the server token."""
    if hasattr(request, "param") and request.param:
        return request.param
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": now,
        "exp": now + 10000000,
    }
    token = jwt.encode(payload, "some_key", algorithm="HS256")
    return token


@fixture(scope="session", autouse=True)
def token_mock(token):
    """Patch the access token with a MagicMock."""
    with mock.patch("drift_monitor.queries.access_token") as access_token:
        access_token.return_value = token
        yield access_token


@fixture(scope="module")
def request_mock():
    """Patch requests module with MagicMocks."""
    with mock.patch("drift_monitor.queries.requests") as requests:
        yield requests


@fixture(scope="function")
def db_experiment(experiment_name, db_experiments):
    """Return a experiment from the database."""
    return db_experiments[experiment_name]


@fixture(scope="function")
def db_drift(drift_id, db_drifts):
    """Return a drift from the database."""
    return db_drifts[drift_id]
