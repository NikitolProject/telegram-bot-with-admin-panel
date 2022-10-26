from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ('ConfirmUserState',)


class ConfirmUserState(StatesGroup):
    IncomerUser = State()
