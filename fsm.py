from aiogram.fsm.state import State, StatesGroup


class CharacterState(StatesGroup):
    role = State()
    end = State()
