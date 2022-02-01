from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession


async def object_exists(session: AsyncSession, statement):
    statement = exists(statement).select()
    result = await session.execute(statement)
    is_object_exists = result.scalar()
    return is_object_exists