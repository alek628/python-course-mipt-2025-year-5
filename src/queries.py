from typing import List

from pypika import PostgreSQLQuery, Table


def get_query_select_experiments_paginated(limit: int, offset: int) -> str:
    experiments = Table("experiments")
    users = Table("users")

    query = (
        PostgreSQLQuery.from_(experiments)
        .left_join(users)
        .on(experiments.assignee == users.user_id)
        .select(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            users.user_id.as_("assignee"),
        )
        .limit(limit)
        .offset(offset)
    )

    return str(query)


def get_query_select_experiments_by_email_paginated(
    email: str, limit: int, offset: int
) -> str:
    experiments = Table("experiments")
    users = Table("users")

    query = (
        PostgreSQLQuery.from_(experiments)
        .left_join(users)
        .on(experiments.assignee == users.user_id)
        .select(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            users.user_id.as_("assignee"),
        )
        .where(users.email == email)
        .limit(limit)
        .offset(offset)
    )

    return str(query)


def get_query_select_experiment_by_id(id_: int) -> str:
    experiments = Table("experiments")

    query = (
        PostgreSQLQuery.from_(experiments)
        .select(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            experiments.assignee,
        )
        .where(experiments.experiment_id == id_)
    )

    return str(query)


def get_query_select_tags_by_experiment_id(id_: int) -> str:
    tags = Table("tags")
    tags_list = Table("tags_list")

    query = (
        PostgreSQLQuery.from_(tags)
        .left_join(tags_list)
        .on(tags.tag_list_id == tags_list.tag_list_id)
        .select(
            tags.tag_id,
            tags.experiment_id,
            tags.tag_list_id,
            tags_list.name.as_("tag_name"),
        )
        .where(tags.experiment_id == id_)
    )

    return str(query)


def get_query_insert_experiment(
    name: str, description: str, state: str, assignee: int
) -> str:
    experiments = Table("experiments")

    query = (
        PostgreSQLQuery.into(experiments)
        .columns(
            experiments.name,
            experiments.description,
            experiments.state,
            experiments.assignee,
        )
        .insert(name, description, state, assignee)
        .returning(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            experiments.assignee,
        )
    )

    return str(query)


def get_query_update_experiment(
    experiment_id: int, name: str, description: str, state: str, assignee: int
) -> str:
    experiments = Table("experiments")

    query = (
        PostgreSQLQuery.update(experiments)
        .set(experiments.name, name)
        .set(experiments.description, description)
        .set(experiments.state, state)
        .set(experiments.assignee, assignee)
        .where(experiments.experiment_id == experiment_id)
        .returning(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            experiments.assignee,
        )
    )

    return str(query)


def get_query_delete_experiment(experiment_id: int) -> str:
    experiments = Table("experiments")

    query = (
        PostgreSQLQuery.from_(experiments)
        .delete()
        .where(experiments.experiment_id == experiment_id)
        .returning(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            experiments.assignee,
        )
    )

    return str(query)


def get_query_delete_experiment_tags(experiment_id: int) -> str:
    tags = Table("tags")

    query = (
        PostgreSQLQuery.from_(tags).delete().where(tags.experiment_id == experiment_id)
    )

    return str(query)


def get_query_insert_tags(tags: List[str]) -> str:
    tags_list = Table("tags_list")

    query = PostgreSQLQuery.into(tags_list).columns(tags_list.name)
    for tag in tags:
        query = query.insert(tag)

    query = query.on_conflict(tags_list.name).do_update(tags_list.name, tags_list.name)
    query = query.returning(tags_list.tag_list_id)

    return str(query)


def get_query_add_tags_to_experiment(experiment_id: int, tags_ids: List[int]) -> str:
    tags = Table("tags")

    query = PostgreSQLQuery.into(tags).columns(tags.experiment_id, tags.tag_list_id)
    for tag in tags_ids:
        query = query.insert(experiment_id, tag)

    query = query.on_conflict(tags.experiment_id, tags.tag_list_id).do_nothing()
    query = query.returning(tags.tag_id)

    return str(query)


def get_query_get_user_by_email(email: str) -> str:
    users = Table("users")

    query = (
        PostgreSQLQuery.from_(users)
        .select(
            users.user_id,
            users.name,
            users.email,
            users.password,
        )
        .where(users.email == email)
    )

    return str(query)


def get_query_insert_user(name: str, email: str, password: str) -> str:
    users = Table("users")

    query = (
        PostgreSQLQuery.into(users)
        .columns(
            users.name,
            users.email,
            users.password,
        )
        .insert(name, email, password)
        .returning(
            users.user_id,
            users.name,
            users.email,
            users.password,
        )
    )

    return str(query)


def get_query_get_all_tags(limit: int, offset: int) -> str:
    tags_list = Table("tags_list")

    query = (
        PostgreSQLQuery.from_(tags_list)
        .select(
            tags_list.tag_list_id.as_("tag_id"),
            tags_list.name,
        )
        .limit(limit)
        .offset(offset)
    )

    return str(query)


def get_query_get_experiments_by_tag(tag: str, limit: int, offset: int) -> str:
    experiments = Table("experiments")
    users = Table("users")
    tags = Table("tags")
    tags_list = Table("tags_list")

    query = (
        PostgreSQLQuery.from_(experiments)
        .left_join(users)
        .on(experiments.assignee == users.user_id)
        .left_join(tags)
        .on(experiments.experiment_id == tags.experiment_id)
        .left_join(tags_list)
        .on(tags.tag_list_id == tags_list.tag_list_id)
        .select(
            experiments.experiment_id,
            experiments.name,
            experiments.description,
            experiments.state,
            users.user_id.as_("assignee"),
        )
        .where(tags_list.name == tag)
        .limit(limit)
        .offset(offset)
    )

    return str(query)
