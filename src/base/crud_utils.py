from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession


async def object_exists(session: AsyncSession, statement):
    statement = exists(statement).select()
    result = await session.execute(statement)
    is_object_exists = result.scalar()
    return is_object_exists


async def update_object(session: AsyncSession, object_, to_update: dict):
    for column_name, column_value in to_update.items():
        if not hasattr(object_, column_name):
            raise AttributeError(f'The object has no column {column_name}')
        setattr(object_, column_name, column_value)
    session.add(object_)
    await session.commit()