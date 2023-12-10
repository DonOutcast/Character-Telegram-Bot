from sqlalchemy import delete, insert, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Character, UserRequest


async def add_user(
        session: AsyncSession,
        user_id: int,
        username: str,
        name: str,
        surname: str,
) -> None:
    query = User(
        user_id=user_id,
        username=username,
        name=name,
        surname=surname
    )
    session.add(query)
    await session.commit()


async def user_exists(session: AsyncSession, user_id) -> bool:
    query = select(User).where(User.user_id == user_id)
    response = await session.execute(query)
    return response.scalar()


async def save_user_request_response(
        session: AsyncSession,
        user_id: int,
        user_request: str,
        user_response: str = ""
) -> None:
    query = UserRequest(
        user_id=user_id,
        request=user_request,
        response=user_response
    )
    session.add(query)
    await session.commit()


async def get_character_answer(session: AsyncSession, character_name: str) -> str | None:
    query = select(Character.message).filter_by(name=character_name)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def fill_character(session: AsyncSession) -> None:
    queries = []
    data = {
        0: ["Charizard", "It is said that Charizard’s fire burns hotter if it has experienced harsh battles."],
        1: ["Venusaur", "Its plant blooms when it is absorbing solar energy. It stays on the move to seek sunlight."],
        2: ["Snorlax", "Its stomach can digest any kind of food, even if it happens to be moldy or rotten."],
        3: ["Blastoise",
            "It crushes its foe under its heavy body to cause fainting. In a pinch, it will withdraw inside its shell."],
        4: ["Gyarados",
            "Once it appears, it goes on a rampage. It remains enraged until it demolishes everything around it."],
        5: ["Vaporeon",
            "It lives close to water. Its long tail is ridged with a fin, which is often mistaken for a mermaid’s."]
    }
    for i in range(6):
        row = data.get(i)
        queries.append(
            Character(name=row[0], message=row[1])
        )
    session.add_all(queries)
    await session.commit()
