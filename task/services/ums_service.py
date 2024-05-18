from task.schemas.auth_schemas import UserUpdate
from uuid import UUID
import task.services.auth_service as auth_service


async def ums_user_update(user_update: UserUpdate, user_uid: UUID):
    return await auth_service.user_update(user_update=user_update, user_uid=user_uid)
