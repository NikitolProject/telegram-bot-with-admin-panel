from aiogram import Dispatcher
from aiogram.utils import executor

from src import dp, start_jsonrpc, start_updating_chats
from src.middlewares.throttling import ThrottlingMiddleware


async def on_startup() -> None:
    await start_jsonrpc()
    await start_updating_chats()


if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=executor.start(dp, on_startup()))
