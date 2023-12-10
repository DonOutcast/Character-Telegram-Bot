from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiohttp import ClientSession
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from fsm import CharacterState
from services.open_ai import send_to_gpt
from services.render import render
from services.amplitude import send_amplitude_event
from services.db_requests import user_exists, add_user, fill_character, get_character_answer, save_user_request_response
from services.utils import get_user_response_from_data

simple_router = Router()


@simple_router.message(CommandStart())
async def user_start(message: Message, aiohttp_session: ClientSession, db_session: AsyncSession, state: FSMContext) -> None:
    await message.answer(
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Жми сюда!",
                        web_app=WebAppInfo(url="https://donoutcast.github.io")
                    )
                ]
            ]
        ),
        text=render.get_template(template_name="start.html")

    )
    await send_amplitude_event(aiohttp_session, user_id=message.from_user.id, event_type="sign up")
    if not await user_exists(session=db_session, user_id=message.from_user.id):
        await add_user(
            session=db_session,
            user_id=message.from_user.id,
            username=message.from_user.full_name,
            name=message.from_user.first_name,
            surname=message.from_user.last_name
        )
    await state.set_state(CharacterState.role)


@simple_router.message(Command("menu"))
async def web_app_menu(message: Message, state: FSMContext) -> None:
    await message.answer(
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="Жми сюда!",
                        web_app=WebAppInfo(url="https://donoutcast.github.io")
                    )
                ]
            ]
        ),
        text=render.get_template(template_name="menu.html", data={"user_name": message.from_user.full_name})
    )
    await state.set_state(CharacterState.role)


@simple_router.message(F.web_app_data)
async def web_app(message: Message, aiohttp_session: ClientSession, db_session: AsyncSession,
                  state: FSMContext) -> None:
    character = message.web_app_data.data
    message_from_character = ""
    await send_amplitude_event(aiohttp_session, user_id=message.from_user.id,
                               event_type=f"choose character {character}")
    if answer := await get_character_answer(session=db_session, character_name=character) is None:
        await fill_character(db_session)
    else:
        message_from_character = answer
    await message.answer(text=render.get_template(
        "character.html",
        data={
            "character": character,
            "message_from_character": message_from_character
        }
    )
    )
    await state.update_data(role=character)
    await state.set_state(CharacterState.end)


@simple_router.message(CharacterState.end)
async def user_request(message: Message, aiohttp_session: ClientSession, db_session: AsyncSession,
                       state: FSMContext) -> None:
    user_request = message.text
    state_data = await state.get_data()
    await send_amplitude_event(aiohttp_session, user_id=message.from_user.id,
                               event_type=f"Send request")
    data = await send_to_gpt(user_message=user_request, user_character=state_data.get("role"))
    user_response = get_user_response_from_data(data)
    if user_response:
        await send_amplitude_event(aiohttp_session, user_id=message.from_user.id,
                                   event_type=f"Have a response")
        await save_user_request_response(
            session=db_session,
            user_id=message.from_user.id,
            user_request=user_request,
            user_response=user_response
        )
        await message.answer(text=render.get_template(
            "gpt_200.html",
            data={
                "user_response": user_response
            }
        )
        )
    else:
        await message.answer(text=render.get_template("gpt_error.html"))
    await state.clear()
