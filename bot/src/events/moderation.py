import datetime
import asyncio

import requests

from typing import Optional

from pony.orm import db_session

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.exceptions import CantRestrictSelf

from src.events import bot, dp, storage
from src.events.chat import update_users_from_all_chats
from src.database import TelegramUser
from src.utils import (config, filters, keyboards, states)
from src.utils.exceptions import (
    ChatNotFoundException, MatfilterDisabledException, 
    AntispamFilterDisabledException, CaptchaModuleDisabledException
)
from src.utils.misc.phrase_generator import users_entrance_generator


@dp.message_handler(chat_type=['group', 'supergroup'])
async def antispam_filter(message: types.Message) -> None:
    """
    Хэндлер фильтрации спама (возможных вредоносных ссылок).

    TODO: Переделать метод, сделав "редактирование" сообщения вместо его полного удаления.
    """
    try:
        filters.check_activate_antispam_module(
            message.chat.id, message.chat.title, message.chat.description, message.chat.mention
        )
        expired_time = filters.get_time_delete_messages_from_bot(message.chat.id)
    except (ChatNotFoundException, AntispamFilterDisabledException):
        await matfilter_handler(message)
        return None

    phrase = message.text.lower()

    if "http://" in phrase or "https://" in phrase or ".com" in phrase or ".ru" in phrase:
        await bot.delete_message(message.chat.id, message.message_id)
        msg = await bot.send_message(
            message.chat.id, 
            "[{} {}](tg://user?id={}), "
            "твоё сообщение было удалено из-за с"
            "одержания в нём спама! "
                .format(
                    message.from_user.first_name,
                    message.from_user.last_name, 
                    message.from_user.id
                ), 
            disable_web_page_preview=True, 
            parse_mode="Markdown"
        )
        await asyncio.sleep(expired_time)
        return await msg.delete()
    
    await matfilter_handler(message, expired_time)


async def matfilter_handler(message: types.Message, expired_time: int = None) -> None:
    """
    Хэндлер фильтрации матерных слов.
    """
    try:
        filters.check_activate_matfilter_module(
            message.chat.id, message.chat.title, message.chat.description, message.chat.mention
        )

        if expired_time is None:
            expired_time = filters.get_time_delete_messages_from_bot(message.chat.id)

    except (ChatNotFoundException, MatfilterDisabledException):
        return None

    words = [word["word"] for word in config.mate if str(message.chat.id) in word["chats"]]
    phrase = message.text.lower()

    for key, value in config.d.items():
        for letter in value:
            for phr in phrase:
                if letter == phr:
                    phrase = phrase.replace(phr, key)

    for word in words:
        for part in range(len(phrase)):
            fragment = phrase[part: part + len(word)]

            if filters.distance_for_matfilter(fragment, word) > len(word) * 0.15:
                continue
            
            await bot.delete_message(message.chat.id, message.message_id)
            msg = await bot.send_message(
                message.chat.id, 
                "[{} {}](tg://user?id={}), "
                "твоё сообщение было удалено из-за с"
                "одержания в нём запрещённых слов! "
                    .format(
                        message.from_user.first_name,
                        message.from_user.last_name, 
                        message.from_user.id
                    ), 
                disable_web_page_preview=True, 
                parse_mode="Markdown"
            )
            await asyncio.sleep(expired_time)
            await msg.delete()


@dp.message_handler(
    chat_type=['group', 'supergroup'], 
    content_types=types.ContentTypes.NEW_CHAT_MEMBERS
)
async def new_chat_member(message: types.Message) -> None:
    """
    Хэндлер обработки входа нового пользователя.
    """

    try:
        filters.check_activate_captha_module(
            message.chat.id, message.chat.title, message.chat.description, message.chat.mention
        )
    except (ChatNotFoundException, CaptchaModuleDisabledException):
        for new_member in message.new_chat_members:
            filters.add_new_user(
                user_id=new_member.id, chat_id=message.chat.id, 
                username=new_member.username
            )
        return None

    if message.date < datetime.datetime.now() - datetime.timedelta(minutes=1):
        return None

    for new_member in message.new_chat_members:
        try:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=new_member.id,
                permissions=config.NEW_USER_ADDED,
            )
        except CantRestrictSelf:
            return None

    service_messages = list()

    for new_member in message.new_chat_members:
        generated_tuple = keyboards.generate_confirm_markup(new_member.id, new_member.full_name)
        markup = generated_tuple[0]
        subject = generated_tuple[1]

        answer = users_entrance_generator(
            mention=new_member.get_mention(as_html=True), subject=subject
        )
        service_message: types.Message = await message.reply(
            text=answer,
            reply_markup=markup
        )

        await storage.set_state(chat=message.chat.id, user=new_member.id, state=states.ConfirmUserState.IncomerUser)
        state = dp.current_state(user=new_member.id, chat=message.chat.id)
        
        await state.update_data(user_id=new_member.id)
        service_messages.append(service_message)

    await asyncio.sleep(config.ENTRY_TIME)

    for new_member in message.new_chat_members:
        state = dp.current_state(user=new_member.id, chat=message.chat.id)
        data = await state.get_data()

        if data.get('user_id', None):
            until_date = datetime.datetime.now() + datetime.timedelta(seconds=config.BAN_TIME)
            asyncio.user = await bot.get_chat_member(chat_id=message.chat.id, user_id=new_member.id)

            if asyncio.user['status'] != 'kicked':
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=new_member.id, until_date=until_date)
                
            state = dp.current_state(user=new_member.id, chat=message.chat.id)
            await state.finish()

    for service_message in service_messages:
        await service_message.delete()
        await message.delete()


@dp.callback_query_handler(keyboards.confirming_callback.filter(), state="*")
async def user_confirm(query: types.CallbackQuery, callback_data: dict) -> None:
    """
    Хэндлер обрабатывающий нажатие на кнопку.
    """
    subject = callback_data.get("subject")
    necessary_subject = callback_data.get('necessary_subject')
    user_id = int(callback_data.get("user_id"))
    chat_id = int(query.message.chat.id)
    username = callback_data.get('username')

    if query.from_user.id != user_id:
        return await query.answer("Эта кнопочка не для тебя", show_alert=True)

    if subject == necessary_subject:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=config.USER_ALLOWED,
        )
        filters.add_new_user(
            user_id=user_id, chat_id=chat_id, username=username
        )
    else:
        until_date = datetime.datetime.now() + datetime.timedelta(seconds=config.BAN_TIME)
        await bot.kick_chat_member(chat_id=chat_id, user_id=user_id, until_date=until_date)

    state = dp.current_state(user=query.from_user.id, chat=query.message.chat.id)
    await state.finish()

    await query.answer()

    service_message = query.message
    await service_message.delete()


@dp.message_handler(
    chat_type=['group', 'supergroup'], 
    content_types=types.ContentTypes.LEFT_CHAT_MEMBER
)
async def left_chat_member(message: types.Message) -> None:
    """
    Хэндлер обработки выхода участника.
    """
    if message.from_user.id != bot.id:
        return filters.delete_user(message.from_user.id, message.chat.id)
    
