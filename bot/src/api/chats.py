import os
import asyncio

from urllib import request

from aiogram.types import Chat, InputFile

from src.api import api
from src.events import bot

__all__ = ('update_chat',)


@api.add_function
async def update_chat(chat_id: str, title: str, description: str, avatar: str) -> bool:
    chat: Chat = await bot.get_chat(chat_id=int(chat_id))

    if chat.title != title:
        await chat.set_title(title)
    
    if chat.description != description:
        await chat.set_description(description)
    
    await chat.set_photo(InputFile(open(f"../admin/media/{avatar}", "rb")))

    return True
