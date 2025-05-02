from typing import List
from pydantic import BaseModel


class Experiment(BaseModel):
    id: int | None
    name: str
    state: str
    researcher: str
    tags: List[str]


class State(BaseModel):
    id: int
    name: str


class Researcher(BaseModel):
    id: int
    name: str


class Tag(BaseModel):
    id: int
    name: str
