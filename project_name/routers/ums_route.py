from fastapi import APIRouter, status, Depends
import project_name.services.ums_service as agent_ums_service
import project_name.schemas.auth_schemas as schemas
from project_name.services.service_utils.auth_utils import get_current_user

api_router = APIRouter(prefix="/v1/ums", tags=["User Management"])


@api_router.patch(
    "/admin-update",
    response_model=schemas.AdminUserProfile,
    status_code=status.HTTP_200_OK,
)
async def update_admin(
    admin_update: schemas.AdminUserUpdate,
    current_admin_profile: schemas.AdminUserProfile = Depends(get_current_user),
):
    return await agent_ums_service.ums_admin_update(
        admin_update=admin_update, admin_user_uid=current_admin_profile.admin_uid
    )
