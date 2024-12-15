from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup


class AppleForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_type = State()
    waiting_for_description = State()
    waiting_for_image_url = State()


class AppleUpdateForm(StatesGroup):
    waiting_for_apple_id = State()
    waiting_for_name = State()
    waiting_for_type = State()
    waiting_for_description = State()
    waiting_for_image_url = State()
