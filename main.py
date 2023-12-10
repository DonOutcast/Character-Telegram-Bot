import asyncio

from aiogram import Bot, Dispatcher
from aiohttp import ClientTimeout
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings
from routrer import simple_router
from middleware import AiohttpSessionMiddleware, DbSessionMiddleware

TOKEN = settings.bot_token
dp = Dispatcher()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    engine = create_async_engine(
        url=settings.get_postgresql_url,
        echo=True
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    await bot.delete_my_commands()
    dp.include_routers(simple_router)
    dp.message.middleware(AiohttpSessionMiddleware(ClientTimeout(total=1, connect=5)))
    dp.message.outer_middleware(DbSessionMiddleware(session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
