from fastapi import APIRouter
from task.routers.auth_route import api_router as auth_router
from task.routers.ums_route import api_router as ums_router
from task.routers.task_route import api_router as task_router

router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=ums_router)
router.include_router(router=task_router)
