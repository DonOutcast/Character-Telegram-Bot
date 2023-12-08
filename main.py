import asyncio
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from utils import os_getenv
from configurate import settings

TOKEN = settings.bot_token
dp = Dispatcher()
main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}")


@main_router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN)
    dp.include_routers(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
