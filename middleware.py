from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiohttp import ClientSession, ClientTimeout
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class AiohttpSessionMiddleware(BaseMiddleware):
    def __init__(self, aiohttp_timeout: ClientTimeout):
        super().__init__()
        self.aiohttp_session_timeout = aiohttp_timeout

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        async with ClientSession(timeout=self.aiohttp_session_timeout) as aiohttp_session:
            aiohttp_session.connector._ssl = False
            data["aiohttp_session"] = aiohttp_session
            return await handler(event, data)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
        ) -> Any:
        session: AsyncSession
        async with self.session_pool() as db_session:
            data["db_session"] = db_session
            return await handler(event, data)

