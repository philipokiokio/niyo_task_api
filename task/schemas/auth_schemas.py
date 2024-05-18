from . import AbstractModel
from pydantic import Field, constr, EmailStr
from uuid import UUID
from typing import Optional


class Login(AbstractModel):
    email: EmailStr
    password: constr(
        min_length=6,
        pattern="^[A-Za-z0-9!@#$&*_+%-=]+$",
    )


class User(Login):
    first_name: str
    last_name: str


class UserProfile(User):
    user_uid: UUID
    # excluding password
    password: str = Field(exclude=True)
    email: EmailStr = Field(exclude=True)


class UserUpdate(AbstractModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class TokenData(AbstractModel):
    user_uid: UUID


class UserAccessToken(AbstractModel):
    access_token: str
    refresh_token: str
