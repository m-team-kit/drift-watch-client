"""Dataclasses for drift_monitor module."""

import dataclasses
import uuid
from abc import ABC

import marshmallow as ma

from drift_monitor import schemas


class _BaseModel(ABC):  # pylint: disable=too-few-public-methods
    id: uuid.UUID | None = None
    created_at: str | None = None


@dataclasses.dataclass(init=False)
class Experiment(_BaseModel):
    """Experiment dataclass."""

    name: str
    description: str | None = None
    public: bool = False
    permissions: list = dataclasses.field(default_factory=list)

    def __init__(self, data):
        load = schemas.Experiment(unknown=ma.INCLUDE).load(data)
        self.__dict__.update(load)


@dataclasses.dataclass(init=False)
class Drift(_BaseModel):
    """Drift dataclass."""

    model: str
    schema_version: str | None = None
    job_status: str = "Running"
    tags: list = dataclasses.field(default_factory=list)
    drift_detected: bool = False
    parameters: dict = dataclasses.field(default_factory=dict)

    def __init__(self, data):
        load = schemas.Drift(unknown=ma.INCLUDE).load(data)
        self.__dict__.update(load)


@dataclasses.dataclass(init=False)
class User(_BaseModel):
    """User dataclass."""

    subject: str
    issuer: str
    email: str

    def __init__(self, data):
        load = schemas.User(unknown=ma.INCLUDE).load(data)
        self.__dict__.update(load)
