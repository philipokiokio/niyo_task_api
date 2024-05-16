from fastapi import (
    APIRouter,
    Body,
    status,
    Depends,
    UploadFile,
)
from project_name.services.service_utils.auth_utils import (
    get_current_user,
    AdminUserProfile,
)
from uuid import UUID
