from task.database.orms.auth_orm import User as User_DB
from task.root.database import async_session
import logging
from task.schemas.auth_schemas import UserProfile

from sqlalchemy import insert, select, update, delete
from task.services.service_utils.exception_collection import (
    CreateError,
    DeleteError,
    NotFound,
    UpdateError,
)
from sqlalchemy.orm import joinedload
import task.schemas.task_schemas as schemas
from uuid import UUID
from task.database.orms.task_orm import Task as TaskDB


LOGGER = logging.getLogger(__name__)


async def create_task(task: schemas.Task, user: UserProfile):

    async with async_session() as session:

        stmt = (
            insert(TaskDB)
            .values(**task.model_dump(), user_uid=user.user_uid)
            .returning(TaskDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            LOGGER.error(f"task: {task.model_dump()} fir user {user.user_uid}")
            await session.rollback()
            raise CreateError

        await session.commit()

        return schemas.TaskProfile(**result.as_dict(), owner=user)


async def get_task(task_uid: UUID, user_uid: UUID):

    async with async_session() as session:
        stmt = (
            select(TaskDB)
            .options(joinedload(TaskDB.owner))
            .filter(TaskDB.task_uid == task_uid, TaskDB.user_uid == user_uid)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            logging.error(
                f"task with task_uid: {task_uid}, for user: {user_uid} not found"
            )
            raise NotFound

        return schemas.TaskProfile(**result.as_dict(), owner=result.owner)


async def get_tasks(user_uid: UUID):
    async with async_session() as session:
        stmt = (
            select(TaskDB)
            .options(joinedload(TaskDB.owner))
            .filter(TaskDB.user_uid == user_uid)
        )

        result = (await session.execute(statement=stmt)).scalars().all()

        if not result:
            return schemas.PaginatedTaskProfile()

        return schemas.PaginatedTaskProfile(
            result_set=[
                schemas.TaskProfile(**x.as_dict(), owner=x.owner) for x in result
            ],
            result_size=len(result),
        )


async def update_task(
    user: UserProfile, task_uid: UUID, task_update: schemas.TaskUpdate
):
    async with async_session() as session:
        stmt = (
            update(TaskDB)
            .filter(TaskDB.user_uid == user.user_uid, TaskDB.task_uid == task_uid)
            .values(**task_update.model_dump(exclude_none=True))
            .returning(TaskDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            LOGGER.error(
                f"task is with task_uid: {task_uid}, with user_uid: {user.user_uid} via data: {task_update.model_dump()}"
            )
            await session.rollback()
            raise UpdateError

        await session.commit()

        return schemas.TaskProfile(**result.as_dict(), owner=user)


async def delete_task(task_uid: UUID, user_uid: UUID):

    async with async_session() as session:
        stmt = (
            delete(TaskDB)
            .filter(TaskDB.user_uid == user_uid, TaskDB.task_uid == task_uid)
            .returning(TaskDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            LOGGER.error(
                f"task is with task_uid: {task_uid}, with user_uid: {user_uid}"
            )
            await session.rollback()
            raise DeleteError

        await session.commit()

        return schemas.TaskProfile(**result.as_dict())
