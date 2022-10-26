from typing import Optional, List

from requests import get

from pony.orm import db_session

from src.database import TelegramChat, TelegramUser
from src.utils.exceptions import (
    ChatNotFoundException, MatfilterDisabledException,
    AntispamFilterDisabledException, CaptchaModuleDisabledException
)

__all__ = (
    'distance_for_matfilter',
    'check_activate_matfilter_module',
    'check_activate_antispam_module',
    'check_activate_captha_module',
    'get_time_delete_messages_from_bot',
    'add_new_user', 'add_new_chat', 
    'delete_user', 'get_swear_words'
)


def distance_for_matfilter(a: str, b: str) -> int: 
    n, m = len(a), len(b)
        

    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)

    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n

        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]

            if a[j - 1] != b[i - 1]:
                change += 1

            current_row[j] = min(add, delete, change)

    return current_row[n]


@db_session
def check_activate_matfilter_module(chat_id: int, title: str, description: str, mention: str) -> Optional[bool]:
    chat = TelegramChat.get(chat_id=str(chat_id))
    
    if chat is None:
        TelegramChat(
            chat_id=str(chat_id), title=title, description=description if description else "none",
            mention=mention if mention else "none", matfilter=True, spamfilter=True, captha=True,
            time_delete_messages_from_bot=10
        )
        return True

    if not chat.matfilter:
        raise MatfilterDisabledException(title)

    return True


@db_session
def check_activate_antispam_module(chat_id: int, title: str, description: str, mention: str) -> Optional[bool]:
    chat = TelegramChat.get(chat_id=str(chat_id))
    
    if chat is None:
        TelegramChat(
            chat_id=str(chat_id), title=title, description=description if description else "none",
            mention=mention if mention else "none", matfilter=True, spamfilter=True, captha=True,
            time_delete_messages_from_bot=10
        )
        return True

    if not chat.spamfilter:
        raise AntispamFilterDisabledException(title)

    return True


@db_session
def check_activate_captha_module(chat_id: int, title: str, description: str, mention: str) -> Optional[bool]:
    chat = TelegramChat.get(chat_id=str(chat_id))
    
    if chat is None:
        TelegramChat(
            chat_id=str(chat_id), title=title, description=description if description else "none",
            mention=mention if mention else "none", matfilter=True, spamfilter=True, captha=True,
            time_delete_messages_from_bot=10
        )
        return True

    if not chat.captha:
        raise CaptchaModuleDisabledException(title)

    return True


def get_swear_words() -> List[dict]:
    return get("http://127.0.0.1:8000/api/v1/swear-words").json()


@db_session
def get_time_delete_messages_from_bot(chat_id: int) -> int:
    chat = TelegramChat.get(chat_id=str(chat_id))
    return chat.time_delete_messages_from_bot


@db_session
def add_new_user(user_id: int, chat_id: int, username: str) -> None:
    user = TelegramUser.get(user_id=str(user_id), chat_id=str(chat_id))

    if user is not None:
        return None

    TelegramUser(
        user_id=str(user_id), chat_id=str(chat_id), username=username
    )


@db_session
def delete_user(user_id: int, chat_id: int) -> None:
    user = TelegramUser.get(user_id=str(user_id), chat_id=str(chat_id))

    if user is None:
        return None

    user.delete()


@db_session
def add_new_chat(chat_id: int, title: str, mention: str, description: str, avatar_url: str) -> None:
    chat = TelegramChat.get(chat_id=str(chat_id))

    if chat is not None:
        return None

    TelegramChat(
        chat_id=str(chat_id), title=title, mention=mention, 
        description=description,
        matfilter=True, spamfilter=True, captha=True
    )
