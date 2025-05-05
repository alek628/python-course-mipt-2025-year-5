from typing import List, Annotated
from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer
import jwt

from controller import DBConnection
from config import SECRET_KEY
from models import Experiment, InputExperiment
from queries import (
    get_query_select_experiment_by_id,
    get_query_select_tags_by_experiment_id,
    get_query_select_experiments_paginated,
    get_query_select_experiments_by_email_paginated,
    get_query_insert_experiment,
    get_query_insert_tags,
    get_query_add_tags_to_experiment,
    get_query_update_experiment,
    get_query_delete_experiment,
    get_query_delete_experiment_tags,
)

router = APIRouter(prefix="/experiment")


@router.get("")
async def get_experiments(limit: int = 10, offset: int = 0) -> List[Experiment]:
    database = DBConnection()
    experiments_query = get_query_select_experiments_paginated(limit, offset)

    results = []

    async with database.pool.acquire() as conn:
        experiments_records = await conn.fetch(experiments_query)
        if not experiments_records:
            raise HTTPException(404, "experiments not found")

        for experiment_record in experiments_records:
            experiment_id = experiment_record["experiment_id"]

            tags_query = get_query_select_tags_by_experiment_id(experiment_id)
            tags_records = await conn.fetch(tags_query)
            tags = []
            for record in tags_records:
                tags.append(record["tag_name"])

            results.append(Experiment(**dict(experiment_record), tags=tags))

        tags_records = await conn.fetch(tags_query)

    return results


@router.get("/my")
async def get_experiments_for_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/login"))],
    limit: int = 10,
    offset: int = 0,
) -> List[Experiment]:
    database = DBConnection()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(401, "invalid token - none")
    except jwt.InvalidTokenError as e:
        raise HTTPException(401, "invalid token - exception") from e

    experiments_query = get_query_select_experiments_by_email_paginated(
        email, limit, offset
    )

    results = []

    async with database.pool.acquire() as conn:
        experiments_records = await conn.fetch(experiments_query)
        if not experiments_records:
            raise HTTPException(404, "experiments not found")

        for experiment_record in experiments_records:
            experiment_id = experiment_record["experiment_id"]

            tags_query = get_query_select_tags_by_experiment_id(experiment_id)
            tags_records = await conn.fetch(tags_query)
            tags = []
            for record in tags_records:
                tags.append(record["tag_name"])

            results.append(Experiment(**dict(experiment_record), tags=tags))

        tags_records = await conn.fetch(tags_query)

    return results


@router.get("/{experiment_id}")
async def get_experiment_by_id(experiment_id: int) -> Experiment:
    database = DBConnection()
    experiment_query = get_query_select_experiment_by_id(experiment_id)
    tags_query = get_query_select_tags_by_experiment_id(experiment_id)

    async with database.pool.acquire() as conn:
        experiment = await conn.fetchrow(experiment_query)
        if not experiment:
            raise HTTPException(404, "no experiment with such id")
        tags_records = await conn.fetch(tags_query)

        print(dict(experiment))

    tags = []
    for record in tags_records:
        tags.append(record["tag_name"])

    return Experiment(**dict(experiment), tags=tags)


@router.post("")
async def create_experiment(
    experiment: InputExperiment,
) -> Experiment:
    database = DBConnection()
    insert_experiment_query = get_query_insert_experiment(
        experiment.name,
        experiment.description,
        experiment.state,
        experiment.assignee,
    )
    print(insert_experiment_query)

    tags = []

    async with database.pool.acquire() as conn:
        inserted_experiment_record = await conn.fetchrow(insert_experiment_query)
        if not inserted_experiment_record:
            raise HTTPException(500, "failed to create experiment")

        # updating tags_list
        if experiment.tags:
            insert_new_tags_query = get_query_insert_tags(experiment.tags)

            new_tags_in_tags_list = await conn.fetch(insert_new_tags_query)
            if len(experiment.tags) != len(new_tags_in_tags_list):
                raise HTTPException(500, "failed to create new tags")

            inserted_experiment_id = inserted_experiment_record["experiment_id"]
            add_tags_to_experiment_query = get_query_add_tags_to_experiment(
                inserted_experiment_id,
                [tag_record["tag_list_id"] for tag_record in new_tags_in_tags_list],
            )
            _ = await conn.execute(add_tags_to_experiment_query)
            added_tags_query = get_query_select_tags_by_experiment_id(
                inserted_experiment_id
            )
            added_tags = await conn.fetch(added_tags_query)

            for record in added_tags:
                tags.append(record["tag_name"])

    return Experiment(**dict(inserted_experiment_record), tags=tags)


@router.patch("/{experiment_id}")
async def edit_experiment(
    experiment_id: int, experiment: InputExperiment
) -> Experiment:
    database = DBConnection()
    update_experiment_query = get_query_update_experiment(
        experiment_id,
        experiment.name,
        experiment.description,
        experiment.state,
        experiment.assignee,
    )
    print(update_experiment_query)

    tags = []

    async with database.pool.acquire() as conn:
        updated_experiment_record = await conn.fetchrow(update_experiment_query)
        if not updated_experiment_record:
            raise HTTPException(500, "failed to update experiment")

        # updating tags_list
        if experiment.tags:
            delete_tags_query = get_query_delete_experiment_tags(experiment_id)
            await conn.execute(delete_tags_query)

            insert_new_tags_query = get_query_insert_tags(experiment.tags)

            new_tags_in_tags_list = await conn.fetch(insert_new_tags_query)
            if len(experiment.tags) != len(new_tags_in_tags_list):
                raise HTTPException(500, "failed to update tags")

            inserted_experiment_id = experiment_id
            add_tags_to_experiment_query = get_query_add_tags_to_experiment(
                inserted_experiment_id,
                [tag_record["tag_list_id"] for tag_record in new_tags_in_tags_list],
            )
            _ = await conn.execute(add_tags_to_experiment_query)
            added_tags_query = get_query_select_tags_by_experiment_id(
                inserted_experiment_id
            )
            added_tags = await conn.fetch(added_tags_query)

            for record in added_tags:
                tags.append(record["tag_name"])

    return Experiment(**dict(updated_experiment_record), tags=tags)


@router.delete("/{experiment_id}")
async def delete_experiment(experiment_id: int) -> Experiment:
    database = DBConnection()

    delete_tags_query = get_query_delete_experiment_tags(experiment_id)
    delete_experiment_query = get_query_delete_experiment(experiment_id)

    async with database.pool.acquire() as conn:
        await conn.execute(delete_tags_query)

        deleted_experiment = await conn.fetchrow(delete_experiment_query)
        if not deleted_experiment:
            raise HTTPException(404, "no experiment with such id")

    return Experiment(**dict(deleted_experiment), tags=[])
