from .utils.base_schemas import AbstractSettings
from pydantic.networks import PostgresDsn, RedisDsn
from pydantic import constr, EmailStr


class Settings(AbstractSettings):
    postgres_url: PostgresDsn
    redis_url: RedisDsn
    jwt_secret_key: constr(min_length=32)
    ref_jwt_secret_key: constr(max_length=64)
    second_signer_key: constr(min_length=10)
    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_from_name: str
    mail_port: int
    mail_server: str
    space_secret_key: str
    space_access_key: str
    space_bucket: str
    space_region_name: str
    is_prod_env: bool
