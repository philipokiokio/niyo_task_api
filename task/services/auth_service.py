import logging
from task.schemas.auth_schemas import User, UserUpdate, UserAccessToken
import task.database.db_handlers.auth_db_handler as user_db_handler
from uuid import UUID
from fastapi import HTTPException, status
from task.services.service_utils.exception_collection import (
    NotFound,
    UpdateError,
)
import task.services.service_utils.gr_redis_utils as redis_utils
import task.services.service_utils.auth_utils as auth_utils
import task.services.service_utils.token_utils as gr_toks_utils
from task.root.utils.mailer import send_mail

LOGGER = logging.getLogger(__name__)


async def get_user_by_mail(email: str):
    try:
        return await user_db_handler.get_user(email=email)
    except NotFound as e:
        LOGGER.exception(e)
        LOGGER.error("User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )


async def get_user(user_uid: UUID):
    try:
        return await user_db_handler.get_user_profile(user_uid=user_uid)
    except NotFound as e:
        LOGGER.exception(e)
        LOGGER.error("User not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )


# create record
async def sign_up(user: User):
    """Create Admin Token

    Args:
        invite_token (AgentInviteToken): _description_

    Raises:
        HTTPException: invalid_token

    Returns:
        _type_: _description_
    """
    try:
        user_profile = await get_user_by_mail(email=user.email)

        if user_profile:
            LOGGER.error("Admin Account: exists")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="user account exist"
            )
    # else create record
    except HTTPException:
        user.password = auth_utils.hash_password(plain_password=user.password)

        user_profile = await user_db_handler.create_user(user=user)
        user_profile_dict = {"user_uid": str(user_profile.user_uid)}
        access_token, refresh_token = (
            auth_utils.create_access_token(data=user_profile_dict),
            auth_utils.create_refresh_token(data=user_profile_dict),
        )

        return UserAccessToken(access_token=access_token, refresh_token=refresh_token)


# login
async def login(email: str, password: str):
    user_profile = await get_user_by_mail(email=email)
    if not auth_utils.verify_password(
        hashed_password=user_profile.password, plain_password=password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="could not validate credentials",
        )

    payload_dict = {"user_uid": str(user_profile.user_uid), "email": user_profile.email}
    access_token, refresh_token = auth_utils.create_access_token(
        data=payload_dict
    ), auth_utils.create_refresh_token(data=payload_dict)

    return UserAccessToken(access_token=access_token, refresh_token=refresh_token)


# forget password
async def forgot_password(email: str):
    await get_user_by_mail(email=email)

    # Create a Token 4 OTP
    token = gr_toks_utils.gr_token_gen()

    redis_utils.add_forget_token(token=token, email=email)
    # send mail

    await send_mail(
        subject="Forgot Password",
        reciepients=[email],
        payload={"token": token},
        template="user_auth/token_email_template.html",
    )
    return {"messge": "mail sent"}

    ...


async def user_update(user_update: UserUpdate, user_uid: UUID):
    try:
        return await user_db_handler.update_user(
            user_update=user_update, user_uid=user_uid
        )
    except UpdateError as e:
        LOGGER.exception(e)
        LOGGER.error("unexplainable update error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user failed to update"
        )


async def reset_password(token: int, new_password: str):
    email = redis_utils.get_forget_token(token=token)
    if not email:
        LOGGER.error(f"forgot password token: {token} not valid")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password token has expired"
        )

    user_profile = await get_user_by_mail(email=email)

    new_password = auth_utils.hash_password(plain_password=new_password)
    updated_user_profile = await user_update(
        admin_update=UserUpdate(password=new_password),
        user_uid=user_profile.user_uid,
    )
    return updated_user_profile


async def logout(access_token: str, refresh_token: str):
    redis_utils.add_token_blacklist(
        access_token=access_token, refresh_token=refresh_token
    )

    return {}
