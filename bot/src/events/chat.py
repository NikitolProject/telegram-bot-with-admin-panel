import asyncio
import contextlib

import requests

from src.events import app, bot

from src.utils import chats, filters

__all__ = ('start_updating_chats',)


async def update_users_from_all_chats() -> None:
    while True:
        chat_ids = chats.get_all_chat_ids()
        users = list()

        async with app:
            for chat_id in chat_ids:
                async for member in app.get_chat_members(chat_id):
                    if member.user.is_bot:
                        continue
                    
                    if member.user.photo is not None:
                        with contextlib.suppress(Exception):
                            files = await bot.get_user_profile_photos(user_id=member.user.id)
                            response = requests.get(
                                bot.get_file_url(
                                    (await bot.get_file(files["photos"][0][-1]["file_id"]))['file_path']
                                ), allow_redirects=True
                            )
                            open(f"../admin/media/{member.user.id}.jpg", "wb").write(response.content)

                    users.append(
                        (
                            member.user.id, 
                            chat_id,
                            f"@{member.user.username}"
                            if member.user.username else \
                                f"{member.user.first_name} {member.user.last_name}"
                        )
                    )
        
        for user in users:
            chats.check_user_in_chat(
                user_id=user[0],
                chat_id=user[1],
                username=user[2]
            )

        for chat_id in chat_ids:
            chats.check_exited_users([user[0] for user in users if users[1] == chat_id])
        
        await asyncio.sleep(10 * 60)


async def start_updating_chats() -> None:
    asyncio.run_coroutine_threadsafe(update_users_from_all_chats(), asyncio.get_event_loop())
