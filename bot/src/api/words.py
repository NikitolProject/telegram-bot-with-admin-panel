from src.api import api
from src.events import bot
from src.utils import config

__all__ = ('add_swear_word',)


@api.add_function
async def add_swear_word(word: str, chats: list) -> bool:
    print(word, chats)
    config.mate.append({"word": word, "chats": chats})
    print({"word": word, "chats": chats} in config.mate)
    return True
