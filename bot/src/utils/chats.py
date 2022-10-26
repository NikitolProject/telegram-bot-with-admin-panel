from select import select
from typing import List

from requests import post

from pony.orm import db_session, select

from src.database import TelegramChat, TelegramUser

__all__ = (
    'get_all_chat_ids',
    'check_user_in_chat',
    'check_exited_users'
)


@db_session
def get_all_chat_ids() -> List[int]:
    return list(select(int(c.chat_id) for c in TelegramChat))


@db_session
def check_user_in_chat(user_id: int, chat_id: int, username: str) -> int:
    user = TelegramUser.get(user_id=str(user_id), chat_id=str(chat_id))

    if user is None:
         post(
            "http://127.0.0.1:8000/api/v1/telegram-user",
            json={
                "user_id": str(user_id),
                "chat_id": str(chat_id),
                "username": username
            }
        )
    elif user.username != username:
        user.username = username

    return user_id


@db_session
def check_exited_users(user_ids: List[int], chat_id: int) -> None:
    for user in TelegramUser.select(lambda u: u.chat_id == chat_id):
        if user.user_id in user_ids:
            continue
        user.delete()
