from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, insert
from sqlalchemy.orm import Load

from auth.security import get_password_hash, verify_password
from base.crud_utils import object_exists
from core.db import async_session_maker
from user.schemas import UserRegistrationIn
from user.models import User


async def create_user(session: AsyncSession, new_user: UserRegistrationIn):
    statement = select(User).where(or_(User.username == new_user.username, User.email == new_user.email))
    is_object_exists = await object_exists(session=session, statement=statement)
    if is_object_exists:
        raise HTTPException(
            status_code=409,
            detail=f'User with username: {new_user.username} or email: {new_user.email} exists'
        )
    hash_password = get_password_hash(new_user.dict().pop('password'))
    new_user.password = hash_password
    statement = insert(User).values(**new_user.dict()).returning('*')
    await session.execute(statement)
    await session.commit()


async def authenticate(session: AsyncSession, username: str, password: str):
    statement = select(User).options(
        Load(User).load_only(User.password, User.is_active)
    )
    statement = statement.where(User.username == username)
    result = await session.execute(statement)
    user = result.scalar()
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Provided password is incorrect')
    return user


async def get_user_by_id(user_id):
    async with async_session_maker() as session:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar()
        return user