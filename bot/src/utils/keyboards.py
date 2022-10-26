import random

from typing import Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.config import NUM_BUTTONS
from src.utils.misc.emojies import emojies

confirming_callback = CallbackData("confirm", "subject", "necessary_subject", "user_id", "username")


def generate_confirm_markup(user_id: int, username: str) -> Tuple[InlineKeyboardMarkup, str]:
    """
    Функция, создающая клавиатуру для подтверждения, что пользователь не является ботом
    """
    confirm_user_markup = InlineKeyboardMarkup(row_width=NUM_BUTTONS)
    subjects = random.sample(emojies, NUM_BUTTONS)
    necessary_subject = random.choice(subjects)

    for emoji in subjects:
        button = InlineKeyboardButton(
            text=emoji.unicode,
            callback_data=confirming_callback.new(
                subject=emoji.subject, 
                necessary_subject=necessary_subject.subject, 
                user_id=user_id,
                username=username
            )
        )
        confirm_user_markup.insert(button)

    return confirm_user_markup, necessary_subject.name
