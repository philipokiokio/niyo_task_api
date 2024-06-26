from task.root.redis_manager import gr_redis
from typing import Optional


def refresh_token_key_generator(key: str):
    return f"GR-Refresh-Token-{key}"


def add_refresh_token(refresh_token: str, expire_time: int):
    key = refresh_token_key_generator(key=refresh_token)
    return gr_redis.set(name=key, value=refresh_token, ex=expire_time)


def get_refresh_token(refresh_token: str) -> Optional[str]:
    key = refresh_token_key_generator(key=refresh_token)
    return gr_redis.get(name=key)


def delete_refresh_token(refresh_token: str):
    key = refresh_token_key_generator(key=refresh_token)
    return gr_redis.delete(key)


def admin_invite_token_key_generator(key: str):
    return f"Admin-Invite-Key-{key}"


def add_admin_invite_token(token: int, email: str):
    key = admin_invite_token_key_generator(key=token)
    return gr_redis.set(name=key, value=email)


def get_admin_invite_token(token: str):
    key = admin_invite_token_key_generator(key=token)

    return gr_redis.get(name=key)


def delete_admin_invite_token(token: str):
    key = admin_invite_token_key_generator(key=token)
    return gr_redis.delete(key)


FORGET_PASSWORD_EXPIRE = 120


def forget_admin_key_generator(token: int):
    return f"Forget-Admin-Key-{token}"


def add_forget_token(token: int, email: str):
    key = forget_admin_key_generator(token=token)

    return gr_redis.set(name=key, value=email, ex=FORGET_PASSWORD_EXPIRE)


def get_forget_token(token: int):
    key = forget_admin_key_generator(token=token)

    return gr_redis.get(name=key)


def delete_forget_token(token: int):
    key = forget_admin_key_generator(token=token)
    return gr_redis.delete(key)


def black_list_bearer_tokens(access_token: str):
    return f"black-list-token-{access_token}"


def add_token_blacklist(access_token: str, refresh_token: str):
    for token in [access_token, refresh_token]:
        key = black_list_bearer_tokens(access_token=token)
        gr_redis.set(name=key, value=token, ex=60 * 60 * 24)


def get_token_blacklist(token: str):
    key = black_list_bearer_tokens(access_token=token)
    return gr_redis.get(name=key)
