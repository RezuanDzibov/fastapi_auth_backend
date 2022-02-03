from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, insert, update
from sqlalchemy.orm import Load
from starlette.background import BackgroundTasks

from src.auth.security import get_password_hash, verify_password
from src.auth.send_email import send_new_account_email
from src.auth import services as auth_services
from src.base.crud_utils import object_exists
from src.models.db import async_session_maker
from src.user.schemas import UserRegistrationIn
from src.models.user import User


async def create_user(session: AsyncSession, new_user: UserRegistrationIn, task: BackgroundTasks):
    statement = select(User).where(or_(User.username == new_user.username, User.email == new_user.email))
    is_object_exists = await object_exists(session=session, statement=statement)
    if is_object_exists:
        raise HTTPException(
            status_code=409,
            detail=f'User with username: {new_user.username} or email: {new_user.email} exists'
        )
    raw_password = new_user.dict().pop('password')
    hash_password = get_password_hash(raw_password)
    new_user.password = hash_password
    statement = insert(User).values(**new_user.dict()).returning(User.id)
    result = await session.execute(statement)
    await session.commit()
    user_id = result.scalar()
    verification_id = await auth_services.create_verification(session=session, user_id=str(user_id))
    task.add_task(
        send_new_account_email, new_user.email, new_user.username, raw_password, verification_id
    )


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


async def get_user(session: AsyncSession, where_statements: list):
    async with async_session_maker() as session:
        statement = select(User).where(*where_statements)
        result = await session.execute(statement)
        user = result.scalar()
        return user


async def update_user(session: AsyncSession, user_id: UUID, to_update: dict):
    statement = update(User).where(User.id == user_id).values(**to_update)
    await session.execute(statement)
    await session.commit()