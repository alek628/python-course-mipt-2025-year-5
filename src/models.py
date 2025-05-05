from typing import List, Optional
from pydantic import BaseModel, SecretStr


class BaseExperiment(BaseModel):
    name: str
    description: str
    state: str
    assignee: Optional[int] = None
    tags: Optional[List[str]] = None


class Experiment(BaseExperiment):
    experiment_id: int


class InputExperiment(BaseExperiment): ...


class State(BaseModel):
    state_id: int
    name: str


class BaseUser(BaseModel):
    name: str
    email: str
    password: SecretStr


class User(BaseUser):
    user_id: int


class InputUser(BaseUser): ...


class Tag(BaseModel):
    tag_id: int
    name: str
