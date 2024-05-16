from fastapi import APIRouter
from project_name.routers.auth_route import api_router as auth_router
from project_name.routers.ums_route import api_router as ums_router
from project_name.routers.misc_router import api_router as misc_router


router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=ums_router)
router.include_router(router=misc_router)
