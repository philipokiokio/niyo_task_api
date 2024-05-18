import logging
from uuid import UUID
from fastapi import HTTPException, status
from task.schemas.auth_schemas import UserProfile
from task.services.service_utils.exception_collection import (
    NotFound,
    UpdateError,
)
import task.database.db_handlers.task_db_handler as task_db_handler
import task.schemas.task_schemas as schemas
from task.services.ws_manager_service import manager

LOGGER = logging.getLogger(__name__)


async def create_task(task: schemas.Task, user: UserProfile):

    task_profile = await task_db_handler.create_task(task=task, user=user)

    # send via websocket
    await manager.send_personal_message(task=task_profile)
    return task_profile

    ...


async def get_tasks(user_uid: UUID):

    return await task_db_handler.get_tasks(user_uid=user_uid)


async def get_task(user_uid: UUID, task_uid: UUID):
    try:

        return await task_db_handler.get_task(task_uid=task_uid, user_uid=user_uid)

    except NotFound:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task is not found"
        )


async def update_task(
    task_uid: UUID, user: UserProfile, task_update: schemas.TaskUpdate
):

    await get_task(task_uid=task_uid, user_uid=user.user_uid)

    try:
        return await task_db_handler.update_task(
            task_uid=task_uid, user=user, task_update=task_update
        )
    except UpdateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="task update failed"
        )


async def delete_task(task_uid: UUID, user_uid: UUID):
    await get_task(task_uid=task_uid, user_uid=user_uid)

    await task_db_handler.delete_task(task_uid=task_uid, user_uid=user_uid)
    return {}
