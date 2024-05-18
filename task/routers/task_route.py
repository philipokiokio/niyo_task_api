from fastapi import (
    APIRouter,
    status,
    Depends,
)
import task.schemas.task_schemas as schemas

from task.services.service_utils.auth_utils import get_current_user
import task.services.task_service as task_service
from uuid import UUID

api_router = APIRouter(prefix="/v1/task", tags=["Tasks Management"])


@api_router.post(
    path="", response_model=schemas.TaskProfile, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: schemas.Task,
    current_user_profile: schemas.UserProfile = Depends(get_current_user),
):

    return await task_service.create_task(task=task, user=current_user_profile)


@api_router.get(
    path="s",
    response_model=schemas.PaginatedTaskProfile,
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    current_user_profile: schemas.UserProfile = Depends(get_current_user),
):

    return await task_service.get_tasks(user_uid=current_user_profile.user_uid)


@api_router.get(
    path="/{task_uid}",
    response_model=schemas.TaskProfile,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_uid: UUID,
    current_user_profile: schemas.UserProfile = Depends(get_current_user),
):

    return await task_service.get_task(
        user_uid=current_user_profile.user_uid, task_uid=task_uid
    )


@api_router.patch(
    path="/{task_uid}",
    response_model=schemas.TaskProfile,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_uid: UUID,
    task_update: schemas.TaskUpdate,
    current_user_profile: schemas.UserProfile = Depends(get_current_user),
):

    return await task_service.update_task(
        user=current_user_profile,
        task_uid=task_uid,
        task_update=task_update,
    )


@api_router.delete(
    path="/{task_uid}",
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_uid: UUID,
    current_user_profile: schemas.UserProfile = Depends(get_current_user),
):

    return await task_service.delete_task(
        user_uid=current_user_profile.user_uid,
        task_uid=task_uid,
    )
