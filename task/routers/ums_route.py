from fastapi import APIRouter, status, Depends
import task.services.ums_service as ums_service
import task.schemas.auth_schemas as schemas
from task.services.service_utils.auth_utils import get_current_user

api_router = APIRouter(prefix="/v1/ums", tags=["User Management"])


@api_router.patch(
    "/user-update",
    response_model=schemas.UserProfile,
    status_code=status.HTTP_200_OK,
)
async def update_admin(
    user_update: schemas.UserUpdate,
    current_admin_profile: schemas.UserProfile = Depends(get_current_user),
):
    return await ums_service.ums_user_update(
        user_update=user_update, user_uid=current_admin_profile.user_uid
    )
