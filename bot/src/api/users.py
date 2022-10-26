from src.api import api
from src.events import bot
from src.utils import filters

__all__ = ('delete_user_from_chat',)


@api.add_function
async def delete_user_from_chat(user_id: str, chat_id: str) -> bool:
    filters.delete_user(user_id=int(user_id), chat_id=int(chat_id))
    await bot.kick_chat_member(chat_id=int(chat_id), user_id=int(user_id))
    return True
