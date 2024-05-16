from project_name.schemas.auth_schemas import AdminUserUpdate
from uuid import UUID
import project_name.services.auth_service as admin_auth_service


async def ums_admin_update(admin_update: AdminUserUpdate, admin_user_uid: UUID):
    return await admin_auth_service.admin_update(
        admin_update=admin_update, admin_user_uid=admin_user_uid
    )
