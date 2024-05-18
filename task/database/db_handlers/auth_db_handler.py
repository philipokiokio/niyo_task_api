from task.database.orms.auth_orm import User as User_DB
from task.root.database import async_session
import logging
from task.schemas.auth_schemas import (
    User,
    UserProfile,
    UserUpdate,
)
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from task.services.service_utils.exception_collection import (
    CreateError,
    DuplicateError,
    NotFound,
    UpdateError,
)
from uuid import UUID

LOGGER = logging.getLogger(__name__)


async def create_user(user: User) -> UserProfile:
    async with async_session() as session:
        stmt = insert(User_DB).values(user.model_dump()).returning(User_DB)
        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"duplicate record found for {user.model_dump()}")
            session.rollback()
            raise DuplicateError
        if not result:
            LOGGER.error("create_admin failed")
            session.rollback()
            raise CreateError

        await session.commit()
        return UserProfile(**result.as_dict())


async def get_user(email: str):
    async with async_session() as session:
        result = (
            await session.execute(select(User_DB).where(User_DB.email == email))
        ).scalar_one_or_none()

        if not result:
            raise NotFound

        return UserProfile(**result.as_dict())


async def get_user_profile(user_uid: UUID):
    async with async_session() as session:
        result = (
            await session.execute(select(User_DB).where(User_DB.user_uid == user_uid))
        ).scalar_one_or_none()

        if not result:
            raise NotFound

        return UserProfile(**result.as_dict())


async def update_user(user_update: UserUpdate, admin_user_uid: UUID):
    async with async_session() as session:
        stmt = (
            update(User_DB)
            .where(User_DB.user_uid == admin_user_uid)
            .values(user_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(User_DB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if not result:
            raise UpdateError

        await session.commit()
        return UserProfile(**result.as_dict())


async def delete_user(): ...
