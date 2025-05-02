from typing import List
from fastapi import Response
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse
from models import Experiment

router = APIRouter(prefix="/experiment")


@router.get("")
async def get_experiments(limit: int = 10, offset: int = 0) -> List[Experiment]:
    return 4


@router.get("/{experiment_id}")
async def get_experiment_by_id() -> Experiment:
    return Experiment(
        id=1,
        name="hehe",
        state="haha",
        researcher="hoho",
        tags=[],
    )


@router.post("")
async def create_experiment(experiment: Experiment) -> Experiment:
    pass


@router.patch("/{experiment_id}")
async def edit_experiment(experiment: Experiment) -> Experiment:
    pass


@router.delete("/{experiment_id}")
async def delete_experiment() -> Experiment:
    pass
