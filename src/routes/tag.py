from typing import List
from fastapi import HTTPException
from fastapi.routing import APIRouter

from controller import DBConnection

from models import Experiment, Tag
from queries import (
    get_query_select_tags_by_experiment_id,
    get_query_get_all_tags,
    get_query_get_experiments_by_tag,
)

router = APIRouter(prefix="/tags")


@router.get("")
async def get_all_tags(limit: int = 10, offset: int = 0) -> List[Tag]:
    database = DBConnection()
    tags_query = get_query_get_all_tags(limit, offset)
    async with database.pool.acquire() as conn:
        tags_records = await conn.fetch(tags_query)
        tags = []
        for record in tags_records:
            tags.append(Tag(**record))

    return tags


@router.get("/{tag}")
async def get_experiments_by_tag(
    tag: str, limit: int = 10, offset: int = 0
) -> List[Experiment]:
    database = DBConnection()
    experiments_query = get_query_get_experiments_by_tag(tag, limit, offset)

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
