from random import choice

from aiogram.utils.markdown import hbold

from src.utils.config import users_entrance
from src.utils.config import throttled_answers


def users_entrance_generator(mention: str, subject: str) -> str:
    return choice(users_entrance).format(mention=mention, subject=hbold(subject))


def throttled_answers_generator(limit: int) -> str:
    return choice(throttled_answers).format(limit=limit)
