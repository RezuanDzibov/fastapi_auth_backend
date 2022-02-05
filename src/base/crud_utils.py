from sqlalchemy import delete, exists, insert, update
from sqlalchemy.ext.asyncio import AsyncSession


async def object_exists(session: AsyncSession, statement):
    statement = exists(statement).select()
    result = await session.execute(statement)
    is_object_exists = result.scalar()
    return is_object_exists


async def update_model_instance(session: AsyncSession, object_, to_update: dict):
    for column_name, column_value in to_update.items():
        if not hasattr(object_, column_name):
            raise AttributeError(f'The object has no column {column_name}')
        setattr(object_, column_name, column_value)
    session.add(object_)
    await session.commit()
    
    
async def update_object(session: AsyncSession, model, where_statements: list, to_update: dict, returning: list):
    statement = update(model).where(*where_statements).values(**to_update).returning(*returning)
    result = await session.execute(statement)
    await session.commit()
    if returning:
        object_ = result.scalar()
        return object_
    return None
    
    
async def insert_object(session: AsyncSession, model, to_insert: dict, returning: list):
    statement = insert(model).values(**to_insert).returning(*returning)
    result = await session.execute(statement)
    await session.commit()
    if returning:
        object_ = result.scalar()
        return object_
    return None


async def delete_object(session: AsyncSession, model, where_statements: list, returning: list):
    statement = delete(model).where(*where_statements).returning(*returning)
    result = await session.execute(statement)
    await session.commit()
    if returning:
        object_ = result.scalar()
        return object_
    return None


async def get_object(session: AsyncSession, statement):
    result = await session.execute(statement)
    object_ = result.scalar()
    return object_