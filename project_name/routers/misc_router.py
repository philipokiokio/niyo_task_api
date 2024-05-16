from . import (
    APIRouter,
    Body,
    status,
    Depends,
    UploadFile,
)  # This imports FASTAPI Specific tools for all routers
import project_name.services.misc_service as misc_service
from project_name.services.service_utils.auth_utils import get_current_user
from project_name.schemas.auth_schemas import AdminUserProfile
from typing import List
import project_name.schemas.misc_schemas as misc_schema


api_router = APIRouter(prefix="/v1/misc", tags=["MISC Service"])


@api_router.post("/upload", status_code=status.HTTP_201_CREATED)  # response_model,
async def file_uploader(
    upload_files: List[UploadFile],
    target: misc_schema.purpose = Body(embed=True),
    current_admin_profile: AdminUserProfile = Depends(get_current_user),
):
    return await misc_service.file_uploader(
        files=upload_files, purpose=target, admin_profile=current_admin_profile
    )


@api_router.post("/delete-upload", status_code=status.HTTP_200_OK)  # response_model,
async def file_delete(
    uploaded_file: str = Body(embed=True),
    current_agent_profile: AdminUserProfile = Depends(get_current_user),
):
    return await misc_service.file_delete(uploaded_file=uploaded_file)
