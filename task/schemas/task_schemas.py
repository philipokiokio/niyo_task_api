from task.root.utils.base_schemas import AbstractModel
from typing import Optional
from enum import Enum
from uuid import UUID
from task.schemas.auth_schemas import UserProfile
from pydantic import conint


class Status(Enum):
    on_going = "On-Going"
    completed = "Completed"
    postponed = "Postponded"
    ...


class Task(AbstractModel):
    title: str
    detail: Optional[str] = None
    is_completed: bool = False
    status: str = Status.on_going


class TaskProfile(Task):
    task_uid: UUID
    user_uid: UUID
    owner: UserProfile


class TaskUpdate(AbstractModel):
    title: Optional[str] = None
    detail: Optional[str] = None
    is_completed: Optional[bool] = None
    status: Optional[Status] = None


class PaginatedTaskProfile(AbstractModel):
    result_set: list[TaskProfile]
    result_size: conint(ge=0) = 0
